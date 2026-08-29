from omega_check.core.enums import ConfidenceLevel
from omega_check.domain.services.models import Service
from omega_check.domain.services.service import merge_probes


def test_merge_takes_non_tls_fields_from_http_and_tls_fields_from_tls() -> None:
    http = Service(
        protocol_name="HTTPS",
        protocol_confidence=ConfidenceLevel.VERIFIED,
        software="nginx",
        software_confidence=ConfidenceLevel.DECLARED,
        evidence=["HTTP 200 OK"],
    )
    tls = Service(
        tls_version="TLSv1.3",
        tls_version_confidence=ConfidenceLevel.VERIFIED,
        tls_cert_subject="example.com",
        evidence=["handshake TLS reussi : TLSv1.3"],
    )

    merged = merge_probes(http=http, tls=tls)

    assert merged.protocol_name == "HTTPS"
    assert merged.software == "nginx"
    assert merged.tls_version == "TLSv1.3"
    assert merged.tls_cert_subject == "example.com"
    assert merged.evidence == ["HTTP 200 OK", "handshake TLS reussi : TLSv1.3"]


def test_merge_with_only_http() -> None:
    http = Service(protocol_name="HTTP")
    assert merge_probes(http=http, tls=None) is http


def test_merge_with_only_tls() -> None:
    tls = Service(tls_version="TLSv1.3")
    assert merge_probes(http=None, tls=tls) is tls


def test_merge_with_neither_returns_empty_service() -> None:
    merged = merge_probes(http=None, tls=None)
    assert merged.protocol_name is None
