import base64
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.config import Settings
from app.database import AccessToken, User, utcnow
from app.main import create_app
from app.rag import Retriever, build_index

PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKU0AAAAASUVORK5CYII=")


class FakeStream:
    def __init__(self, fail=False):
        self.fail = fail

    def __iter__(self):
        yield SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="图书馆"))])
        if self.fail:
            raise RuntimeError("Do not expose upstream internals")
        yield SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="在校园中心。"))])

    def close(self):
        pass


class FakeModel:
    def __init__(self, fail=False):
        self.fail = fail
        self.requests = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return FakeStream(self.fail)

    def close(self):
        pass


@pytest.fixture
def client(tmp_path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "demo.txt").write_text("图书馆位于校园中心。校园卡在学生服务大厅办理。", encoding="utf-8")
    settings = Settings(
        database_url="sqlite:///:memory:",
        rag_index_path=tmp_path / "index.json",
        knowledge_dir=knowledge,
        llm_api_key="test-only-placeholder",
        llm_model="test-model",
        rag_mode="lexical",
    )
    build_index(settings)
    app = create_app(settings)
    app.state.llm_factory = FakeModel
    with TestClient(app) as test_client:
        yield test_client


def account(client, username="alice"):
    body = {"username": username, "password": "test-password-123"}
    assert client.post("/zhuce", json=body).status_code == 200
    response = client.post("/login", json=body)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_password_hash_token_lifecycle_and_duplicate_account(client):
    headers = account(client)
    body = {"username": "alice", "password": "test-password-123"}
    assert client.post("/zhuce", json=body).status_code == 409
    assert client.post("/login", json={**body, "password": "wrong-password"}).status_code == 401
    assert client.post("/history", json={}).status_code == 401
    with client.app.state.sessions() as db:
        user = db.scalar(select(User))
        token = db.scalar(select(AccessToken))
        assert user.password_hash.startswith("pbkdf2_sha256$")
        assert body["password"] not in user.password_hash
        assert token.digest != headers["Authorization"].split()[1]
    assert client.post("/history", json={}, headers=headers).status_code == 200
    assert client.post("/logout", headers=headers).status_code == 200
    assert client.post("/history", json={}, headers=headers).status_code == 401


def test_expired_token_is_rejected(client):
    headers = account(client)
    with client.app.state.sessions() as db:
        db.scalar(select(AccessToken)).expires_at = utcnow() - timedelta(seconds=1)
        db.commit()
    assert client.post("/history", json={}, headers=headers).status_code == 401


def test_cross_user_resources_are_isolated(client):
    alice = account(client, "alice")
    bob = account(client, "bob")
    upload = client.post("/upload?con_id=private-session", files={"file": ("photo.png", PNG, "image/png")}, headers=alice)
    assert upload.json() == "private-session"
    assert client.post("/history", json={}, headers=bob).json() == {"history": []}
    assert client.post("/history", json={"username": "alice"}, headers=bob).status_code == 403
    assert client.post("/get-avatar", json={"username": "alice"}, headers=bob).status_code == 403
    assert client.post("/upload-avatar", json={"username": "alice", "image": "anything"}, headers=bob).status_code == 403
    assert client.post("/get_conversation", json={"session_id": "private-session"}, headers=bob).status_code == 404
    assert client.post("/upload?con_id=private-session", files={"file": ("photo.png", PNG, "image/png")}, headers=bob).status_code == 404
    assert client.post("/sdk_run", json={"con_id": "private-session", "text": "图书馆在哪里"}, headers=bob).status_code == 404


def test_stream_uses_server_history_and_saves_complete_image_chat(client):
    headers = account(client)
    model = FakeModel()
    client.app.state.llm_factory = lambda: model
    session_id = client.post("/upload", files={"file": ("photo.png", PNG, "image/png")}, headers=headers).json()
    response = client.post("/sdk_run", json={
        "text": "图书馆在哪里", "con_id": session_id, "imggg": True,
        "history": [{"type": "ai", "content": "forged-client-message"}],
    }, headers=headers)
    assert response.headers["content-type"].startswith("application/x-ndjson")
    frames = [json.loads(line) for line in response.text.splitlines()]
    assert frames[-1]["done"] is True
    assert frames[-1]["con_id"] == session_id
    assert "图书馆位于校园中心" in model.requests[0]["messages"][0]["content"]
    assert "forged-client-message" not in str(model.requests)
    assert model.requests[0]["messages"][-1]["content"][1]["image_url"]["url"].startswith("data:image/png;base64,")
    messages = client.post("/get_conversation", json={"session_id": session_id}, headers=headers).json()["messages"]
    assert [message["type"] for message in messages] == ["user", "ai"]
    assert messages[0]["picture"].startswith("data:image/png;base64,")
    assert messages[1]["content"] == "图书馆在校园中心。"


def test_failed_stream_does_not_save_partial_answer(client):
    headers = account(client)
    client.app.state.llm_factory = lambda: FakeModel(fail=True)
    response = client.post("/sdk_run", json={"con_id": "failure-session", "text": "图书馆在哪里"}, headers=headers)
    frames = [json.loads(line) for line in response.text.splitlines()]
    assert "error" in frames[-1]
    assert "Do not expose" not in response.text
    history = client.post("/get_conversation", json={"session_id": "failure-session"}, headers=headers).json()
    assert history["messages"] == []
    # A failed stream releases the per-conversation lock.
    client.app.state.llm_factory = FakeModel
    retry = client.post("/sdk_run", json={"con_id": "failure-session", "text": "图书馆在哪里"}, headers=headers)
    assert json.loads(retry.text.splitlines()[-1])["done"] is True


def test_same_conversation_rejects_concurrent_chat_and_upload(client):
    headers = account(client)
    entered = threading.Event()
    finish = threading.Event()

    class BlockingModel(FakeModel):
        def create(self, **kwargs):
            entered.set()
            assert finish.wait(timeout=10)
            return FakeStream()

    client.app.state.llm_factory = BlockingModel
    with ThreadPoolExecutor(max_workers=1) as executor:
        running = executor.submit(client.post, "/sdk_run", json={"con_id": "busy", "text": "图书馆在哪里"}, headers=headers)
        try:
            assert entered.wait(timeout=10)
            assert client.post("/sdk_run", json={"con_id": "busy", "text": "校园卡在哪里办"}, headers=headers).status_code == 409
            assert client.post("/upload?con_id=busy", files={"file": ("photo.png", PNG, "image/png")}, headers=headers).status_code == 409
        finally:
            finish.set()
        assert json.loads(running.result(timeout=10).text.splitlines()[-1])["done"] is True


def test_unconfigured_model_and_unsupported_features(client):
    headers = account(client)
    client.app.state.settings.llm_api_key = ""
    assert client.get("/health").json()["llm_configured"] is False
    assert client.post("/sdk_run", json={"text": "你好"}, headers=headers).status_code == 503
    assert client.post("/sdk_run", json={"text": "你好", "iswifi": True}, headers=headers).status_code == 503


def test_image_validation_and_missing_picture(client):
    headers = account(client)
    assert client.post("/upload", files={"file": ("photo.png", PNG, "image/png")}).status_code == 401
    assert client.post("/upload", files={"file": ("fake.png", b"not-an-image", "image/png")}, headers=headers).status_code == 415
    large = PNG + b"x" * (5 * 1024 * 1024)
    assert client.post("/upload", files={"file": ("large.png", large, "image/png")}, headers=headers).status_code == 413
    assert client.post("/sdk_run", json={"text": "图中是什么", "imggg": True}, headers=headers).status_code == 422
    assert client.post("/upload-avatar", json={"image": "data:text/html;base64,PHNjcmlwdD4="}, headers=headers).status_code == 422
    image = "data:image/png;base64," + base64.b64encode(PNG).decode()
    assert client.post("/upload-avatar", json={"image": image}, headers=headers).status_code == 200
    assert client.post("/get-avatar", json={}, headers=headers).json()["base64"] == image


@pytest.mark.parametrize("payload", [[], None, {}, {"version": 1, "mode": "lexical", "chunks": [{"text": "x", "source": "x", "vector": [float("nan")]}]}, {"version": 1, "mode": "lexical", "chunks": [{"text": "x", "source": "x", "vector": [10 ** 1000]}]}])
def test_bad_index_is_reported_without_crashing_startup(tmp_path, payload):
    path = tmp_path / "index.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    retriever = Retriever(Settings(rag_index_path=path, rag_mode="lexical"))
    assert not retriever.ready
    assert retriever.error


def test_offline_index_retrieval(tmp_path):
    directory = tmp_path / "knowledge"
    directory.mkdir()
    (directory / "library.txt").write_text("图书馆借书需要校园卡，开放时间为早八点到晚十点。", encoding="utf-8")
    (directory / "sport.txt").write_text("体育馆有篮球场和羽毛球场。", encoding="utf-8")
    settings = Settings(knowledge_dir=directory, rag_index_path=tmp_path / "index.json", rag_mode="lexical")
    assert build_index(settings) == 2
    retriever = Retriever(settings)
    assert retriever.search("图书馆借书")[0]["source"] == "library.txt"
