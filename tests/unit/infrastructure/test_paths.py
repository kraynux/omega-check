from pathlib import Path

import pytest

from omega_check.infrastructure.config.paths import (
    ENV_VAR_DIR,
    default_db_path,
    default_exports_dir,
    default_profiles_path,
    default_screenshots_dir,
    default_settings_path,
    resolve_var_dir,
)


def test_resolve_var_dir_defaults_to_cwd_var(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENV_VAR_DIR, raising=False)
    monkeypatch.chdir(tmp_path)
    assert resolve_var_dir() == tmp_path / "var"


def test_resolve_var_dir_honors_env_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    override = tmp_path / "elsewhere"
    monkeypatch.setenv(ENV_VAR_DIR, str(override))
    assert resolve_var_dir() == override


def test_default_db_path_is_under_var_db(tmp_path: Path) -> None:
    path = default_db_path(tmp_path)
    assert path == tmp_path / "db" / "omega-check.db"


def test_default_profiles_path_is_under_var(tmp_path: Path) -> None:
    path = default_profiles_path(tmp_path)
    assert path == tmp_path / "user_profiles.json"


def test_default_settings_path_is_under_var(tmp_path: Path) -> None:
    path = default_settings_path(tmp_path)
    assert path == tmp_path / "settings.json"


def test_default_exports_dir_is_under_var(tmp_path: Path) -> None:
    path = default_exports_dir(tmp_path)
    assert path == tmp_path / "exports"


def test_default_screenshots_dir_is_under_var(tmp_path: Path) -> None:
    path = default_screenshots_dir(tmp_path)
    assert path == tmp_path / "screenshots"
