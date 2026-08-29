import pytest

from omega_check.domain.targets.validation import normalize_target_input


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("127.0.0.1", "127.0.0.1"),
        ("example.org", "example.org"),
        ("http://example.org", "example.org"),
        ("https://example.org", "example.org"),
        ("http://example.org:8080", "example.org"),
        ("http://example.org:8080/chemin", "example.org"),
        ("  http://example.org  ", "example.org"),
        ("HTTP://Example.org", "Example.org"),
        ("example.org/chemin", "example.org"),
    ],
)
def test_normalize_target_input(raw: str, expected: str) -> None:
    assert normalize_target_input(raw) == expected


def test_normalize_target_input_is_idempotent() -> None:
    once = normalize_target_input("http://example.org:8080/x")
    twice = normalize_target_input(once)
    assert once == twice
