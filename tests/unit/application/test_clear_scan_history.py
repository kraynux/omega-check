from omega_check.application.commands.clear_scan_history import clear_scan_history
from omega_check.domain.scans.models import Scan


class FakeScanRepository:
    def __init__(self) -> None:
        self.cleared = False

    def save(self, scan: Scan) -> None: ...

    def get(self, scan_id: str) -> Scan | None:
        return None

    def list_history(self, *, target: str | None = None, limit: int = 50) -> tuple[Scan, ...]:
        return ()

    def save_host(self, scan_id: str, host: object) -> None: ...

    def get_host(self, scan_id: str) -> None:
        return None

    def clear(self) -> None:
        self.cleared = True


def test_clear_scan_history_delegates_to_repository() -> None:
    repo = FakeScanRepository()
    clear_scan_history(scan_repository=repo)
    assert repo.cleared is True
