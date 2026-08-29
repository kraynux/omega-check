from omega_lib.theme.policies import DEFAULT_EXPORT_THEME, EXPORT_PALETTES

from omega_check.infrastructure.exporters.html_theme_resolver import resolve_export_palette


def test_resolve_known_theme() -> None:
    assert resolve_export_palette("omega-neon") == EXPORT_PALETTES["omega-neon"]


def test_resolve_unknown_theme_falls_back_to_default() -> None:
    assert resolve_export_palette("does-not-exist") == EXPORT_PALETTES[DEFAULT_EXPORT_THEME]
