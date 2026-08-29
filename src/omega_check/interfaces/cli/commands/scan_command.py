# Copyright (c) 2026 kraynux - Licence MIT
"""Sous-commande `omega-check scan <cible> --profile <nom>` (Phase 2 — base:
seul --profile est supporte, --port/--range/--ports arrivent en Phase 5)."""
from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from omega_check.application.commands.run_scan import run_scan
from omega_check.application.queries.list_profiles import get_profile
from omega_check.core.enums import ScanMode
from omega_check.interfaces.cli.formatters.text_formatter import format_scan_result

if TYPE_CHECKING:
    # Type uniquement : jamais importe a l'execution (voir main.py, meme
    # raisonnement que omega-scan pour ne pas tirer infrastructure/ dans
    # interfaces/ via app/).
    from omega_check.app.dependency_container import DependencyContainer


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("scan", help="Scanner une cible unique (ports)")
    parser.add_argument("target", help="IP ou hostname de la cible")
    parser.add_argument("--profile", default="minimal", help="Profil de ports (defaut: minimal)")
    parser.set_defaults(handler=handle_scan)


def handle_scan(args: argparse.Namespace, container: DependencyContainer) -> str:
    profile = get_profile(container.profile_repository, args.profile)

    scan, host = run_scan(
        target=args.target,
        ports=profile.ports,
        scan_mode=ScanMode.PROFILE,
        dns_resolver=container.dns_resolver,
        port_prober=container.port_prober,
        http_prober=container.http_prober,
        tls_prober=container.tls_prober,
        ssh_prober=container.ssh_prober,
        vnc_prober=container.vnc_prober,
        generic_prober=container.generic_prober,
        scan_repository=container.scan_repository,
        id_factory=container.id_factory,
        now=container.clock,
        profile_name=profile.name,
        profile_origin=profile.origin,
    )
    return format_scan_result(scan, host)
