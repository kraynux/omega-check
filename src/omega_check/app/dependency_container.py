# Copyright (c) 2026 kraynux - Licence MIT
"""Cablage des adaptateurs concrets derriere les ports — consomme
uniquement par app/bootstrap.py (racine de composition) et par
interfaces/ (sous TYPE_CHECKING uniquement, jamais a l'execution — voir
interfaces/cli/main.py et interfaces/tui/app.py)."""
from __future__ import annotations

import sqlite3
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from omega_lib.shared.typing import IdFactory

from omega_check.ports.dns_resolver import DnsResolver
from omega_check.ports.generic_banner_prober import GenericBannerProber
from omega_check.ports.http_prober import HttpProber
from omega_check.ports.port_prober import PortProber
from omega_check.ports.profile_repository import ProfileRepository
from omega_check.ports.report_exporter import ReportExporter
from omega_check.ports.scan_repository import ScanRepository
from omega_check.ports.settings_store import SettingsStore
from omega_check.ports.ssh_prober import SshProber
from omega_check.ports.target_repository import TargetRepository
from omega_check.ports.terminal_detector import TerminalDetector
from omega_check.ports.tls_prober import TlsProber
from omega_check.ports.vnc_prober import VncProber


@dataclass
class DependencyContainer:
    dns_resolver: DnsResolver
    port_prober: PortProber
    http_prober: HttpProber
    tls_prober: TlsProber
    ssh_prober: SshProber
    vnc_prober: VncProber
    generic_prober: GenericBannerProber
    scan_repository: ScanRepository
    profile_repository: ProfileRepository
    target_repository: TargetRepository
    report_exporter: ReportExporter
    settings_store: SettingsStore
    terminal_detector: TerminalDetector
    default_exports_dir: Path
    default_screenshots_dir: Path
    id_factory: IdFactory
    clock: Callable[[], datetime]
    connection: sqlite3.Connection

    def close(self) -> None:
        self.connection.close()
