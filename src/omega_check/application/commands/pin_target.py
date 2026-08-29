# Copyright (c) 2026 kraynux - Licence MIT
"""Use case : epingler une cible (menu Cibles)."""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from omega_check.domain.targets.models import PinnedTarget
from omega_check.domain.targets.validation import normalize_target_input
from omega_check.ports.target_repository import TargetRepository


def pin_target(
    *,
    target_repository: TargetRepository,
    now: Callable[[], datetime],
    raw_input: str,
    note: str | None = None,
) -> PinnedTarget:
    pinned = PinnedTarget(host=normalize_target_input(raw_input), pinned_at=now().isoformat(), note=note)
    target_repository.pin(pinned)
    return pinned
