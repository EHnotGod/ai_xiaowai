"""Run explicitly with python -m app.build_index from backend/."""

from .config import Settings
from .rag import build_index


def main():
    settings = Settings()
    try:
        count = build_index(settings)
    except (OSError, ValueError, ImportError) as exc:
        raise SystemExit(f"Index build failed: {exc}") from exc
    print(f"Built {count} chunks ({settings.rag_mode}) -> {settings.rag_index_path}")


if __name__ == "__main__":
    main()
