# Copyright (c) 2026 kraynux - Licence MIT
"""Mise en forme texte simple (Phase 2 — base). Pas de couleurs/tableaux
riches ici : Phase 5 pour un affichage complet."""
from __future__ import annotations

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host


def format_scan_result(scan: Scan, host: Host | None) -> str:
    if host is None:
        return f"Scan {scan.id} : ECHEC (resolution DNS impossible pour '{scan.target}')"

    lines = [
        f"Scan {scan.id} — cible {scan.target} ({host.ip}) — statut {scan.status.value}",
        f"{len(host.ports)} port(s) scanne(s) :",
    ]
    for port in sorted(host.ports, key=lambda p: p.port_number):
        lines.append(
            f"  {port.port_number:>5}/{port.protocol} — {port.state.value:<8} "
            f"[{port.state_confidence.value}]"
        )
        service = port.service
        if service is not None and service.protocol_name:
            software = f" {service.software} {service.version or ''}".rstrip() if service.software else ""
            role = f", role={service.role} [{service.role_confidence.value}]" if service.role else ""
            lines.append(f"         └─ {service.protocol_name}{software}{role}")
    return "\n".join(lines)


def format_error(message: str) -> str:
    return f"erreur : {message}"
