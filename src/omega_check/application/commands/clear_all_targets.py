# Copyright (c) 2026 kraynux - Licence MIT
"""Use case : supprimer toutes les cibles epinglees (ecran Reglages)."""
from __future__ import annotations

from omega_check.ports.target_repository import TargetRepository


def clear_all_targets(*, target_repository: TargetRepository) -> None:
    target_repository.clear()
