# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de la sonde SSH (banner grabbing — voir
OMEGA-CHECK_SPECIFICATIONS.md §4.3)."""
from __future__ import annotations

from typing import Protocol

from omega_check.domain.services.models import Service


class SshProber(Protocol):
    """Implemente par infrastructure/network/socket_ssh_prober.py."""

    def probe(self, target_ip: str, port: int, timeout: float) -> Service:
        """Remplit protocol_name/software/version depuis le banner SSH.
        `auth_types` reste vide (UNKNOWN) en Phase 3 : l'enumeration reelle
        des methodes d'authentification demande un echange de cles SSH
        partiel, hors-scope de cette phase — voir
        OMEGA-CHECK_PLAN_DEV-complet.md Phase 3.2 pour la note de perimetre.
        Ne leve jamais pour un echec de connexion previsible."""
        ...
