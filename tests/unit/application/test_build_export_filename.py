from omega_check.application.queries.build_export_filename import build_export_filename
from omega_check.domain.scans.models import Scan


def _make_scan(**overrides: object) -> Scan:
    defaults: dict[str, object] = {
        "id": "scan-1",
        "created_at": "2026-08-29T14:30:00+00:00",
        "target": "192.168.1.10",
    }
    defaults.update(overrides)
    return Scan(**defaults)  # type: ignore[arg-type]


def test_system_profile_scan_uses_profile_name() -> None:
    scan = _make_scan(profile_name="minimal", profile_origin="system")
    assert build_export_filename(scan, "json") == "scan-minimal-20260829-143000.json"


def test_user_profile_scan_uses_generic_custom_stem() -> None:
    scan = _make_scan(profile_name="monprofil", profile_origin="user")
    assert build_export_filename(scan, "html") == "scan-custom-20260829-143000.html"


def test_ad_hoc_scan_without_profile_uses_bare_stem() -> None:
    scan = _make_scan(profile_name=None, profile_origin=None)
    assert build_export_filename(scan, "text") == "scan-20260829-143000.txt"
