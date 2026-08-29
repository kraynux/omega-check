from omega_check.core.enums import ConfidenceLevel, PortState, ScanMode, ScanStatus
from omega_check.domain.profiles.models import Profile
from omega_check.domain.scans.models import Scan
from omega_check.domain.services.models import Port, RoleElement, Service, TransportLayer
from omega_check.domain.targets.models import Host


def test_confidence_level_reexported_from_omega_lib() -> None:
    from omega_lib.core.confidence import ConfidenceLevel as LibConfidenceLevel

    assert ConfidenceLevel is LibConfidenceLevel


def test_scan_defaults() -> None:
    scan = Scan(target="192.168.1.10")
    assert scan.status == ScanStatus.RUNNING
    assert scan.scan_mode == ScanMode.PROFILE
    assert scan.ports_scanned == []


def test_host_defaults_are_unknown_confidence() -> None:
    host = Host(ip="192.168.1.10")
    assert host.os_confidence == ConfidenceLevel.UNKNOWN
    assert host.waf_confidence == ConfidenceLevel.UNKNOWN
    assert host.ports == []


def test_port_and_service_composition() -> None:
    service = Service(
        protocol_name="HTTP",
        protocol_confidence=ConfidenceLevel.VERIFIED,
        software="NGINX",
        software_confidence=ConfidenceLevel.DECLARED,
    )
    port = Port(
        port_number=80,
        protocol="tcp",
        state=PortState.OPEN,
        state_confidence=ConfidenceLevel.VERIFIED,
        service=service,
    )
    assert port.service is not None
    assert port.service.software_confidence == ConfidenceLevel.DECLARED


def test_role_chain_and_transport_layer() -> None:
    chain = [
        RoleElement(role="reverse proxy", software="NGINX", confidence=ConfidenceLevel.CORROBORATED),
        RoleElement(role="serveur web backend", software="Lighttpd", confidence=ConfidenceLevel.INFERRED),
    ]
    layer = TransportLayer(order=0, layer_type="transport", protocol="tcp")
    assert chain[0].confidence == ConfidenceLevel.CORROBORATED
    assert layer.confidence == ConfidenceLevel.UNKNOWN


def test_profile_defaults() -> None:
    profile = Profile(name="minimal", description="Scan ultra-rapide", ports=[22, 80, 443])
    assert profile.origin == "system"
    assert profile.pinned is False
