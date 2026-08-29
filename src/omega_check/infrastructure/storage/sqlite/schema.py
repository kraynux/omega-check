# Copyright (c) 2026 kraynux - Licence MIT
"""Definition DDL des tables SQLite (Phase 2 : `scans` ; Phase 3.5 ajoute
`hosts`/`ports`/`services`, cascade complete de l'agregat Scan -> Host ->
Port -> Service).

Colonnes choisies pour tenir des maintenant les principes de fusion Suite
(~/DEV/SUITE/DECISIONS_ARCHITECTURE.md D-006) : `id` en UUID (pas
autoincrement), `tool` present des la v1 solo, `created_at` en ISO8601 UTC.
Un index sur `ports.port_number` existe des maintenant pour permettre plus
tard des requetes structurees inter-scans ("tous les 443 ouverts") sans
avoir a deserialiser du JSON — c'est la raison d'etre de tables dediees
plutot qu'une colonne `results_json` fourre-tout (voir D-006)."""
from __future__ import annotations

SCHEMA_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS scans (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        tool TEXT NOT NULL DEFAULT 'check',
        target TEXT NOT NULL,
        target_ip TEXT NOT NULL,
        profile_name TEXT,
        profile_origin TEXT,
        ports_scanned TEXT NOT NULL,
        scan_mode TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_scans_target ON scans (target)
    """,
    """
    CREATE TABLE IF NOT EXISTS hosts (
        id TEXT PRIMARY KEY,
        scan_id TEXT NOT NULL REFERENCES scans (id),
        ip TEXT NOT NULL,
        hostname TEXT,
        os_guess TEXT,
        os_confidence TEXT NOT NULL,
        firewall_network_present INTEGER,
        firewall_network_confidence TEXT NOT NULL,
        waf_present INTEGER,
        waf_name_guess TEXT,
        waf_confidence TEXT NOT NULL,
        exposure TEXT,
        exposure_confidence TEXT NOT NULL
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_hosts_scan_id ON hosts (scan_id)
    """,
    """
    CREATE TABLE IF NOT EXISTS ports (
        id TEXT PRIMARY KEY,
        host_id TEXT NOT NULL REFERENCES hosts (id),
        port_number INTEGER NOT NULL,
        protocol TEXT NOT NULL,
        state TEXT NOT NULL,
        state_confidence TEXT NOT NULL,
        evidence TEXT NOT NULL
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_ports_host_id ON ports (host_id)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_ports_port_number ON ports (port_number)
    """,
    """
    CREATE TABLE IF NOT EXISTS services (
        id TEXT PRIMARY KEY,
        port_id TEXT NOT NULL REFERENCES ports (id),
        protocol_name TEXT,
        protocol_confidence TEXT NOT NULL,
        software TEXT,
        software_confidence TEXT NOT NULL,
        version TEXT,
        version_confidence TEXT NOT NULL,
        role TEXT,
        role_confidence TEXT NOT NULL,
        role_chain TEXT NOT NULL,
        auth_required INTEGER,
        auth_required_confidence TEXT NOT NULL,
        auth_types TEXT NOT NULL,
        auth_types_confidence TEXT NOT NULL,
        auth_details TEXT NOT NULL,
        firewall_app_present INTEGER,
        firewall_app_confidence TEXT NOT NULL,
        waf_present INTEGER,
        waf_name_guess TEXT,
        waf_confidence TEXT NOT NULL,
        tls_library TEXT,
        tls_library_confidence TEXT NOT NULL,
        tls_version TEXT,
        tls_version_confidence TEXT NOT NULL,
        tls_cipher TEXT,
        tls_cipher_confidence TEXT NOT NULL,
        tls_cert_subject TEXT,
        tls_cert_issuer TEXT,
        tls_cert_san TEXT NOT NULL,
        encapsulation_layers TEXT NOT NULL,
        evidence TEXT NOT NULL
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_services_port_id ON services (port_id)
    """,
    """
    CREATE TABLE IF NOT EXISTS pinned_targets (
        host TEXT PRIMARY KEY,
        pinned_at TEXT NOT NULL,
        note TEXT
    )
    """,
)
