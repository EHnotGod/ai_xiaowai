"""Original backend deployment settings; paths are relative to this directory."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def resource_path(name, default):
    path = Path(os.getenv(name, default))
    return str(path if path.is_absolute() else BASE_DIR / path)


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "web")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen-vl-max")
TOOL_API_KEY = os.getenv("TOOL_API_KEY") or LLM_API_KEY
TOOL_BASE_URL = os.getenv("TOOL_BASE_URL") or LLM_BASE_URL
TOOL_MODEL = os.getenv("TOOL_MODEL", "qwen-max-latest")

BOCHA_API_KEY = os.getenv("BOCHA_API_KEY", "")
BOCHA_SEARCH_URL = os.getenv("BOCHA_SEARCH_URL", "https://api.bochaai.com/v1/web-search")
WEATHER_APPCODE = os.getenv("WEATHER_APPCODE", "")
WEATHER_HOST = os.getenv("WEATHER_HOST", "https://ali-weather.showapi.com")
WEATHER_PATH = os.getenv("WEATHER_PATH", "/day15")

EMBEDDING_MODEL_PATH = resource_path("EMBEDDING_MODEL_PATH", "m3e-small")
KNOWLEDGE_DIR = resource_path("KNOWLEDGE_DIR", "linces")
INDEX_DIR = resource_path("INDEX_DIR", "camp")
AVATAR_PATH = resource_path("AVATAR_PATH", "nailong.png")
