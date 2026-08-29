# Copyright (c) 2026 kraynux - Licence MIT
"""Implementation SQLite du port TargetRepository (ports/target_repository.py)."""
from __future__ import annotations

import sqlite3

from omega_check.domain.targets.models import PinnedTarget
from omega_check.infrastructure.exceptions import StorageError


class SqliteTargetRepository:
    """Implemente ports/target_repository.py::TargetRepository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def pin(self, pinned: PinnedTarget) -> None:
        try:
            self._connection.execute(
                "INSERT OR REPLACE INTO pinned_targets (host, pinned_at, note) VALUES (?, ?, ?)",
                (pinned.host, pinned.pinned_at, pinned.note),
            )
            self._connection.commit()
        except sqlite3.Error as exc:
            raise StorageError(f"echec d'epinglage de la cible {pinned.host!r}") from exc

    def unpin(self, host: str) -> None:
        self._connection.execute("DELETE FROM pinned_targets WHERE host = ?", (host,))
        self._connection.commit()

    def get(self, host: str) -> PinnedTarget | None:
        row = self._connection.execute(
            "SELECT * FROM pinned_targets WHERE host = ?", (host,)
        ).fetchone()
        return self._row_to_target(row) if row is not None else None

    def list_pinned(self) -> tuple[PinnedTarget, ...]:
        rows = self._connection.execute(
            "SELECT * FROM pinned_targets ORDER BY pinned_at DESC"
        ).fetchall()
        return tuple(self._row_to_target(row) for row in rows)

    def clear(self) -> None:
        self._connection.execute("DELETE FROM pinned_targets")
        self._connection.commit()

    @staticmethod
    def _row_to_target(row: sqlite3.Row) -> PinnedTarget:
        return PinnedTarget(host=row["host"], pinned_at=row["pinned_at"], note=row["note"])
