# Copyright (c) 2026 kraynux - Licence MIT
"""Export HTML (Jinja2 + theme d'export choisi). Seul module autorise a
importer jinja2 directement — voir contrat import-linter 'jinja2 seulement
dans infrastructure.exporters.html_exporter' dans pyproject.toml.

Systeme de theme d'export porte depuis omega-scan/omega-stress (D-007/D-008,
catalogue dans omega_lib.theme.policies.EXPORT_PALETTES) : independant du
theme d'interface actif au moment du scan — voir html_theme_resolver.py."""
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from omega_lib.theme.policies import DEFAULT_EXPORT_THEME

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host
from omega_check.infrastructure.exporters.html_theme_resolver import resolve_export_palette

_TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)


def export_html(scan: Scan, host: Host | None, theme_name: str = DEFAULT_EXPORT_THEME) -> str:
    template = _env.get_template("scan_report.html.j2")
    palette = resolve_export_palette(theme_name)
    return template.render(scan=scan, host=host, palette=palette)
