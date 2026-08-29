# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de persistance et d'historique des scans (voir
OMEGA-CHECK_SPECIFICATIONS.md §6 et ~/DEV/SUITE/DECISIONS_ARCHITECTURE.md
D-006 : scan_id en UUID, colonne `tool`, DB separee par outil pour l'instant)."""
from __future__ import annotations

from typing import Protocol

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host


class ScanRepository(Protocol):
    """Implemente par infrastructure/storage/sqlite/scan_repository.py."""

    def save(self, scan: Scan) -> None: ...

    def get(self, scan_id: str) -> Scan | None: ...

    def list_history(self, *, target: str | None = None, limit: int = 50) -> tuple[Scan, ...]: ...

    def clear(self) -> None: ...

    def save_host(self, scan_id: str, host: Host) -> None:
        """Persiste l'agregat complet Host -> Port -> Service (cascade),
        associe au scan `scan_id` (Phase 3.5). Remplace tout host deja
        associe a ce scan."""
        ...

    def get_host(self, scan_id: str) -> Host | None: ...
