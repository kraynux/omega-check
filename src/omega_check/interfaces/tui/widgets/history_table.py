# Copyright (c) 2026 kraynux - Licence MIT
"""Tableau de l'historique des scans (adapte du patron omega-scan/omega-stress,
D-007/D-008 — colonnes propres au modele Scan de CHECK)."""
from __future__ import annotations

from textual.widgets import DataTable

from omega_check.domain.scans.models import Scan


class HistoryTable(DataTable[str]):
    """Une ligne par scan passe, la plus recente en premier."""

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("Cible", "Date", "Profil", "Statut")

    def set_scans(self, scans: tuple[Scan, ...]) -> None:
        self.clear()
        for scan in scans:
            assert scan.id is not None
            self.add_row(
                f"{scan.target} ({scan.target_ip})" if scan.target_ip else scan.target,
                scan.created_at,
                scan.profile_name or "-",
                scan.status.value,
                key=scan.id,
            )
