# Copyright (c) 2026 kraynux - Licence MIT
"""Use case principal : lancer un scan de ports sur une cible unique
('scan fixe', voir OMEGA-CHECK_SPECIFICATIONS.md §1.2).

Prend une liste de ports deja resolue (depuis un profil ou des options CLI
explicites — voir application/queries/list_profiles.py pour la resolution
d'un nom de profil) : ce use case ne connait que "scanner ces ports sur
cette cible", pas d'ou vient la liste.

Phase 4.3 (integration) : pour chaque port trouve OPEN, identifie le
service via probe_service (Phase 3+4) et persiste l'agregat Host complet."""
from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime

from omega_lib.shared.typing import IdFactory

from omega_check.application.commands.probe_service import probe_service
from omega_check.application.exceptions import TargetResolutionError
from omega_check.core.enums import PortState, ScanMode, ScanStatus
from omega_check.domain.scans.models import Scan
from omega_check.domain.services.models import Port
from omega_check.domain.targets.models import Host
from omega_check.domain.targets.validation import normalize_target_input
from omega_check.ports.dns_resolver import DnsResolver
from omega_check.ports.generic_banner_prober import GenericBannerProber
from omega_check.ports.http_prober import HttpProber
from omega_check.ports.port_prober import PortProber
from omega_check.ports.scan_repository import ScanRepository
from omega_check.ports.ssh_prober import SshProber
from omega_check.ports.tls_prober import TlsProber
from omega_check.ports.vnc_prober import VncProber

_logger = logging.getLogger("omega_check.scan")
"""Nom de logger stable : interfaces/tui/screens/scan_progress.py y attache
un handler temporaire (duree du scan) pour relayer ces lignes vers le
RichLog de ProgressPanel — voir sa propre docstring."""


def run_scan(
    *,
    target: str,
    ports: list[int],
    scan_mode: ScanMode,
    dns_resolver: DnsResolver,
    port_prober: PortProber,
    scan_repository: ScanRepository,
    http_prober: HttpProber,
    tls_prober: TlsProber,
    ssh_prober: SshProber,
    vnc_prober: VncProber,
    generic_prober: GenericBannerProber,
    id_factory: IdFactory,
    now: Callable[[], datetime],
    profile_name: str | None = None,
    profile_origin: str | None = None,
    protocol: str = "tcp",
    timeout: float = 1.0,
    retries: int = 1,
) -> tuple[Scan, Host | None]:
    target = normalize_target_input(target)
    scan = Scan(
        id=id_factory(),
        created_at=now().isoformat(),
        target=target,
        target_ip="",
        profile_name=profile_name,
        profile_origin=profile_origin,
        ports_scanned=list(ports),
        scan_mode=scan_mode,
        status=ScanStatus.RUNNING,
    )

    _logger.info("Resolution DNS de %r...", target)
    try:
        target_ip = dns_resolver.resolve(target)
    except TargetResolutionError as exc:
        _logger.error("Resolution DNS echouee pour %r : %s", target, exc.reason or exc)
        scan.status = ScanStatus.FAILED
        scan_repository.save(scan)
        return scan, None

    _logger.info("Cible resolue : %s -> %s", target, target_ip)
    scan.target_ip = target_ip

    probed_ports: list[Port] = []
    for port in ports:
        _logger.info("Scan du port %s/%s...", port, protocol)
        probed_port = port_prober.probe(target_ip, port, protocol, timeout, retries)
        probed_ports.append(probed_port)
        _logger.info("Port %s/%s : %s", port, protocol, probed_port.state.value)

        if probed_port.state == PortState.OPEN:
            _logger.info("Identification du service sur le port %s...", port)
            probed_port.service = probe_service(
                target_ip=target_ip,
                port=probed_port.port_number,
                host_header=target,
                http_prober=http_prober,
                tls_prober=tls_prober,
                ssh_prober=ssh_prober,
                vnc_prober=vnc_prober,
                generic_prober=generic_prober,
                timeout=timeout,
            )

    host = Host(ip=target_ip, ports=probed_ports)
    scan.status = ScanStatus.COMPLETED
    _logger.info("Scan termine : %d port(s) analyse(s).", len(probed_ports))
    scan_repository.save(scan)
    assert scan.id is not None  # toujours fixe par id_factory() ci-dessus, jamais None en pratique
    scan_repository.save_host(scan.id, host)
    return scan, host
