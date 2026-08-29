# Copyright (c) 2026 kraynux - Licence MIT
"""Racine des erreurs de la couche interfaces (CLI/TUI)."""
from __future__ import annotations

from omega_check.core.exceptions import OmegaCheckError


class InterfaceError(OmegaCheckError):
    """Racine des echecs propres a la couche de presentation (TUI et CLI)."""


class UserInputError(InterfaceError):
    """Saisie utilisateur invalide avant meme d'atteindre un command/query."""
