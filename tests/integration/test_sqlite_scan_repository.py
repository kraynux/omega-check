from collections.abc import Iterator
from pathlib import Path

import pytest

from omega_check.core.enums import ConfidenceLevel, PortState, ScanMode, ScanStatus
from omega_check.domain.scans.models import Scan
from omega_check.domain.services.models import Port, RoleElement, Service, TransportLayer
from omega_check.domain.targets.models import Host
from omega_check.infrastructure.storage.sqlite.connection import open_connection
from omega_check.infrastructure.storage.sqlite.scan_repository import SqliteScanRepository


@pytest.fixture
def repo(tmp_path: Path) -> Iterator[SqliteScanRepository]:
    connection = open_connection(tmp_path / "omega-check.db")
    try:
        yield SqliteScanRepository(connection)
    finally:
        connection.close()


def _make_scan(**overrides: object) -> Scan:
    defaults: dict[str, object] = {
        "id": "scan-1",
        "created_at": "2026-08-28T00:00:00+00:00",
        "target": "192.168.1.10",
        "target_ip": "192.168.1.10",
        "profile_name": "minimal",
        "profile_origin": "system",
        "ports_scanned": [22, 80, 443],
        "scan_mode": ScanMode.PROFILE,
        "status": ScanStatus.COMPLETED,
    }
    defaults.update(overrides)
    return Scan(**defaults)  # type: ignore[arg-type]


def test_save_and_get_round_trips(repo: SqliteScanRepository) -> None:
    scan = _make_scan()
    repo.save(scan)

    fetched = repo.get("scan-1")
    assert fetched == scan


def test_get_missing_returns_none(repo: SqliteScanRepository) -> None:
    assert repo.get("inexistant") is None


def test_list_history_ordered_and_filtered_by_target(repo: SqliteScanRepository) -> None:
    repo.save(_make_scan(id="a", target="host-a", created_at="2026-08-28T00:00:00+00:00"))
    repo.save(_make_scan(id="b", target="host-b", created_at="2026-08-28T01:00:00+00:00"))
    repo.save(_make_scan(id="c", target="host-a", created_at="2026-08-28T02:00:00+00:00"))

    all_history = repo.list_history()
    assert [s.id for s in all_history] == ["c", "b", "a"]  # plus recent d'abord

    host_a_history = repo.list_history(target="host-a")
    assert [s.id for s in host_a_history] == ["c", "a"]


def test_clear_removes_everything(repo: SqliteScanRepository) -> None:
    repo.save(_make_scan())
    repo.clear()
    assert repo.list_history() == ()


def _make_host_with_full_service() -> Host:
    service = Service(
        protocol_name="HTTPS",
        protocol_confidence=ConfidenceLevel.VERIFIED,
        software="nginx",
        software_confidence=ConfidenceLevel.DECLARED,
        version="1.25.3",
        version_confidence=ConfidenceLevel.DECLARED,
        role="reverse proxy",
        role_confidence=ConfidenceLevel.CORROBORATED,
        role_chain=[
            RoleElement(role="reverse proxy", software="NGINX", confidence=ConfidenceLevel.CORROBORATED),
            RoleElement(role="backend", software="Lighttpd", confidence=ConfidenceLevel.INFERRED),
        ],
        auth_required=True,
        auth_required_confidence=ConfidenceLevel.VERIFIED,
        auth_types=["Basic"],
        auth_types_confidence=ConfidenceLevel.VERIFIED,
        auth_details={"realm": "admin"},
        waf_present=True,
        waf_name_guess="Cloudflare",
        waf_confidence=ConfidenceLevel.DECLARED,
        tls_version="TLSv1.3",
        tls_version_confidence=ConfidenceLevel.VERIFIED,
        tls_cipher="TLS_AES_256_GCM_SHA384",
        tls_cipher_confidence=ConfidenceLevel.VERIFIED,
        tls_cert_subject="example.com",
        tls_cert_issuer="Let's Encrypt",
        tls_cert_san=["DNS:example.com", "DNS:www.example.com"],
        encapsulation_layers=[
            TransportLayer(order=0, layer_type="transport", protocol="tcp"),
            TransportLayer(order=1, layer_type="security", protocol="tls", version="1.3"),
        ],
        evidence=["HTTP 200 OK", "handshake TLS reussi : TLSv1.3"],
    )
    port_with_service = Port(
        port_number=443,
        protocol="tcp",
        state=PortState.OPEN,
        state_confidence=ConfidenceLevel.VERIFIED,
        evidence=["connexion TCP etablie"],
        service=service,
    )
    port_without_service = Port(
        port_number=80,
        protocol="tcp",
        state=PortState.CLOSED,
        state_confidence=ConfidenceLevel.VERIFIED,
    )
    return Host(ip="192.168.1.10", hostname="example.com", ports=[port_with_service, port_without_service])


def test_save_and_get_host_round_trips_full_aggregate(repo: SqliteScanRepository) -> None:
    repo.save(_make_scan(id="scan-host-1"))

    host = _make_host_with_full_service()
    repo.save_host("scan-host-1", host)

    fetched = repo.get_host("scan-host-1")
    assert fetched == host


def test_get_host_missing_returns_none(repo: SqliteScanRepository) -> None:
    assert repo.get_host("inexistant") is None


def test_save_host_replaces_previous_host_for_same_scan(repo: SqliteScanRepository) -> None:
    repo.save(_make_scan(id="scan-host-2"))

    repo.save_host("scan-host-2", Host(ip="10.0.0.1", ports=[]))
    repo.save_host("scan-host-2", Host(ip="10.0.0.2", ports=[]))

    fetched = repo.get_host("scan-host-2")
    assert fetched is not None
    assert fetched.ip == "10.0.0.2"
