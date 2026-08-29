import pytest

from omega_check.application.commands.export_scan_report import export_scan_report
from omega_check.application.queries.compare_scans import compare_scans
from omega_check.application.queries.get_scan_details import get_scan_details
from omega_check.application.queries.get_scan_history import get_scan_history
from omega_check.core.enums import ConfidenceLevel, PortState, ScanMode, ScanStatus
from omega_check.domain.scans.exceptions import ScanNotFoundError
from omega_check.domain.scans.models import Scan
from omega_check.domain.services.models import Port
from omega_check.domain.targets.models import Host


def _scan(scan_id: str, target: str = "192.168.1.10") -> Scan:
    return Scan(
        id=scan_id,
        created_at="2026-08-29T00:00:00+00:00",
        target=target,
        target_ip=target,
        scan_mode=ScanMode.PROFILE,
        status=ScanStatus.COMPLETED,
    )


class FakeScanRepository:
    def __init__(self) -> None:
        self.scans: dict[str, Scan] = {}
        self.hosts: dict[str, Host] = {}

    def save(self, scan: Scan) -> None:
        self.scans[scan.id] = scan  # type: ignore[index]

    def get(self, scan_id: str) -> Scan | None:
        return self.scans.get(scan_id)

    def list_history(self, *, target: str | None = None, limit: int = 50) -> tuple[Scan, ...]:
        values = list(self.scans.values())
        if target is not None:
            values = [s for s in values if s.target == target]
        return tuple(values[:limit])

    def save_host(self, scan_id: str, host: Host) -> None:
        self.hosts[scan_id] = host

    def get_host(self, scan_id: str) -> Host | None:
        return self.hosts.get(scan_id)

    def clear(self) -> None:
        self.scans.clear()
        self.hosts.clear()


class FakeReportExporter:
    def export_json(self, scan: Scan, host: Host | None) -> str:
        return f"json:{scan.id}"

    def export_text(self, scan: Scan, host: Host | None) -> str:
        return f"text:{scan.id}"

    def export_html(self, scan: Scan, host: Host | None, theme_name: str) -> str:
        return f"html:{scan.id}:{theme_name}"


def test_get_scan_history_returns_all() -> None:
    repo = FakeScanRepository()
    repo.save(_scan("a"))
    repo.save(_scan("b"))
    assert {s.id for s in get_scan_history(repo)} == {"a", "b"}


def test_get_scan_history_filters_by_target() -> None:
    repo = FakeScanRepository()
    repo.save(_scan("a", target="10.0.0.1"))
    repo.save(_scan("b", target="10.0.0.2"))
    result = get_scan_history(repo, target="10.0.0.1")
    assert [s.id for s in result] == ["a"]


def test_get_scan_details_found() -> None:
    repo = FakeScanRepository()
    repo.save(_scan("a"))
    host = Host(ip="10.0.0.1")
    repo.save_host("a", host)

    scan, fetched_host = get_scan_details(repo, "a")
    assert scan.id == "a"
    assert fetched_host is host


def test_get_scan_details_missing_raises() -> None:
    repo = FakeScanRepository()
    with pytest.raises(ScanNotFoundError):
        get_scan_details(repo, "inexistant")


def test_compare_scans_delegates_to_domain_diff() -> None:
    repo = FakeScanRepository()
    repo.save(_scan("a"))
    repo.save(_scan("b"))
    repo.save_host("a", Host(ip="10.0.0.1", ports=[
        Port(port_number=22, protocol="tcp", state=PortState.OPEN, state_confidence=ConfidenceLevel.VERIFIED)
    ]))
    repo.save_host("b", Host(ip="10.0.0.1", ports=[]))

    comparison = compare_scans(repo, "a", "b")

    assert comparison.ports_only_in_a == [22]


def test_export_scan_report_dispatches_by_format() -> None:
    repo = FakeScanRepository()
    repo.save(_scan("a"))
    exporter = FakeReportExporter()

    assert export_scan_report(repo, exporter, "a", "json") == "json:a"
    assert export_scan_report(repo, exporter, "a", "text") == "text:a"
    assert export_scan_report(repo, exporter, "a", "html") == "html:a:omega-base"
    assert export_scan_report(repo, exporter, "a", "html", "omega-neon") == "html:a:omega-neon"


def test_export_scan_report_rejects_unknown_format() -> None:
    repo = FakeScanRepository()
    repo.save(_scan("a"))
    with pytest.raises(ValueError, match="format d'export inconnu"):
        export_scan_report(repo, FakeReportExporter(), "a", "xml")
