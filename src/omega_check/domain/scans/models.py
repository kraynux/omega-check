# Copyright (c) 2026 kraynux - Licence MIT
"""Bounded context 'scans' : l'agregat Scan, cycle de vie d'un scan mono-cible."""
from __future__ import annotations

from dataclasses import dataclass, field

from omega_check.core.enums import ScanMode, ScanStatus


@dataclass
class Scan:
    id: str | None = None  # UUID (omega_lib.shared.ids.new_id), voir D-006
    created_at: str = ""
    target: str = ""
    target_ip: str = ""
    profile_name: str | None = None
    profile_origin: str | None = None
    ports_scanned: list[int] = field(default_factory=list)
    scan_mode: ScanMode = ScanMode.PROFILE
    status: ScanStatus = ScanStatus.RUNNING
