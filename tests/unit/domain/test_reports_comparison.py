from omega_check.core.enums import ConfidenceLevel, PortState, ScanMode, ScanStatus
from omega_check.domain.reports.comparison import compare_hosts
from omega_check.domain.scans.models import Scan
from omega_check.domain.services.models import Port
from omega_check.domain.targets.models import Host


def _scan(scan_id: str) -> Scan:
    return Scan(
        id=scan_id,
        created_at="2026-08-29T00:00:00+00:00",
        target="192.168.1.10",
        target_ip="192.168.1.10",
        scan_mode=ScanMode.PROFILE,
        status=ScanStatus.COMPLETED,
    )


def _port(number: int, state: PortState) -> Port:
    return Port(port_number=number, protocol="tcp", state=state, state_confidence=ConfidenceLevel.VERIFIED)


def test_detects_ports_only_in_a() -> None:
    host_a = Host(ip="192.168.1.10", ports=[_port(22, PortState.OPEN), _port(80, PortState.OPEN)])
    host_b = Host(ip="192.168.1.10", ports=[_port(22, PortState.OPEN)])

    comparison = compare_hosts(_scan("a"), host_a, _scan("b"), host_b)

    assert comparison.ports_only_in_a == [80]
    assert comparison.ports_only_in_b == []
    assert comparison.state_changes == []


def test_detects_ports_only_in_b() -> None:
    host_a = Host(ip="192.168.1.10", ports=[_port(22, PortState.OPEN)])
    host_b = Host(ip="192.168.1.10", ports=[_port(22, PortState.OPEN), _port(443, PortState.OPEN)])

    comparison = compare_hosts(_scan("a"), host_a, _scan("b"), host_b)

    assert comparison.ports_only_in_b == [443]


def test_detects_state_change() -> None:
    host_a = Host(ip="192.168.1.10", ports=[_port(22, PortState.CLOSED)])
    host_b = Host(ip="192.168.1.10", ports=[_port(22, PortState.OPEN)])

    comparison = compare_hosts(_scan("a"), host_a, _scan("b"), host_b)

    assert len(comparison.state_changes) == 1
    change = comparison.state_changes[0]
    assert change.port_number == 22
    assert change.state_a == PortState.CLOSED
    assert change.state_b == PortState.OPEN


def test_no_differences_when_identical() -> None:
    host = Host(ip="192.168.1.10", ports=[_port(22, PortState.OPEN)])
    comparison = compare_hosts(_scan("a"), host, _scan("b"), host)
    assert comparison.ports_only_in_a == []
    assert comparison.ports_only_in_b == []
    assert comparison.state_changes == []


def test_handles_missing_hosts() -> None:
    comparison = compare_hosts(_scan("a"), None, _scan("b"), None)
    assert comparison.ports_only_in_a == []
    assert comparison.ports_only_in_b == []
    assert comparison.state_changes == []
