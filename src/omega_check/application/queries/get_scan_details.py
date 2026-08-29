# Copyright (c) 2026 kraynux - Licence MIT
"""Use case : recuperer un scan detaille (Scan + Host, sans recalcul —
voir OMEGA-CHECK_SPECIFICATIONS.md §6.2)."""
from __future__ import annotations

from omega_check.domain.scans.exceptions import ScanNotFoundError
from omega_check.domain.scans.models import Scan
from omega_check.domain.targets.models import Host
from omega_check.ports.scan_repository import ScanRepository


def get_scan_details(repo: ScanRepository, scan_id: str) -> tuple[Scan, Host | None]:
    scan = repo.get(scan_id)
    if scan is None:
        raise ScanNotFoundError(scan_id)
    return scan, repo.get_host(scan_id)
