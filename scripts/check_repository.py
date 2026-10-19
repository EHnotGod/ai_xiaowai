"""Check files Git would publish without displaying any credential values."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {
    ".zip", ".key", ".pem", ".p12", ".pfx", ".crt", ".db", ".sqlite",
    ".sqlite3", ".bin", ".safetensors", ".faiss", ".pkl", ".pyc",
}
FORBIDDEN_PARTS = {"node_modules", "dist", ".work", ".venv", "__pycache__"}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "API token": re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "database URL with password": re.compile(
        r"(?:mysql|postgres(?:ql)?)(?:\+[a-z0-9_]+)?://[^\s:/]+:([^\s@]+)@",
        re.IGNORECASE,
    ),
    "literal service credential": re.compile(
        r'''(?i)(?:api[_-]?key|appcode|appsecret|access[_-]?token)\s*[=:]\s*["']([A-Za-z0-9_-]{24,})["']'''
    ),
    "literal authorization header": re.compile(
        r"(?i)\b(?:Bearer|APPCODE)\s+([A-Za-z0-9_.-]{24,})\b"
    ),
}
PLACEHOLDER_PASSWORDS = {"password", "your_password", "change_me", "example_password"}


def inspect_content(name: str, raw: bytes, issues: list[str]) -> None:
    if len(raw) > 5 * 1024 * 1024:
        issues.append(f"{name}: file exceeds 5 MiB; review before publishing")
        return
    if Path(name.removesuffix(" [staged]")).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".ico"}:
        return
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        issues.append(f"{name}: unexpected binary file; review before publishing")
        return
    for line_number, line in enumerate(content.splitlines(), 1):
        for label, pattern in SECRET_PATTERNS.items():
            match = pattern.search(line)
            if match and not (
                label == "database URL with password"
                and match.group(1).lower() in PLACEHOLDER_PASSWORDS
            ):
                issues.append(f"{name}:{line_number}: possible {label} (value hidden)")


def check() -> int:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    names = sorted(set(result.stdout.decode("utf-8").split("\0")) - {""})
    staged_result = subprocess.run(
        ["git", "ls-files", "--stage", "-z"], cwd=ROOT, check=True, stdout=subprocess.PIPE
    )
    objects = {}
    for entry in staged_result.stdout.split(b"\0"):
        if entry:
            metadata, name = entry.split(b"\t", 1)
            mode, object_id, stage = metadata.split()
            if stage != b"0":
                print("Resolve Git merge conflicts before running this check.", file=sys.stderr)
                return 1
            objects[name.decode("utf-8")] = object_id.decode("ascii")
    issues: list[str] = []
    for name in names:
        path = ROOT / name
        if (
            path.suffix.lower() in FORBIDDEN_SUFFIXES
            or FORBIDDEN_PARTS.intersection(Path(name).parts)
            or (path.name.startswith(".env") and path.name != ".env.example")
        ):
            issues.append(f"{name}: local/generated/private file must not be published")
            continue
        working = path.read_bytes() if path.is_file() else None
        if working is not None:
            inspect_content(name, working, issues)
        if name in objects:
            staged = subprocess.run(
                ["git", "cat-file", "blob", objects[name]], cwd=ROOT,
                check=True, stdout=subprocess.PIPE,
            ).stdout
            if staged != working:
                inspect_content(f"{name} [staged]", staged, issues)
    if issues:
        print("Repository check failed:")
        for issue in issues:
            print(f"  {issue}")
        return 1
    print(f"Repository check passed: {len(names)} publishable files inspected.")
    print("This checks common mistakes; asset rights and arbitrary secrets need human review.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(check())
    except subprocess.CalledProcessError:
        print("Run this check inside an initialized Git repository.", file=sys.stderr)
        sys.exit(2)
