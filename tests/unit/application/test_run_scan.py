from datetime import datetime, timezone

from omega_check.application.commands.run_scan import run_scan
from omega_check.application.exceptions import TargetResolutionError
from omega_check.core.enums import ConfidenceLevel, PortState, ScanMode, ScanStatus
from omega_check.domain.scans.models import Scan
from omega_check.domain.services.models import Port, Service
from omega_check.domain.targets.models import Host


class FakeDnsResolver:
    def __init__(self, ip: str = "10.0.0.5", fail: bool = False) -> None:
        self._ip = ip
        self._fail = fail

    def resolve(self, target: str) -> str:
        if self._fail:
            raise TargetResolutionError(target)
        return self._ip


class FakePortProber:
    def probe(self, target_ip: str, port: int, protocol: str, timeout: float, retries: int) -> Port:
        return Port(
            port_number=port,
            protocol=protocol,
            state=PortState.OPEN,
            state_confidence=ConfidenceLevel.VERIFIED,
        )


class FakeHttpProber:
    def probe(self, target_ip: str, port: int, host_header: str, timeout: float, use_tls: bool) -> Service:
        return Service(protocol_name="HTTPS" if use_tls else "HTTP")


class FakeTlsProber:
    def probe(self, target_ip: str, port: int, sni_hostname: str, timeout: float) -> Service:
        return Service(tls_version="TLSv1.3")


class FakeSshProber:
    def probe(self, target_ip: str, port: int, timeout: float) -> Service:
        return Service(protocol_name="SSH")


class FakeVncProber:
    def probe(self, target_ip: str, port: int, timeout: float) -> Service:
        return Service(protocol_name="VNC")


class FakeGenericProber:
    def probe(self, target_ip: str, port: int, timeout: float) -> Service:
        return Service()


class FakeScanRepository:
    def __init__(self) -> None:
        self.saved: list[Scan] = []
        self.saved_hosts: dict[str, Host] = {}

    def save(self, scan: Scan) -> None:
        self.saved.append(scan)

    def get(self, scan_id: str) -> Scan | None:
        return next((s for s in self.saved if s.id == scan_id), None)

    def list_history(self, *, target: str | None = None, limit: int = 50) -> tuple[Scan, ...]:
        return tuple(self.saved)

    def save_host(self, scan_id: str, host: Host) -> None:
        self.saved_hosts[scan_id] = host

    def get_host(self, scan_id: str) -> Host | None:
        return self.saved_hosts.get(scan_id)

    def clear(self) -> None:
        self.saved.clear()
        self.saved_hosts.clear()


def _now() -> datetime:
    return datetime(2026, 8, 28, tzinfo=timezone.utc)


def _service_probers() -> dict[str, object]:
    return {
        "http_prober": FakeHttpProber(),
        "tls_prober": FakeTlsProber(),
        "ssh_prober": FakeSshProber(),
        "vnc_prober": FakeVncProber(),
        "generic_prober": FakeGenericProber(),
    }


def test_run_scan_success_path() -> None:
    repo = FakeScanRepository()
    scan, host = run_scan(
        target="example.invalid",
        ports=[22, 80, 443],
        scan_mode=ScanMode.PROFILE,
        dns_resolver=FakeDnsResolver(ip="10.0.0.5"),
        port_prober=FakePortProber(),
        scan_repository=repo,
        id_factory=lambda: "fixed-id",
        now=_now,
        profile_name="minimal",
        profile_origin="system",
        **_service_probers(),  # type: ignore[arg-type]
    )

    assert scan.status == ScanStatus.COMPLETED
    assert scan.target_ip == "10.0.0.5"
    assert host is not None
    assert len(host.ports) == 3
    assert repo.saved == [scan]
    assert repo.saved_hosts["fixed-id"] is host
    # Chaque port OPEN a bien ete identifie (role Phase 4 applique).
    assert all(port.service is not None for port in host.ports)
    assert all(port.service.role is not None for port in host.ports)  # type: ignore[union-attr]


def test_run_scan_dns_failure_path() -> None:
    repo = FakeScanRepository()
    scan, host = run_scan(
        target="does-not-exist.invalid",
        ports=[22, 80],
        scan_mode=ScanMode.PROFILE,
        dns_resolver=FakeDnsResolver(fail=True),
        port_prober=FakePortProber(),
        scan_repository=repo,
        id_factory=lambda: "fixed-id",
        now=_now,
        **_service_probers(),  # type: ignore[arg-type]
    )

    assert scan.status == ScanStatus.FAILED
    assert host is None
    assert repo.saved == [scan]
    assert repo.saved_hosts == {}
