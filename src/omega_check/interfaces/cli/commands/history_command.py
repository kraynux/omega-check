# Copyright (c) 2026 kraynux - Licence MIT
"""Sous-commande `omega-check history`."""
from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from omega_check.application.queries.get_scan_history import get_scan_history

if TYPE_CHECKING:
    from omega_check.app.dependency_container import DependencyContainer


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("history", help="Lister les scans precedents")
    parser.add_argument("--target", default=None, help="Filtrer par cible")
    parser.add_argument("--limit", type=int, default=50)
    parser.set_defaults(handler=handle_history)


def handle_history(args: argparse.Namespace, container: DependencyContainer) -> str:
    scans = get_scan_history(container.scan_repository, target=args.target, limit=args.limit)
    if not scans:
        return "Aucun scan enregistre."

    lines = [f"{s.id}  {s.created_at}  {s.target} ({s.target_ip})  {s.status.value}" for s in scans]
    return "\n".join(lines)
