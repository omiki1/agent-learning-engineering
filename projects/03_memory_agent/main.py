"""Project 03：可查看、修改、删除的 SQLite 长期记忆。"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DB = Path(tempfile.gettempdir()) / "stu_agent_memory.sqlite3"

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class MemoryStore:
    def __init__(self, path: Path) -> None:
        self.conn = sqlite3.connect(path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS preference (user_id TEXT, key TEXT, value TEXT, updated_at TEXT, PRIMARY KEY(user_id,key))")

    def set(self, user_id: str, key: str, value: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute("INSERT INTO preference VALUES (?,?,?,?) ON CONFLICT(user_id,key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at", (user_id, key, value, now))
        self.conn.commit()

    def get(self, user_id: str, key: str) -> str | None:
        row = self.conn.execute("SELECT value FROM preference WHERE user_id=? AND key=?", (user_id, key)).fetchone()
        return row[0] if row else None

    def list(self, user_id: str) -> dict[str, str]:
        rows = self.conn.execute("SELECT key,value FROM preference WHERE user_id=? ORDER BY key", (user_id,)).fetchall()
        return dict(rows)

    def delete(self, user_id: str, key: str) -> None:
        self.conn.execute("DELETE FROM preference WHERE user_id=? AND key=?", (user_id, key)); self.conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("command", nargs="?", choices=["set", "get", "list", "delete"])
    parser.add_argument("user", nargs="?")
    parser.add_argument("key", nargs="?")
    parser.add_argument("value", nargs="?")
    args = parser.parse_args()
    store = MemoryStore(args.db)
    if args.demo:
        store.set("alice", "language", "zh-CN"); store.set("alice", "style", "concise")
        print(json.dumps(store.list("alice"), ensure_ascii=False)); return
    if not args.command or not args.user: parser.error("需要 command 和 user")
    if args.command == "set": store.set(args.user, args.key, args.value)
    elif args.command == "get": print(store.get(args.user, args.key))
    elif args.command == "list": print(json.dumps(store.list(args.user), ensure_ascii=False))
    else: store.delete(args.user, args.key)


if __name__ == "__main__": main()
