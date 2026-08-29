from collections.abc import Iterator
from pathlib import Path

import pytest

from omega_check.app.bootstrap import bootstrap
from omega_check.app.dependency_container import DependencyContainer
from omega_check.interfaces.cli.main import run


@pytest.fixture
def container(tmp_path: Path) -> Iterator[DependencyContainer]:
    c = bootstrap(var_dir=tmp_path)
    yield c
    c.close()


def _run(container: DependencyContainer, argv: list[str], capsys: pytest.CaptureFixture[str]) -> str:
    code = run(container, argv)
    assert code == 0
    return capsys.readouterr().out.strip()


def test_scan_then_history_then_show(container: DependencyContainer, capsys: pytest.CaptureFixture[str]) -> None:
    _run(container, ["scan", "127.0.0.1", "--profile", "minimal"], capsys)

    history_output = _run(container, ["history"], capsys)
    assert "127.0.0.1" in history_output
    scan_id = history_output.split()[0]

    text_output = _run(container, ["show", scan_id], capsys)
    assert scan_id in text_output

    json_output = _run(container, ["show", scan_id, "--format", "json"], capsys)
    assert '"target": "127.0.0.1"' in json_output

    html_output = _run(container, ["show", scan_id, "--format", "html"], capsys)
    assert "<table>" in html_output


def test_show_writes_to_output_file(
    container: DependencyContainer, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _run(container, ["scan", "127.0.0.1", "--profile", "minimal"], capsys)
    scan_id = _run(container, ["history"], capsys).split()[0]

    output_file = tmp_path / "report.html"
    result = _run(container, ["show", scan_id, "--format", "html", "--output", str(output_file)], capsys)

    assert str(output_file) in result
    assert output_file.exists()
    assert "<table>" in output_file.read_text(encoding="utf-8")


def test_history_empty_when_no_scans(container: DependencyContainer, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run(container, ["history"], capsys) == "Aucun scan enregistre."


def test_compare_two_scans(container: DependencyContainer, capsys: pytest.CaptureFixture[str]) -> None:
    _run(container, ["scan", "127.0.0.1", "--profile", "minimal"], capsys)
    _run(container, ["scan", "127.0.0.1", "--profile", "minimal"], capsys)
    history = _run(container, ["history"], capsys).splitlines()
    scan_id_newest, scan_id_oldest = history[0].split()[0], history[-1].split()[0]

    output = _run(container, ["compare", scan_id_oldest, scan_id_newest], capsys)
    assert "Comparaison" in output


def test_compare_reports_differences(container: DependencyContainer, capsys: pytest.CaptureFixture[str]) -> None:
    _run(container, ["profile", "create", "p1", "--ports", "80"], capsys)
    _run(container, ["scan", "127.0.0.1", "--profile", "p1"], capsys)
    _run(container, ["profile", "edit", "p1", "--ports", "80,81"], capsys)
    _run(container, ["scan", "127.0.0.1", "--profile", "p1"], capsys)

    history = _run(container, ["history"], capsys).splitlines()
    scan_id_newest, scan_id_oldest = history[0].split()[0], history[-1].split()[0]

    output = _run(container, ["compare", scan_id_oldest, scan_id_newest], capsys)
    assert "seulement dans" in output
    assert "81" in output


def test_command_error_is_reported_and_exits_non_zero(
    container: DependencyContainer, capsys: pytest.CaptureFixture[str]
) -> None:
    code = run(container, ["show", "inexistant"])
    assert code == 1
    assert "erreur" in capsys.readouterr().err


def test_profile_edit_pin_unpin(container: DependencyContainer, capsys: pytest.CaptureFixture[str]) -> None:
    _run(container, ["profile", "create", "labo", "--ports", "22"], capsys)

    edit_output = _run(container, ["profile", "edit", "labo", "--ports", "22,80", "--description", "maj"], capsys)
    assert "mis a jour" in edit_output

    def _labo_line(list_output: str) -> str:
        return next(line for line in list_output.splitlines() if line.startswith("labo"))

    pin_output = _run(container, ["profile", "pin", "labo"], capsys)
    assert "epingle" in pin_output
    assert "(pinned)" in _labo_line(_run(container, ["profile", "list"], capsys))

    unpin_output = _run(container, ["profile", "unpin", "labo"], capsys)
    assert "desepingle" in unpin_output
    assert "(pinned)" not in _labo_line(_run(container, ["profile", "list"], capsys))


def test_profile_create_list_delete(container: DependencyContainer, capsys: pytest.CaptureFixture[str]) -> None:
    create_output = _run(
        container, ["profile", "create", "labo", "--ports", "22,8080", "--description", "test"], capsys
    )
    assert "labo" in create_output

    list_output = _run(container, ["profile", "list"], capsys)
    assert "labo" in list_output
    assert "minimal" in list_output  # profil systeme toujours present

    delete_output = _run(container, ["profile", "delete", "labo"], capsys)
    assert "supprime" in delete_output

    list_after_delete = _run(container, ["profile", "list"], capsys)
    assert "labo" not in list_after_delete
