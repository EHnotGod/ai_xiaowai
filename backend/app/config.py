"""Load local configuration without embedding credentials in source code."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")


def local_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else BACKEND_DIR / path


@dataclass
class Settings:
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///data/xiaowai.db"))
    cors_origins: list[str] = field(default_factory=lambda: os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(","))
    token_ttl_hours: int = field(default_factory=lambda: int(os.getenv("TOKEN_TTL_HOURS", "24")))
    llm_api_key: str = field(default_factory=lambda: os.getenv("LLM_API_KEY", ""))
    llm_base_url: str = field(default_factory=lambda: os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"))
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", ""))
    llm_timeout_seconds: float = field(default_factory=lambda: float(os.getenv("LLM_TIMEOUT_SECONDS", "60")))
    rag_mode: str = field(default_factory=lambda: os.getenv("RAG_MODE", "lexical"))
    embedding_model: str = field(default_factory=lambda: os.getenv("EMBEDDING_MODEL", "moka-ai/m3e-small"))
    knowledge_dir: Path = field(default_factory=lambda: local_path(os.getenv("KNOWLEDGE_DIR", "knowledge")))
    rag_index_path: Path = field(default_factory=lambda: local_path(os.getenv("RAG_INDEX_PATH", "data/knowledge-index.json")))
    max_image_bytes: int = 5 * 1024 * 1024

    @property
    def llm_configured(self) -> bool:
        return bool(self.llm_api_key and self.llm_base_url and self.llm_model)
