# Copyright (c) 2026 kraynux - Licence MIT
"""Bounded context 'targets' : la cible scannee (scan fixe, une seule IP/
hostname resolu, aucune derive)."""
from __future__ import annotations

from dataclasses import dataclass, field

from omega_check.core.enums import ConfidenceLevel
from omega_check.domain.services.models import Port


@dataclass
class PinnedTarget:
    """Cible enregistree a l'avance ('cibles epinglees', menu Cibles) pour
    reutilisation rapide dans l'ecran Scanner. Pas de notion d'autorisation
    ici (contrairement a omega-scan) : CHECK ne gate aucun scan sur ce
    modele, c'est un simple carnet d'adresses avec systeme d'epingle."""

    host: str
    pinned_at: str
    note: str | None = None


@dataclass
class Host:
    ip: str
    hostname: str | None = None
    os_guess: str | None = None
    os_confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    firewall_network_present: bool | None = None
    firewall_network_confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    waf_present: bool | None = None
    waf_name_guess: str | None = None
    waf_confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    exposure: str | None = None  # "public", "internal", "mixed", "unknown"
    exposure_confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    ports: list[Port] = field(default_factory=list)
