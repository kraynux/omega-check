# Copyright (c) 2026 kraynux - Licence MIT
"""Normalisation d'une saisie de cible (bounded context 'targets').

Bug reel rapporte : saisir une cible avec un prefixe de schema
('http://'/'https://', copie-collee d'une URL) faisait echouer la
resolution DNS pour 100% des scans (ni `ipaddress.ip_address()` ni
`socket.gethostbyname()` n'acceptent un tel prefixe). Volontairement
simple — pas le `Target`/`parse_target()` complet d'omega-scan
(scope_kind, scan_modes, etc.) : CHECK n'a besoin que de retirer schema/
port/chemin, pas de classifier la cible."""
from __future__ import annotations

_SCHEMES = ("https://", "http://")


def normalize_target_input(raw: str) -> str:
    """'http://exemple.org:8080/chemin' -> 'exemple.org'. Idempotent sur une
    cible deja propre (IP ou hostname nu)."""
    target = raw.strip()

    for scheme in _SCHEMES:
        if target.lower().startswith(scheme):
            target = target[len(scheme) :]
            break

    target = target.split("/", 1)[0]

    if target.count(":") == 1:
        host, _, port = target.partition(":")
        if port.isdigit():
            target = host

    return target
