from omega_check.core.enums import ConfidenceLevel
from omega_check.domain.services.policies import (
    classify_http_auth,
    classify_probe_strategy,
    classify_vnc_security,
    detect_waf,
    parse_generic_banner,
    parse_server_header,
    parse_ssh_banner,
)


def test_parse_server_header_with_version() -> None:
    assert parse_server_header("nginx/1.25.3") == ("nginx", "1.25.3")


def test_parse_server_header_without_version() -> None:
    assert parse_server_header("cloudflare") == ("cloudflare", None)


def test_parse_server_header_missing() -> None:
    assert parse_server_header(None) == (None, None)


def test_classify_http_auth_401_with_www_authenticate() -> None:
    required, confidence, types, types_confidence = classify_http_auth(
        401, {"www-authenticate": "Basic realm=\"admin\""}
    )
    assert required is True
    assert confidence == ConfidenceLevel.VERIFIED
    assert types == ["Basic"]
    assert types_confidence == ConfidenceLevel.VERIFIED


def test_classify_http_auth_200_means_no_auth() -> None:
    required, confidence, types, _ = classify_http_auth(200, {})
    assert required is False
    assert confidence == ConfidenceLevel.VERIFIED
    assert types == []


def test_classify_http_auth_403_is_ambiguous() -> None:
    required, confidence, _, _ = classify_http_auth(403, {})
    assert required is None
    assert confidence == ConfidenceLevel.UNKNOWN


def test_detect_waf_via_cf_ray_header() -> None:
    present, name, confidence = detect_waf({"cf-ray": "abc123"})
    assert present is True
    assert name == "Cloudflare"
    assert confidence == ConfidenceLevel.DECLARED


def test_detect_waf_via_server_header_substring() -> None:
    present, name, _ = detect_waf({"server": "cloudflare"})
    assert present is True
    assert name == "Cloudflare"


def test_detect_waf_no_signature() -> None:
    present, name, confidence = detect_waf({"server": "nginx/1.25.3"})
    assert present is None
    assert name is None
    assert confidence == ConfidenceLevel.UNKNOWN


def test_parse_ssh_banner() -> None:
    assert parse_ssh_banner("SSH-2.0-OpenSSH_8.9") == ("OpenSSH", "8.9")


def test_parse_ssh_banner_no_version_suffix() -> None:
    software, version = parse_ssh_banner("SSH-2.0-dropbear")
    assert software == "dropbear"
    assert version is None


def test_parse_ssh_banner_invalid() -> None:
    assert parse_ssh_banner("not a banner") == (None, None)


def test_parse_generic_banner_with_product_version() -> None:
    assert parse_generic_banner("220 ProFTPD/1.3.5e Server ready") == ("ProFTPD", "1.3.5e")


def test_parse_generic_banner_without_recognizable_pattern() -> None:
    assert parse_generic_banner("220 mail.example.com ESMTP Postfix") == (None, None)


def test_classify_probe_strategy() -> None:
    assert classify_probe_strategy(443) == "https"
    assert classify_probe_strategy(8443) == "https"
    assert classify_probe_strategy(80) == "http"
    assert classify_probe_strategy(8080) == "http"
    assert classify_probe_strategy(22) == "ssh"
    assert classify_probe_strategy(5900) == "vnc"
    assert classify_probe_strategy(21) == "generic"


def test_classify_vnc_security_with_none_offered() -> None:
    auth_required, names = classify_vnc_security([1, 2])
    assert auth_required is False
    assert set(names) == {"none", "vnc_auth"}


def test_classify_vnc_security_without_none() -> None:
    auth_required, names = classify_vnc_security([2])
    assert auth_required is True
    assert names == ["vnc_auth"]


def test_classify_vnc_security_empty() -> None:
    assert classify_vnc_security([]) == (None, [])


def test_classify_vnc_security_unknown_code() -> None:
    _, names = classify_vnc_security([99])
    assert names == ["unknown(99)"]
