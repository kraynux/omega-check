# Copyright (c) 2026 kraynux - Licence MIT
"""Implementation composite du port ReportExporter, delegue aux modules
specifiques par format (json_exporter/text_exporter/html_exporter) —
seul point d'entree expose a app/bootstrap.py."""
from __future__ import annotations

from omega_lib.theme.policies import DEFAULT_EXPORT_THEME

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host
from omega_check.infrastructure.exporters.html_exporter import export_html
from omega_check.infrastructure.exporters.json_exporter import export_json
from omega_check.infrastructure.exporters.text_exporter import export_text


class CompositeReportExporter:
    """Implemente ports/report_exporter.py::ReportExporter."""

    def export_json(self, scan: Scan, host: Host | None) -> str:
        return export_json(scan, host)

    def export_text(self, scan: Scan, host: Host | None) -> str:
        return export_text(scan, host)

    def export_html(self, scan: Scan, host: Host | None, theme_name: str = DEFAULT_EXPORT_THEME) -> str:
        return export_html(scan, host, theme_name)
