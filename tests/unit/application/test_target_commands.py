from datetime import UTC, datetime

from omega_check.application.commands.clear_all_targets import clear_all_targets
from omega_check.application.commands.pin_target import pin_target
from omega_check.application.commands.unpin_target import unpin_target
from omega_check.application.queries.list_targets import list_targets
from omega_check.domain.targets.models import PinnedTarget


class FakeTargetRepository:
    """Implemente structurellement ports/target_repository.py::TargetRepository
    (Protocol) — double en memoire, voir
    infrastructure/storage/sqlite/target_repository.py pour l'implementation
    de production, testee separement."""

    def __init__(self) -> None:
        self._targets: dict[str, PinnedTarget] = {}

    def pin(self, pinned: PinnedTarget) -> None:
        self._targets[pinned.host] = pinned

    def unpin(self, host: str) -> None:
        self._targets.pop(host, None)

    def get(self, host: str) -> PinnedTarget | None:
        return self._targets.get(host)

    def list_pinned(self) -> tuple[PinnedTarget, ...]:
        return tuple(self._targets.values())

    def clear(self) -> None:
        self._targets.clear()


def _fixed_now() -> datetime:
    return datetime(2026, 8, 29, 12, 0, 0, tzinfo=UTC)


def test_pin_target_normalizes_and_stores() -> None:
    repo = FakeTargetRepository()

    pinned = pin_target(target_repository=repo, now=_fixed_now, raw_input="http://exemple.org:8080/x")

    assert pinned.host == "exemple.org"
    assert repo.get("exemple.org") == pinned


def test_pin_target_stores_the_optional_note() -> None:
    repo = FakeTargetRepository()

    pinned = pin_target(target_repository=repo, now=_fixed_now, raw_input="10.0.0.1", note="serveur test")

    assert pinned.note == "serveur test"


def test_unpin_target_removes_it() -> None:
    repo = FakeTargetRepository()
    pin_target(target_repository=repo, now=_fixed_now, raw_input="10.0.0.1")

    unpin_target(target_repository=repo, host="10.0.0.1")

    assert repo.get("10.0.0.1") is None


def test_list_targets_returns_all_pinned() -> None:
    repo = FakeTargetRepository()
    pin_target(target_repository=repo, now=_fixed_now, raw_input="10.0.0.1")
    pin_target(target_repository=repo, now=_fixed_now, raw_input="10.0.0.2")

    hosts = {t.host for t in list_targets(target_repository=repo)}
    assert hosts == {"10.0.0.1", "10.0.0.2"}


def test_clear_all_targets_empties_the_repository() -> None:
    repo = FakeTargetRepository()
    pin_target(target_repository=repo, now=_fixed_now, raw_input="10.0.0.1")

    clear_all_targets(target_repository=repo)

    assert list_targets(target_repository=repo) == ()
