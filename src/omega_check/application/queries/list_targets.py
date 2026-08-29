# Copyright (c) 2026 kraynux - Licence MIT
"""Use case de lecture : lister les cibles epinglees (menu Cibles, picker
de l'ecran Scanner)."""
from __future__ import annotations

from omega_check.domain.targets.models import PinnedTarget
from omega_check.ports.target_repository import TargetRepository


def list_targets(*, target_repository: TargetRepository) -> tuple[PinnedTarget, ...]:
    return target_repository.list_pinned()
