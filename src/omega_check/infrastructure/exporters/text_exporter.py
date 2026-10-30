# Copyright (c) 2026 kraynux - Licence MIT
"""Export TXT (rapport, voir OMEGA-CHECK_PLAN_DEV-complet.md §5.2).

Distinct de interfaces/cli/formatters/text_formatter.py : celui-ci produit
un rapport a archiver/partager (plus detaille), l'autre un affichage
ephemere de console — les deux ont vocation a diverger, pas de
mutualisation forcee entre couches infrastructure/ et interfaces/."""
from __future__ import annotations

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host
from omega_check.shared.i18n import _


def export_text(scan: Scan, host: Host | None) -> str:
    lines = [
        _("=== OMEGA-CHECK — Rapport de scan ==="),
        _("Scan ID    : {id}").format(id=scan.id),
        _("Cible      : {target} ({value})").format(target=scan.target, value=scan.target_ip or _("non résolue")),
        _("Date       : {created_at}").format(created_at=scan.created_at),
        _("Profil     : {value} (origine: {value2})").format(value=scan.profile_name or '-', value2=scan.profile_origin or '-'),
        _("Statut     : {value}").format(value=scan.status.value),
        "",
    ]

    if host is None:
        lines.append(_("Aucun résultat (scan échoué)."))
        return "\n".join(lines)

    lines.append(_("{count} port(s) scanné(s) :").format(count=len(host.ports)))
    for port in sorted(host.ports, key=lambda p: p.port_number):
        lines.append(
            f"  - {port.port_number}/{port.protocol} : {port.state.value} "
            f"[{port.state_confidence.value}]"
        )
        service = port.service
        if service is None or not service.protocol_name:
            continue

        lines.append(_("      protocole : {protocol_name} [{value}]").format(protocol_name=service.protocol_name, value=service.protocol_confidence.value))
        if service.software:
            lines.append(
                f"      logiciel  : {service.software} {service.version or ''} "
                f"[{service.software_confidence.value}]".rstrip()
            )
        if service.role:
            lines.append(_("      rôle      : {role} [{value}]").format(role=service.role, value=service.role_confidence.value))
        if service.auth_required is not None:
            auth_desc = "requise" if service.auth_required else _("non requise")
            types = f" ({', '.join(service.auth_types)})" if service.auth_types else ""
            lines.append(_("      auth      : {auth_desc}{types} [{value}]").format(auth_desc=auth_desc, types=types, value=service.auth_required_confidence.value))
        if service.waf_present:
            lines.append(_("      WAF       : {value} [{value2}]").format(value=service.waf_name_guess or _("présent"), value2=service.waf_confidence.value))
        if service.tls_version:
            lines.append(
                _("      TLS       : {tls_version}, {value} [{value2}]").format(tls_version=service.tls_version, value=service.tls_cipher or '?', value2=service.tls_version_confidence.value)
            )
        if service.tls_cert_subject:
            lines.append(_("      certificat: subject={tls_cert_subject}, "
                           "issuer={tls_cert_issuer}").format(tls_cert_subject=service.tls_cert_subject, tls_cert_issuer=service.tls_cert_issuer))

    return "\n".join(lines)
