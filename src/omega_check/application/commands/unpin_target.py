# Copyright (c) 2026 kraynux - Licence MIT
"""Use case : desepingler une cible (menu Cibles)."""
from __future__ import annotations

from omega_check.ports.target_repository import TargetRepository


def unpin_target(*, target_repository: TargetRepository, host: str) -> None:
    target_repository.unpin(host)
