# Copyright (c) 2026 kraynux - Licence MIT
"""Racine des erreurs de la couche application (use cases, pipeline)."""
from __future__ import annotations

from omega_check.core.exceptions import OmegaCheckError


class ApplicationError(OmegaCheckError):
    """Racine des echecs techniques inattendus survenant dans application/
    — jamais utilisee pour un echec metier attendu (voir domain/errors.py)."""


class TargetResolutionError(ApplicationError):
    """Echec de resolution DNS de la cible, bloquant pour tout le scan.

    Definie ici plutot que dans infrastructure/exceptions.py : c'est le
    type technique que application/commands/run_scan.py doit connaitre
    par son nom pour marquer le Scan en FAILED, et la Dependency Rule
    interdit a application/ d'importer infrastructure/ (meme raisonnement
    que ProberFailureError chez omega-scan). infrastructure/network/
    socket_dns_resolver.py importe ce type depuis ICI (sens autorise :
    infrastructure -> application) et le leve."""

    def __init__(self, target: str, reason: str | None = None) -> None:
        message = f"Echec de resolution DNS : {target}"
        if reason:
            message = f"{message} ({reason})"
        super().__init__(message)
        self.target = target
        self.reason = reason


class UnknownThemeError(ApplicationError):
    """Nom de theme demande absent du catalogue omega_lib.theme.policies.TUI_THEMES."""

    def __init__(self, theme_name: str) -> None:
        super().__init__(f"Theme inconnu : '{theme_name}'")
        self.theme_name = theme_name
