# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de resolution DNS (cible -> IP, une seule fois, avant le scan
fixe — voir domain/targets/validation.py pour la regle 'pas de derive')."""
from __future__ import annotations

from typing import Protocol


class DnsResolver(Protocol):
    """Implemente par infrastructure/network/socket_dns_resolver.py."""

    def resolve(self, target: str) -> str:
        """Retourne l'IP resolue de `target` (deja une IP -> retournee
        telle quelle). Leve TargetResolutionError (application/exceptions.py
        — pas infrastructure/, voir la Dependency Rule) si la resolution
        echoue — contrairement au scan de port, une cible non resolue rend
        tout le scan impossible, ce n'est pas un resultat a collecter mais
        un echec bloquant."""
        ...
