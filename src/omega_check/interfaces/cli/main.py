# Copyright (c) 2026 kraynux - Licence MIT
"""Dispatch CLI scriptable (Phase 5 — CLI complete : scan/history/show/compare/profile).

Ne demarre pas l'application lui-meme : __main__.py appelle bootstrap()
puis run(container, argv)."""
from __future__ import annotations

import argparse
import sys
from typing import TYPE_CHECKING

from omega_check.interfaces.cli.commands import (
    compare_command,
    history_command,
    profile_command,
    scan_command,
    show_command,
)
from omega_check.interfaces.cli.formatters.text_formatter import format_error

if TYPE_CHECKING:
    from omega_check.app.dependency_container import DependencyContainer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omega-check", description="Scanneur de ports + services + roles (cible unique)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_command.register(subparsers)
    history_command.register(subparsers)
    show_command.register(subparsers)
    compare_command.register(subparsers)
    profile_command.register(subparsers)
    return parser


def run(container: DependencyContainer, argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        result = args.handler(args, container)
    except Exception as exc:  # noqa: BLE001 — filet de securite generique (meme choix qu'omega-scan)
        print(format_error(str(exc)), file=sys.stderr)
        return 1

    print(result)
    return 0
