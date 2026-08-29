# Copyright (c) 2026 kraynux - Licence MIT
"""Ouverture d'une connexion SQLite configuree pour le projet.

Porte verbatim depuis omega_scan.infrastructure.storage.sqlite.connection
(D-007) : meme raisonnement `check_same_thread=False` (TUI a venir,
worker Textual separe du thread principal, connexion ouverte une seule
fois par app/dependency_container.py)."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from omega_check.infrastructure.storage.sqlite.schema import SCHEMA_STATEMENTS


def open_connection(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    for statement in SCHEMA_STATEMENTS:
        connection.execute(statement)
    connection.commit()
    return connection
