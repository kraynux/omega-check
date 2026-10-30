# Copyright (c) 2026 kraynux - Licence MIT
"""Tableau des cibles epinglees (adapte du patron
interfaces/tui/screens/targets.py d'omega-scan, D-007/D-008)."""
from __future__ import annotations

from textual.widgets import DataTable

from omega_check.domain.targets.models import PinnedTarget
from omega_check.shared.i18n import _


class TargetsTable(DataTable[str]):
    """Une ligne par cible epinglee, la plus recente en premier."""

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns(_("Hôte"), _("Épinglé le"), _("Note"))

    def set_targets(self, targets: tuple[PinnedTarget, ...]) -> None:
        self.clear()
        for target in targets:
            self.add_row(target.host, target.pinned_at, target.note or "-", key=target.host)
