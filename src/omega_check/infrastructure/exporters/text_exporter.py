# Copyright (c) 2026 kraynux - Licence MIT
"""Export TXT (rapport, voir OMEGA-CHECK_PLAN_DEV-complet.md §5.2).

Distinct de interfaces/cli/formatters/text_formatter.py : celui-ci produit
un rapport a archiver/partager (plus detaille), l'autre un affichage
ephemere de console — les deux ont vocation a diverger, pas de
mutualisation forcee entre couches infrastructure/ et interfaces/."""
from __future__ import annotations

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host


def export_text(scan: Scan, host: Host | None) -> str:
    lines = [
        "=== OMEGA-CHECK — Rapport de scan ===",
        f"Scan ID    : {scan.id}",
        f"Cible      : {scan.target} ({scan.target_ip or 'non resolue'})",
        f"Date       : {scan.created_at}",
        f"Profil     : {scan.profile_name or '-'} (origine: {scan.profile_origin or '-'})",
        f"Statut     : {scan.status.value}",
        "",
    ]

    if host is None:
        lines.append("Aucun resultat (scan echoue).")
        return "\n".join(lines)

    lines.append(f"{len(host.ports)} port(s) scanne(s) :")
    for port in sorted(host.ports, key=lambda p: p.port_number):
        lines.append(
            f"  - {port.port_number}/{port.protocol} : {port.state.value} "
            f"[{port.state_confidence.value}]"
        )
        service = port.service
        if service is None or not service.protocol_name:
            continue

        lines.append(f"      protocole : {service.protocol_name} [{service.protocol_confidence.value}]")
        if service.software:
            lines.append(
                f"      logiciel  : {service.software} {service.version or ''} "
                f"[{service.software_confidence.value}]".rstrip()
            )
        if service.role:
            lines.append(f"      role      : {service.role} [{service.role_confidence.value}]")
        if service.auth_required is not None:
            auth_desc = "requise" if service.auth_required else "non requise"
            types = f" ({', '.join(service.auth_types)})" if service.auth_types else ""
            lines.append(f"      auth      : {auth_desc}{types} [{service.auth_required_confidence.value}]")
        if service.waf_present:
            lines.append(f"      WAF       : {service.waf_name_guess or 'present'} [{service.waf_confidence.value}]")
        if service.tls_version:
            lines.append(
                f"      TLS       : {service.tls_version}, {service.tls_cipher or '?'} "
                f"[{service.tls_version_confidence.value}]"
            )
        if service.tls_cert_subject:
            lines.append(f"      certificat: subject={service.tls_cert_subject}, issuer={service.tls_cert_issuer}")

    return "\n".join(lines)
