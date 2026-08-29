from pathlib import Path

from omega_check.infrastructure.storage.files.json_settings_store import JsonSettingsStore


def test_get_returns_default_when_file_missing(tmp_path: Path) -> None:
    store = JsonSettingsStore(tmp_path / "settings.json")
    assert store.get("theme", "fallback") == "fallback"


def test_set_then_get_round_trips(tmp_path: Path) -> None:
    store = JsonSettingsStore(tmp_path / "sub" / "settings.json")
    store.set("theme", "omega-neon")
    assert store.get("theme") == "omega-neon"


def test_set_creates_parent_directories(tmp_path: Path) -> None:
    target = tmp_path / "does" / "not" / "exist" / "settings.json"
    store = JsonSettingsStore(target)
    store.set("k", "v")
    assert target.exists()


def test_all_returns_full_dict(tmp_path: Path) -> None:
    store = JsonSettingsStore(tmp_path / "settings.json")
    store.set("theme", "omega-dark")
    store.set("render_profile_override", "mono")
    assert store.all() == {"theme": "omega-dark", "render_profile_override": "mono"}
