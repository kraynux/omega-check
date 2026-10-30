# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran de progression : lance run_scan() dans un worker, sans bloquer l'UI.

Adapte du patron screens/scan_progress.py d'omega-scan (D-007/D-008) : le
spinner indetermine (ProgressPanel) est complete par un relai des lignes de
journal emises par application/commands/run_scan.py (logger
'omega_check.scan') vers le RichLog du panneau, via un logging.Handler
attache pour la duree du scan puis detache dans un `finally` — memes
mecanisme et raison qu'omega-scan (le worker tourne dans un thread via
`asyncio.to_thread`, `app.call_from_thread` est necessaire pour retourner
sur le thread UI avant de toucher un widget)."""
from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.screen import Screen

from omega_check.application.commands.run_scan import run_scan
from omega_check.application.queries.list_profiles import get_profile
from omega_check.core.enums import ScanMode
from omega_check.interfaces.tui.screens.show_detail import ShowDetailScreen
from omega_check.interfaces.tui.widgets.progress_panel import ProgressPanel
from omega_check.shared.i18n import _, log_message

if TYPE_CHECKING:
    from omega_check.app.dependency_container import DependencyContainer


class _RelayHandler(logging.Handler):
    """Relaie chaque record du logger 'omega_check.scan' vers un callback
    (voir _on_log_record ci-dessous) — pas de formattage, juste le message."""

    def __init__(self, callback: Callable[[str], None]) -> None:
        super().__init__()
        self._callback = callback

    def emit(self, record: logging.LogRecord) -> None:
        # Plan i18n R2 : le fichier journal reste en francais, l'ecran retraduit la ligne.
        self._callback(log_message(record.msg, record.args))


class ScanProgressScreen(Screen[None]):
    """Ecran transitoire : disparait des que le scan se termine (succes ->
    ShowDetailScreen remplace cet ecran)."""

    def __init__(
        self,
        *,
        container: DependencyContainer,
        target: str,
        profile_name: str | None = None,
        profile_origin: str | None = None,
        ports: list[int] | None = None,
    ) -> None:
        super().__init__()
        self._container = container
        self._target = target
        self._profile_name = profile_name
        self._profile_origin = profile_origin
        self._ports = ports

    def compose(self) -> ComposeResult:
        yield ProgressPanel(message=_("Scan de {target} en cours...").format(target=self._target))

    def on_mount(self) -> None:
        self.run_worker(self._run_scan(), exclusive=True)

    async def _run_scan(self) -> None:
        container = self._container
        logger = logging.getLogger("omega_check.scan")
        handler = _RelayHandler(self._on_log_record)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        try:
            if self._ports is not None:
                ports, profile_name, profile_origin = self._ports, self._profile_name, self._profile_origin
            else:
                profile = get_profile(container.profile_repository, self._profile_name or "")
                ports, profile_name, profile_origin = profile.ports, profile.name, profile.origin

            def _call_run_scan() -> tuple:
                return run_scan(
                    target=self._target,
                    ports=ports,
                    scan_mode=ScanMode.PROFILE,
                    dns_resolver=container.dns_resolver,
                    port_prober=container.port_prober,
                    http_prober=container.http_prober,
                    tls_prober=container.tls_prober,
                    ssh_prober=container.ssh_prober,
                    vnc_prober=container.vnc_prober,
                    generic_prober=container.generic_prober,
                    scan_repository=container.scan_repository,
                    id_factory=container.id_factory,
                    now=container.clock,
                    profile_name=profile_name,
                    profile_origin=profile_origin,
                )

            scan, host = await asyncio.to_thread(_call_run_scan)
        finally:
            logger.removeHandler(handler)

        if host is None:
            self.app.notify(
                _("Résolution DNS impossible pour '{target}'.").format(target=self._target), title=_("Scan échoué"), severity="error"
            )
            self.dismiss()
            return

        self.app.switch_screen(ShowDetailScreen(container=self._container, scan=scan, host=host))

    def _on_log_record(self, message: str) -> None:
        self.app.call_from_thread(self._write_log_line, message)

    def _write_log_line(self, message: str) -> None:
        if self.is_mounted:
            self.query_one(ProgressPanel).write_line(message)
