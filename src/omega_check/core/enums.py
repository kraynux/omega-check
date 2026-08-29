# Copyright (c) 2026 kraynux - Licence MIT
"""Vocabulaire transverse : enums utilises par toutes les couches.

ConfidenceLevel n'est PAS defini ici : il vient de omega_lib.core.confidence
(voir OMEGA-CHECK_ARBORESCENCE.md §2 et ~/DEV/SUITE/DECISIONS_ARCHITECTURE.md
D-005). Re-exporte ici pour que le reste de omega_check importe tout son
vocabulaire transverse depuis un seul endroit (`omega_check.core.enums`)
sans se soucier de la frontiere omega-lib/omega-check.
"""
from __future__ import annotations

from enum import Enum

from omega_lib.core.confidence import ConfidenceLevel

__all__ = ["ConfidenceLevel", "PortState", "ScanMode", "ScanStatus"]


class PortState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"


class ScanMode(str, Enum):
    SINGLE_PORT = "single_port"
    RANGE = "range"
    LIST = "list"
    PROFILE = "profile"


class ScanStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
