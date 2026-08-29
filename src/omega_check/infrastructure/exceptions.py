# Copyright (c) 2026 kraynux - Licence MIT
"""Racine des erreurs de la couche infrastructure (adaptateurs concrets)."""
from __future__ import annotations

from omega_check.core.exceptions import OmegaCheckError


class InfrastructureError(OmegaCheckError):
    """Racine des erreurs techniques d'infrastructure. Toute exception
    specifique a une technologie (sqlite3.Error, socket.error...) est
    traduite vers un sous-type de celle-ci par l'adaptateur concerne,
    jamais laissee franchir la frontiere d'un port brute."""


class StorageError(InfrastructureError):
    """Erreur de persistance, traduite depuis sqlite3.Error ou une erreur
    d'ecriture de fichier."""
