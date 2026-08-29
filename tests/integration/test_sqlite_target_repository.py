from collections.abc import Iterator
from pathlib import Path

import pytest

from omega_check.domain.targets.models import PinnedTarget
from omega_check.infrastructure.storage.sqlite.connection import open_connection
from omega_check.infrastructure.storage.sqlite.target_repository import SqliteTargetRepository


@pytest.fixture
def repo(tmp_path: Path) -> Iterator[SqliteTargetRepository]:
    connection = open_connection(tmp_path / "omega-check.db")
    try:
        yield SqliteTargetRepository(connection)
    finally:
        connection.close()


def test_pin_and_get_round_trips(repo: SqliteTargetRepository) -> None:
    pinned = PinnedTarget(host="192.168.1.10", pinned_at="2026-08-29T00:00:00+00:00", note="serveur test")
    repo.pin(pinned)

    assert repo.get("192.168.1.10") == pinned


def test_get_unknown_host_returns_none(repo: SqliteTargetRepository) -> None:
    assert repo.get("absent.example.org") is None


def test_re_pinning_same_host_overwrites(repo: SqliteTargetRepository) -> None:
    repo.pin(PinnedTarget(host="10.0.0.1", pinned_at="2026-08-29T00:00:00+00:00", note="premiere note"))
    repo.pin(PinnedTarget(host="10.0.0.1", pinned_at="2026-08-29T01:00:00+00:00", note="note mise a jour"))

    assert len(repo.list_pinned()) == 1
    assert repo.get("10.0.0.1").note == "note mise a jour"  # type: ignore[union-attr]


def test_unpin_removes_the_target(repo: SqliteTargetRepository) -> None:
    repo.pin(PinnedTarget(host="10.0.0.2", pinned_at="2026-08-29T00:00:00+00:00"))
    repo.unpin("10.0.0.2")

    assert repo.get("10.0.0.2") is None


def test_unpin_unknown_host_is_a_no_op(repo: SqliteTargetRepository) -> None:
    repo.unpin("absent.example.org")  # ne leve pas


def test_list_pinned_returns_all(repo: SqliteTargetRepository) -> None:
    repo.pin(PinnedTarget(host="10.0.0.1", pinned_at="2026-08-29T00:00:00+00:00"))
    repo.pin(PinnedTarget(host="10.0.0.2", pinned_at="2026-08-29T01:00:00+00:00"))

    hosts = {target.host for target in repo.list_pinned()}
    assert hosts == {"10.0.0.1", "10.0.0.2"}


def test_clear_removes_everything(repo: SqliteTargetRepository) -> None:
    repo.pin(PinnedTarget(host="10.0.0.1", pinned_at="2026-08-29T00:00:00+00:00"))
    repo.clear()

    assert repo.list_pinned() == ()
