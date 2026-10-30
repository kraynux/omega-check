# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran Cibles : carnet d'adresses reutilisables dans l'ecran Scanner
(picker de la section 'Cible', voir scan_setup.py). Adapte du patron
interfaces/tui/screens/targets.py d'omega-scan (D-007/D-008), simplifie :
pas de notion d'autorisation (voir domain/targets/models.py::PinnedTarget)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Input, Static

from omega_check.application.commands.pin_target import pin_target
from omega_check.application.commands.unpin_target import unpin_target
from omega_check.application.queries.list_targets import list_targets
from omega_check.interfaces.tui.screens._base import OmegaScreen
from omega_check.interfaces.tui.widgets.targets_table import TargetsTable
from omega_check.shared.i18n import _

if TYPE_CHECKING:
    from omega_check.app.dependency_container import DependencyContainer


class TargetsScreen(OmegaScreen):
    """Epingler/desepingler des cibles pour l'ecran Scanner."""

    def __init__(self, *, container: DependencyContainer) -> None:
        super().__init__()
        self._container = container
        self._selected_host: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="omega-panel"):
            yield Static(_("CIBLES ÉPINGLÉES"), classes="omega-title")
            yield TargetsTable(id="targets-table")
            yield Input(placeholder=_("ex. 192.168.1.10, example.org"), id="host-input")
            yield Input(placeholder=_("Note (optionnel)"), id="note-input")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Épingler"), id="pin", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Désépingler"), id="unpin")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        targets = list_targets(target_repository=self._container.target_repository)
        self.query_one(TargetsTable).set_targets(targets)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self._selected_host = str(event.row_key.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return

        if event.button.id == "pin":
            raw_input = self.query_one("#host-input", Input).value.strip()
            if not raw_input:
                self.app.notify(_("Saisissez un hôte."), severity="warning")
                return
            note = self.query_one("#note-input", Input).value.strip() or None
            pin_target(
                target_repository=self._container.target_repository,
                now=self._container.clock,
                raw_input=raw_input,
                note=note,
            )
            self.query_one("#host-input", Input).value = ""
            self.query_one("#note-input", Input).value = ""
            self._refresh()
            return

        if event.button.id == "unpin":
            if self._selected_host is None:
                self.app.notify(_("Sélectionnez d'abord une ligne."), severity="warning")
                return
            unpin_target(target_repository=self._container.target_repository, host=self._selected_host)
            self._selected_host = None
            self._refresh()
