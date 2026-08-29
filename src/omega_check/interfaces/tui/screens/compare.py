# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran de comparaison de deux scans. Equivalent CHECK de screens/compare.py
chez omega-scan (D-007/D-008)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Static

from omega_check.application.queries.compare_scans import compare_scans
from omega_check.interfaces.tui.screens._base import OmegaScreen

if TYPE_CHECKING:
    from omega_check.app.dependency_container import DependencyContainer


class CompareScreen(OmegaScreen):
    def __init__(self, *, container: DependencyContainer, scan_id_a: str, scan_id_b: str) -> None:
        super().__init__()
        self._container = container
        self._scan_id_a = scan_id_a
        self._scan_id_b = scan_id_b

    def compose(self) -> ComposeResult:
        comparison = compare_scans(self._container.scan_repository, self._scan_id_a, self._scan_id_b)

        yield Header()
        with VerticalScroll(classes="omega-panel"):
            yield Static("COMPARAISON DE SCANS", classes="omega-title")
            yield Static(f"{comparison.scan_a.id} -> {comparison.scan_b.id}", classes="omega-subtitle")

            if comparison.ports_only_in_a:
                yield Static(f"Ports presents seulement dans {comparison.scan_a.id} :")
                yield Static(", ".join(str(p) for p in comparison.ports_only_in_a))

            if comparison.ports_only_in_b:
                yield Static(f"Ports presents seulement dans {comparison.scan_b.id} :")
                yield Static(", ".join(str(p) for p in comparison.ports_only_in_b))

            if comparison.state_changes:
                yield Static("Changements d'etat :", classes="omega-subtitle")
                for change in comparison.state_changes:
                    yield Static(f"  port {change.port_number} : {change.state_a.value} -> {change.state_b.value}")

            if not (comparison.ports_only_in_a or comparison.ports_only_in_b or comparison.state_changes):
                yield Static("Aucune difference detectee.")

            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button("Retour", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
