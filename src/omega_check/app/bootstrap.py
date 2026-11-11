# Copyright (c) 2026 kraynux - Licence MIT
"""Racine de composition : construit un DependencyContainer avec les
adaptateurs concrets de production. Seul module autorise a importer a la
fois infrastructure/ ET app/dependency_container.py."""
from __future__ import annotations

from pathlib import Path

from omega_lib.infrastructure.declaration import build_contact_support
from omega_lib.infrastructure.declaration.app_version import project_version
from omega_lib.infrastructure.terminal.detector import SystemTerminalDetector
from omega_lib.shared.clock import utc_now
from omega_lib.shared.ids import new_id

from omega_check.app.dependency_container import DependencyContainer
from omega_check.infrastructure.config import paths
from omega_check.infrastructure.exporters.exporter import CompositeReportExporter
from omega_check.infrastructure.logging.config import APP_LOG_FILENAME, configure_logging
from omega_check.infrastructure.network.httpx_http_prober import HttpxHttpProber
from omega_check.infrastructure.network.socket_dns_resolver import SocketDnsResolver
from omega_check.infrastructure.network.socket_generic_banner_prober import (
    SocketGenericBannerProber,
)
from omega_check.infrastructure.network.socket_ssh_prober import SocketSshProber
from omega_check.infrastructure.network.socket_vnc_prober import SocketVncProber
from omega_check.infrastructure.network.ssl_tls_prober import SslTlsProber
from omega_check.infrastructure.network.tcp_port_prober import TcpPortProber
from omega_check.infrastructure.storage.files.json_profile_store import JsonProfileStore
from omega_check.infrastructure.storage.files.json_settings_store import JsonSettingsStore
from omega_check.infrastructure.storage.sqlite.connection import open_connection
from omega_check.infrastructure.storage.sqlite.scan_repository import SqliteScanRepository
from omega_check.infrastructure.storage.sqlite.target_repository import SqliteTargetRepository

SOFTWARE = "omega-check"
"""Nom du logiciel pour la reception des declarations et le site (download/)."""
PROJECT_ROOT = Path(__file__).resolve().parents[3]
"""Racine du projet : pyproject.toml, seule source de la version."""


def bootstrap(*, var_dir: Path | None = None, console_logging: bool = True) -> DependencyContainer:
    """`console_logging=False` pour le TUI (voir __main__.py) : Textual
    prend le controle exclusif de l'ecran, une ecriture de log directe sur
    stderr pendant un scan corromprait son rendu. Le CLI garde
    `console_logging=True` par defaut (utile pour le scriptable/debug)."""
    base = var_dir if var_dir is not None else paths.resolve_var_dir()
    configure_logging(log_path=base / APP_LOG_FILENAME, console=console_logging)
    connection = open_connection(paths.default_db_path(base))
    exports_dir = paths.default_exports_dir(base)
    screenshots_dir = paths.default_screenshots_dir(base)

    return DependencyContainer(
        contact_support=build_contact_support(SOFTWARE, project_version(PROJECT_ROOT, SOFTWARE), base),
        dns_resolver=SocketDnsResolver(),
        port_prober=TcpPortProber(),
        http_prober=HttpxHttpProber(),
        tls_prober=SslTlsProber(),
        ssh_prober=SocketSshProber(),
        vnc_prober=SocketVncProber(),
        generic_prober=SocketGenericBannerProber(),
        scan_repository=SqliteScanRepository(connection),
        profile_repository=JsonProfileStore(paths.default_profiles_path(base)),
        target_repository=SqliteTargetRepository(connection),
        report_exporter=CompositeReportExporter(),
        settings_store=JsonSettingsStore(paths.default_settings_path(base)),
        terminal_detector=SystemTerminalDetector(),
        default_exports_dir=exports_dir,
        default_screenshots_dir=screenshots_dir,
        id_factory=new_id,
        clock=utc_now,
        connection=connection,
    )
