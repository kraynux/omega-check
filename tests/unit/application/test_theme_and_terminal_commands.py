import pytest
from omega_lib.terminal.models import RenderProfile, TerminalProfile, TerminalSignals

from omega_check.application.commands.select_render_profile import select_render_profile
from omega_check.application.commands.select_theme import select_theme
from omega_check.application.exceptions import UnknownThemeError
from omega_check.application.queries.detect_terminal import detect_terminal


class FakeSettingsStore:
    def __init__(self) -> None:
        self._data: dict[str, str] = {}

    def get(self, key: str, default: str | None = None) -> str | None:
        return self._data.get(key, default)

    def set(self, key: str, value: str) -> None:
        self._data[key] = value

    def all(self) -> dict[str, str]:
        return dict(self._data)


class FakeTerminalDetector:
    def detect(self) -> TerminalSignals:
        return TerminalSignals(family="kitty", columns=200, rows=50)


def test_select_theme_persists_valid_name() -> None:
    store = FakeSettingsStore()
    select_theme(settings_store=store, theme_name="omega-neon")
    assert store.get("theme") == "omega-neon"


def test_select_theme_rejects_unknown_name() -> None:
    store = FakeSettingsStore()
    with pytest.raises(UnknownThemeError):
        select_theme(settings_store=store, theme_name="does-not-exist")
    assert store.get("theme") is None


def test_select_render_profile_persists_value() -> None:
    store = FakeSettingsStore()
    select_render_profile(settings_store=store, render_profile=RenderProfile.MONO)
    assert store.get("render_profile_override") == "mono"


def test_select_render_profile_none_clears_override() -> None:
    store = FakeSettingsStore()
    store.set("render_profile_override", "mono")
    select_render_profile(settings_store=store, render_profile=None)
    assert store.get("render_profile_override") == ""


def test_detect_terminal_resolves_profile() -> None:
    profile = detect_terminal(terminal_detector=FakeTerminalDetector())
    assert isinstance(profile, TerminalProfile)
    assert profile.render_profile == RenderProfile.COMPLETE
