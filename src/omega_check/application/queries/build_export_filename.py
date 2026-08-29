# Copyright (c) 2026 kraynux - Licence MIT
"""Use case (lecture pure) : construire un nom de fichier d'export explicite
et horodate (retour utilisateur : 'scan-profil-date', 'scan-custom-date',
'scan'). Un scan sans profil (ad-hoc, voir scan_setup.py profil CUSTOM +
saisie libre de ports) n'a pas d'identite de profil -> 'scan' seul."""
from __future__ import annotations

from datetime import datetime

from omega_check.domain.scans.models import Scan

_EXTENSIONS = {"json": "json", "text": "txt", "html": "html"}


def build_export_filename(scan: Scan, fmt: str) -> str:
    date_str = datetime.fromisoformat(scan.created_at).strftime("%Y%m%d-%H%M%S")

    if scan.profile_name is None:
        stem = "scan"
    elif scan.profile_origin == "user":
        stem = "scan-custom"
    else:
        stem = f"scan-{scan.profile_name}"

    return f"{stem}-{date_str}.{_EXTENSIONS[fmt]}"
