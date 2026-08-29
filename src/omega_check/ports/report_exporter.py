# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat d'export de rapport (voir OMEGA-CHECK_SPECIFICATIONS.md §8).

Trois formats en un seul port (plutot que 3 ports separes) : les
consommateurs (application/commands/export_scan_report.py) veulent choisir
le format a l'execution, pas au moment de l'injection de dependance."""
from __future__ import annotations

from typing import Protocol

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host


class ReportExporter(Protocol):
    """Implemente par infrastructure/exporters/exporter.py."""

    def export_json(self, scan: Scan, host: Host | None) -> str: ...

    def export_text(self, scan: Scan, host: Host | None) -> str: ...

    def export_html(self, scan: Scan, host: Host | None, theme_name: str) -> str: ...
