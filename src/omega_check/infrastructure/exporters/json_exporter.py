# Copyright (c) 2026 kraynux - Licence MIT
"""Export JSON (voir OMEGA-CHECK_PLAN_DEV-complet.md §5.2).

`dataclasses.asdict` suffit pour l'integralite de l'agregat Scan/Host
(contrairement au stockage SQLite qui doit aplatir en colonnes) :
ConfidenceLevel etant un str-Enum, `json.dumps` le serialise nativement
sous sa valeur texte, meme imbrique dans Port/Service/RoleElement/
TransportLayer."""
from __future__ import annotations

import json
from dataclasses import asdict

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host


def export_json(scan: Scan, host: Host | None) -> str:
    payload = {
        "scan": asdict(scan),
        "host": asdict(host) if host is not None else None,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)
