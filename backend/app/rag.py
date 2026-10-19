"""Small JSON vector index: no pickle and no model downloads at app startup."""

import hashlib
import json
import math
import re
from functools import lru_cache

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import Settings


class LexicalEmbeddings(Embeddings):
    """Offline character n-gram baseline; this is not a semantic language model."""

    def embed_query(self, text: str) -> list[float]:
        compact = "".join(re.findall(r"[\w\u4e00-\u9fff]+", text.lower()))
        features = [compact[i : i + n] for n in (1, 2, 3) for i in range(max(0, len(compact) - n + 1))]
        vector = [0.0] * 1024
        for feature in features:
            bucket = int.from_bytes(hashlib.blake2b(feature.encode(), digest_size=4).digest(), "big") % len(vector)
            vector[bucket] += 1
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]


@lru_cache(maxsize=2)
def embedding_backend(mode: str, model: str, local_only: bool = True) -> Embeddings:
    if mode == "lexical":
        return LexicalEmbeddings()
    if mode != "huggingface":
        raise ValueError("RAG_MODE must be lexical or huggingface")
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError as exc:
        raise ValueError("Install requirements-rag.txt before using huggingface mode") from exc
    return HuggingFaceEmbeddings(
        model_name=model,
        model_kwargs={"trust_remote_code": False, "local_files_only": local_only},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_index(settings: Settings) -> int:
    documents = [
        Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": path.relative_to(settings.knowledge_dir).as_posix()})
        for path in sorted(settings.knowledge_dir.rglob("*.txt"))
    ]
    if not documents:
        raise ValueError("No UTF-8 .txt documents found in KNOWLEDGE_DIR")
    splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=50, separators=["\n\n", "\n", "。", "；", " ", ""])
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("Knowledge documents contain no usable text")
    embeddings = embedding_backend(settings.rag_mode, settings.embedding_model, local_only=False)
    vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])
    payload = {
        "version": 1,
        "mode": settings.rag_mode,
        "model": settings.embedding_model if settings.rag_mode == "huggingface" else None,
        "chunks": [{"text": chunk.page_content, "source": chunk.metadata["source"], "vector": vector} for chunk, vector in zip(chunks, vectors)],
    }
    settings.rag_index_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = settings.rag_index_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    temporary.replace(settings.rag_index_path)
    return len(chunks)


class Retriever:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.chunks: list[dict] = []
        self.error: str | None = None
        try:
            data = json.loads(settings.rag_index_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Index must be a JSON object")
            if data.get("version") != 1 or data.get("mode") != settings.rag_mode:
                raise ValueError("Index version or retrieval mode changed; rebuild it")
            if settings.rag_mode == "huggingface" and data.get("model") != settings.embedding_model:
                raise ValueError("Embedding model changed; rebuild the index")
            chunks = data["chunks"]
            if not isinstance(chunks, list) or not chunks:
                raise ValueError("Index must contain chunks")
            dimension = None
            for chunk in chunks:
                if not isinstance(chunk, dict) or not isinstance(chunk.get("text"), str) or not isinstance(chunk.get("source"), str):
                    raise ValueError("Invalid chunk text/source")
                vector = chunk.get("vector")
                if not isinstance(vector, list) or not vector or any(type(value) not in (int, float) or not math.isfinite(value) for value in vector):
                    raise ValueError("Invalid chunk vector")
                dimension = dimension or len(vector)
                if len(vector) != dimension:
                    raise ValueError("Inconsistent vector dimensions")
            self.chunks = chunks
        except (OSError, ValueError, KeyError, TypeError, OverflowError):
            self.error = "知识索引不可用，请运行 python -m app.build_index 后重启服务。"

    @property
    def ready(self) -> bool:
        return bool(self.chunks) and not self.error

    def search(self, query: str, k: int = 3) -> list[dict]:
        if not self.ready:
            return []
        try:
            vector = embedding_backend(self.settings.rag_mode, self.settings.embedding_model).embed_query(query)
        except Exception as exc:
            raise ValueError("本地检索模型不可用，请安装可选依赖并重新建立索引。") from exc
        ranked = []
        for chunk in self.chunks:
            other = chunk["vector"]
            if len(vector) != len(other):
                raise ValueError("检索向量维度不匹配，请重新建立索引。")
            denominator = math.sqrt(sum(x * x for x in vector) * sum(x * x for x in other)) or 1
            score = sum(a * b for a, b in zip(vector, other)) / denominator
            if score > 0:
                ranked.append({"source": chunk["source"], "text": chunk["text"], "score": round(score, 4)})
        return sorted(ranked, key=lambda item: item["score"], reverse=True)[:k]
