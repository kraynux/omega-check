# Copyright (c) 2026 kraynux - Licence MIT
"""Sous-commande `omega-check compare <scan_id_a> <scan_id_b>` (non listee
dans la CLI d'origine de OMEGA-CHECK_SPECIFICATIONS.md §7.1, mais le use
case compare_scans y est explicitement prevu §6.1 — ajoutee ici pour le
rendre utilisable depuis la CLI plutot que de le laisser mort code)."""
from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from omega_check.application.queries.compare_scans import compare_scans

if TYPE_CHECKING:
    from omega_check.app.dependency_container import DependencyContainer


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("compare", help="Comparer deux scans (etat des ports)")
    parser.add_argument("scan_id_a")
    parser.add_argument("scan_id_b")
    parser.set_defaults(handler=handle_compare)


def handle_compare(args: argparse.Namespace, container: DependencyContainer) -> str:
    comparison = compare_scans(container.scan_repository, args.scan_id_a, args.scan_id_b)

    lines = [f"Comparaison {comparison.scan_a.id} -> {comparison.scan_b.id}"]

    if comparison.ports_only_in_a:
        lines.append(f"Ports presents seulement dans {comparison.scan_a.id} : {comparison.ports_only_in_a}")
    if comparison.ports_only_in_b:
        lines.append(f"Ports presents seulement dans {comparison.scan_b.id} : {comparison.ports_only_in_b}")
    if comparison.state_changes:
        lines.append("Changements d'etat :")
        for change in comparison.state_changes:
            lines.append(f"  port {change.port_number} : {change.state_a.value} -> {change.state_b.value}")

    if len(lines) == 1:
        lines.append("Aucune difference detectee.")

    return "\n".join(lines)
