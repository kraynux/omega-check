# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de persistance des cibles epinglees (menu Cibles).

Protocol (typage structurel), pas ABC : meme convention que
ports/scan_repository.py et ports/profile_repository.py. Porte depuis
ports/target_repository.py d'omega-scan (D-007/D-008), simplifie : pas de
notion d'autorisation (voir domain/targets/models.py::PinnedTarget)."""
from __future__ import annotations

from typing import Protocol

from omega_check.domain.targets.models import PinnedTarget


class TargetRepository(Protocol):
    """Port consomme par application/commands et application/queries,
    implemente par infrastructure/storage/sqlite/target_repository.py."""

    def pin(self, pinned: PinnedTarget) -> None:
        """Enregistre ou remplace (meme hote) une cible epinglee."""
        ...

    def unpin(self, host: str) -> None:
        """Sans effet si `host` n'est pas epingle."""
        ...

    def get(self, host: str) -> PinnedTarget | None: ...

    def list_pinned(self) -> tuple[PinnedTarget, ...]: ...

    def clear(self) -> None:
        """Supprime toutes les cibles epinglees."""
        ...
