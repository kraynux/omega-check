# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran de detail d'un scan : ports/services/roles + export. Equivalent
CHECK de screens/findings.py chez omega-scan (D-007/D-008) — contenu
different (pas de grade/severite, un tableau de services), meme structure
d'ecran (Header/panel/actions/Footer)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static

from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host
from omega_check.interfaces.tui.screens._base import OmegaScreen
from omega_check.interfaces.tui.screens.export_dialog import ExportDialogScreen
from omega_check.interfaces.tui.widgets.services_table import ServicesTable
from omega_check.shared.i18n import _

if TYPE_CHECKING:
    from omega_check.app.dependency_container import DependencyContainer


class ShowDetailScreen(OmegaScreen):
    def __init__(self, *, container: DependencyContainer, scan: Scan, host: Host | None) -> None:
        super().__init__()
        self._container = container
        self._scan = scan
        self._host = host

    def compose(self) -> ComposeResult:
        scan = self._scan
        yield Header()
        with Vertical(classes="omega-panel"):
            yield Static(_("SCAN {id}").format(id=scan.id), classes="omega-title")
            yield Static(
                _("Cible : {target} ({target_ip}) — profil {value} — statut {value2}").format(target=scan.target, target_ip=scan.target_ip, value=scan.profile_name or '-', value2=scan.status.value),
                classes="omega-subtitle",
            )
            yield ServicesTable(id="services-table")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Exporter"), id="export", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(ServicesTable).set_host(self._host)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return
        if event.button.id == "export":
            self.app.push_screen(
                ExportDialogScreen(container=self._container, scan=self._scan, active_theme=self.app.theme)
            )
