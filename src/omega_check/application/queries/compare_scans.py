# Copyright (c) 2026 kraynux - Licence MIT
"""Use case : comparer deux scans (recupere les deux agregats, delegue le
diff a domain/reports/comparison.py)."""
from __future__ import annotations

from omega_check.application.queries.get_scan_details import get_scan_details
from omega_check.domain.reports.comparison import ScanComparison, compare_hosts
from omega_check.ports.scan_repository import ScanRepository


def compare_scans(repo: ScanRepository, scan_id_a: str, scan_id_b: str) -> ScanComparison:
    scan_a, host_a = get_scan_details(repo, scan_id_a)
    scan_b, host_b = get_scan_details(repo, scan_id_b)
    return compare_hosts(scan_a, host_a, scan_b, host_b)
