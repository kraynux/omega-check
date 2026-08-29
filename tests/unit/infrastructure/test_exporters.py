import json

from omega_check.core.enums import ConfidenceLevel, PortState, ScanMode, ScanStatus
from omega_check.domain.scans.models import Scan
from omega_check.domain.services.models import Port, Service
from omega_check.domain.targets.models import Host
from omega_check.infrastructure.exporters.exporter import CompositeReportExporter
from omega_check.infrastructure.exporters.html_exporter import export_html
from omega_check.infrastructure.exporters.json_exporter import export_json
from omega_check.infrastructure.exporters.text_exporter import export_text


def _scan() -> Scan:
    return Scan(
        id="scan-1",
        created_at="2026-08-29T00:00:00+00:00",
        target="192.168.1.10",
        target_ip="192.168.1.10",
        profile_name="minimal",
        profile_origin="system",
        scan_mode=ScanMode.PROFILE,
        status=ScanStatus.COMPLETED,
    )


def _host() -> Host:
    service = Service(
        protocol_name="SSH",
        protocol_confidence=ConfidenceLevel.VERIFIED,
        software="OpenSSH",
        software_confidence=ConfidenceLevel.DECLARED,
        version="10.4",
        role="acces shell",
        role_confidence=ConfidenceLevel.CORROBORATED,
    )
    port = Port(
        port_number=22,
        protocol="tcp",
        state=PortState.OPEN,
        state_confidence=ConfidenceLevel.VERIFIED,
        service=service,
    )
    return Host(ip="192.168.1.10", ports=[port])


def test_export_json_round_trips_via_json_loads() -> None:
    output = export_json(_scan(), _host())
    parsed = json.loads(output)

    assert parsed["scan"]["id"] == "scan-1"
    assert parsed["host"]["ports"][0]["port_number"] == 22
    assert parsed["host"]["ports"][0]["service"]["software"] == "OpenSSH"
    assert parsed["host"]["ports"][0]["service"]["protocol_confidence"] == "verified"


def test_export_json_handles_missing_host() -> None:
    output = export_json(_scan(), None)
    parsed = json.loads(output)
    assert parsed["host"] is None


def test_export_text_contains_key_facts() -> None:
    output = export_text(_scan(), _host())
    assert "scan-1" in output
    assert "22/tcp : open" in output
    assert "OpenSSH 10.4" in output
    assert "acces shell" in output


def test_export_text_handles_missing_host() -> None:
    output = export_text(_scan(), None)
    assert "echoue" in output


def test_export_text_includes_auth_waf_and_tls_details() -> None:
    service = Service(
        protocol_name="HTTPS",
        protocol_confidence=ConfidenceLevel.VERIFIED,
        auth_required=True,
        auth_required_confidence=ConfidenceLevel.VERIFIED,
        auth_types=["Basic"],
        waf_present=True,
        waf_name_guess="Cloudflare",
        waf_confidence=ConfidenceLevel.DECLARED,
        tls_version="TLSv1.3",
        tls_cipher="TLS_AES_256_GCM_SHA384",
        tls_version_confidence=ConfidenceLevel.VERIFIED,
        tls_cert_subject="example.com",
        tls_cert_issuer="Let's Encrypt",
    )
    port = Port(
        port_number=443,
        protocol="tcp",
        state=PortState.OPEN,
        state_confidence=ConfidenceLevel.VERIFIED,
        service=service,
    )
    host = Host(ip="192.168.1.10", ports=[port])

    output = export_text(_scan(), host)

    assert "auth      : requise (Basic)" in output
    assert "WAF       : Cloudflare" in output
    assert "TLS       : TLSv1.3, TLS_AES_256_GCM_SHA384" in output
    assert "certificat: subject=example.com, issuer=Let's Encrypt" in output


def test_export_html_renders_port_and_role() -> None:
    output = export_html(_scan(), _host())
    assert "192.168.1.10" in output
    assert "OpenSSH" in output
    assert "acces shell" in output
    assert "<table>" in output


def test_export_html_handles_missing_host() -> None:
    output = export_html(_scan(), None)
    assert "échoué" in output


def test_export_html_uses_requested_export_theme_palette() -> None:
    from omega_lib.theme.policies import EXPORT_PALETTES

    output = export_html(_scan(), _host(), theme_name="omega-neon")
    assert EXPORT_PALETTES["omega-neon"].background in output
    assert EXPORT_PALETTES["omega-base"].background not in output


def test_export_html_unknown_theme_falls_back_to_default() -> None:
    from omega_lib.theme.policies import EXPORT_PALETTES

    output = export_html(_scan(), _host(), theme_name="does-not-exist")
    assert EXPORT_PALETTES["omega-base"].background in output


def test_composite_exporter_delegates_to_each_format() -> None:
    exporter = CompositeReportExporter()
    scan, host = _scan(), _host()
    assert exporter.export_json(scan, host) == export_json(scan, host)
    assert exporter.export_text(scan, host) == export_text(scan, host)
    assert exporter.export_html(scan, host, "omega-neon") == export_html(scan, host, "omega-neon")
