"""Persistent stage results and per-question batch checkpoints."""

import hashlib
import json
import sqlite3
from contextlib import contextmanager


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def key(value):
    return hashlib.sha256(encode(value).encode("utf-8")).hexdigest()


class Store:
    def __init__(self, root):
        root.mkdir(parents=True, exist_ok=True)
        self.root = root
        self.db = sqlite3.connect(root / "state.sqlite3")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS cache (
                stage TEXT, key TEXT, value TEXT NOT NULL, PRIMARY KEY (stage, key));
            CREATE TABLE IF NOT EXISTS batch (
                id TEXT PRIMARY KEY, manifest TEXT NOT NULL, summary TEXT);
            CREATE TABLE IF NOT EXISTS question (
                batch TEXT, number INTEGER, value TEXT NOT NULL, PRIMARY KEY (batch, number));
        """)

    @contextmanager
    def worker(self):
        # Separate database keeps the worker lock held across checkpoint commits.
        lock = sqlite3.connect(self.root / "worker.sqlite3", timeout=0)
        try:
            try:
                lock.execute("BEGIN EXCLUSIVE")
            except sqlite3.OperationalError as exc:
                raise ValueError("Một batch Local Agent đang chạy.") from exc
            yield
        finally:
            lock.close()

    def cached(self, stage, key):
        row = self.db.execute("SELECT value FROM cache WHERE stage=? AND key=?", (stage, key)).fetchone()
        return json.loads(row[0]) if row else None

    def remember(self, stage, key, value):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO cache VALUES (?, ?, ?)", (stage, key, encode(value)))

    def start(self, batch, manifest):
        with self.db:
            self.db.execute("""
                INSERT INTO batch VALUES (?, ?, NULL)
                ON CONFLICT(id) DO UPDATE SET manifest=excluded.manifest, summary=NULL
            """, (batch, encode(manifest)))

    def batch(self, batch):
        row = self.db.execute("SELECT manifest, summary FROM batch WHERE id=?", (batch,)).fetchone()
        if row is None:
            raise ValueError(f"Không tìm thấy batch {batch}.")
        return json.loads(row[0]), json.loads(row[1]) if row[1] else None

    def questions(self, batch):
        return {number: json.loads(value) for number, value in self.db.execute(
            "SELECT number, value FROM question WHERE batch=?", (batch,))}

    def checkpoint(self, batch, number, value):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO question VALUES (?, ?, ?)", (batch, number, encode(value)))

    def finish(self, batch, summary):
        with self.db:
            self.db.execute("UPDATE batch SET summary=? WHERE id=?", (encode(summary), batch))
