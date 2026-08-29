# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de persistance des profils utilisateur.

Les profils systeme (domain/profiles/defaults.py) ne sont jamais persistes
via ce port : ils sont fournis en dur avec l'outil, lecture seule.

Protocol (typage structurel), pas ABC : meme convention que
ports/scan_repository.py et ports/http_prober.py d'omega-scan — les
implementations n'heritent pas explicitement de ce type, voir
infrastructure/storage/files/json_profile_store.py.
"""
from __future__ import annotations

from typing import Protocol

from omega_check.domain.profiles.models import Profile


class ProfileRepository(Protocol):
    """Port consomme par application/commands et application/queries,
    implemente par infrastructure/storage/files/json_profile_store.py."""

    def load_user_profiles(self) -> dict[str, Profile]:
        """Charge les profils utilisateur persistes. dict vide si aucun."""
        ...

    def save_user_profiles(self, profiles: dict[str, Profile]) -> None:
        """Remplace l'integralite des profils utilisateur persistes."""
        ...
