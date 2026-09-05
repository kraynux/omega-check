<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT License (see LICENSE file) -->
<div align="center">
  <img src="docs/assets/omega-check.png" alt="Omega-Check" width="256">
</div>

#  OMEGA-CHECK

**Single-target network port, service, and role scanner**

> Developed by **kraynux** for **Omega-server**  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Official page: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Preview: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

**Languages:**  
[Français](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-check** is a TUI + CLI tool that scans the ports of a single network target, identifies the service running on each open port (protocol, software, version, authentication, WAF, TLS), and infers its likely role without ever performing an active attack. It is the fourth tool in the `omega-` suite (after `omega-fire`, `omega-stress`, and `omega-scan`), structured according to Clean Architecture; see `docs/ARCHITECTURE.md` for the complete technical details.

## 1. Vision and scope

Omega-check is a system-administration-oriented port scanner: it quickly checks what is listening on a machine (your own, a LAN host, or an authorized external target), which service is behind it, and how much confidence can be placed in each piece of information.

### What Omega-check does

- Scans a port list (system profile, personal profile, or free-form input) on a single target.
- Identifies the service running on each open port: protocol (HTTP/HTTPS/SSH/TLS/VNC/generic), exposed software and version when available, and authentication requirements.
- Infers a likely role (web server, shell access, graphical access, database) from the protocol actually negotiated, never from a simple port-number assumption.
- Detects known WAF signatures (Cloudflare, Sucuri, Akamai, Imperva Incapsula) when declared in headers.
- Presents results in a Textual TUI or scriptable CLI, with three export formats: JSON, text, and HTML (5 themes).
- Assigns every collected item an explicit confidence level; see [§7](#7-confidence-policy).
- Maintains persistent scan history that can be replayed and compared over time.
- Supports pinned targets and personal port profiles reusable from one scan to another.

### What Omega-check does not do

- Active vulnerability scanning; no SQLi, XSS, or RCE.
- CVE scanning.
- Operating-system fingerprinting (the data model includes the field, but no heuristic currently populates it).
- Low-level nmap-style scanning techniques (SYN scans, raw packets): application-level TCP connections only.
- Brute-force or fuzzing.
- Parallel multi-target scanning.
- Web dashboard.

## 2. Installation

### Requirements

- Python 3.10+
- Internet connection for dependencies

### Installation

```bash
[ -d omega-check ] && echo "ℹ️ Already extracted here; skipping step." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Creates the `.venv` virtual environment if it does not already exist.
2. Installs dependencies (`pip install -e .`; `pyproject.toml` remains the single source of truth).
3. Makes `omega-check.sh` and `install.sh` executable.
4. Adds the `check` alias to `~/.bashrc` and `~/.zshrc` without duplicating it.

### Dependencies

Declared in `pyproject.toml` (there is no longer a `requirements.txt`):
- `omega-lib`: shared suite library (`ConfidenceLevel`, themes, terminal detection).
- `textual`: TUI, themes, and automatic terminal adaptation.
- `httpx`: HTTP/HTTPS probing.
- `cryptography`: reading the negotiated TLS certificate.
- `jinja2`: templating for HTML export.
- Development dependencies (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`.

## 3. Usage

### Interactive mode (TUI)

Recommended for daily use; launch without arguments:

```bash
./omega-check.sh
```

If the alias was created, simply type `check` in the terminal:

```bash
check
```

Workflow: start screen (closes on a key press or click) → main menu (Scanner / Targets / Profiles / History / Settings / Help) → enter the target (with a pinned-target picker) and choose a profile (warning for `complet`, a second field for a personal profile, or free-form port input when using `CUSTOM`) → scan (indeterminate progress bar and live network operations) → scan details (ports/services/roles and export) → history, comparison, replay, and settings from the main menu. Terminal adaptation (colors, size, and structural degradation) is automatic.

#### Keyboard shortcuts

| Key | Action |
|---|---|
| `↑` / `↓` | Navigate between screen elements |
| `Tab` / `Shift+Tab` | Navigate between form fields |
| `Esc` | Return to the previous screen (exit confirmation on the home screen) |
| `t` | Next theme (applied immediately, without confirmation) |
| `r` | Refresh terminal detection |
| `a` | Show help |
| `q` | Quit with confirmation |

### Scriptable mode (CLI)

Any subcommand starts CLI mode:

```bash
# Scan a target with a port profile
./omega-check.sh scan 192.168.1.10 --profile minimal

# History (filterable by target)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Scan details (text, JSON, or HTML) — 5 export themes available
./omega-check.sh show <scan_id> --format html --theme omega-base --output report.html

# Compare two scans (port-state changes)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Personal port profiles
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "My profile"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### Accepted target formats

```text
192.168.1.10                IPv4
example.org                 Hostname
http://example.org          HTTP URL (scheme removed before resolution)
https://example.org:8443    HTTPS URL with port (scheme and port removed)
```

Any scheme and port are removed before DNS resolution (`domain/targets/validation.py::normalize_target_input`): pasting a complete URL works; only the host is retained.

## 4. Scan profiles

| Profile | Description | Pinned |
|---|---|---|
| `minimal` | Ultra-fast scan: SSH + HTTP + HTTPS (22, 80, 443) | yes |
| `classic` | Classic Internet/LAN services (37 ports) | yes |
| `web` | Web services and alternatives | no |
| `db` | Databases and data services | no |
| `remote` | Remote access — shell, desktop, RustDesk | no |
| `mail` | Mail services | no |
| `dns` | DNS services | no |
| `iot` | IoT equipment, cameras, gateways, home automation | no |
| `dev` | Development/lab environments | no |
| `docker` | Docker, Swarm, and common container services | no |
| `complet` | **Generated on the fly**: sorted, deduplicated union of all profiles above | no |
| `CUSTOM` | A personal profile created in **Profiles**, and/or free-form input (`80` / `22,443,8080` / `1000-2000`); both are merged and deduplicated | no |

Full details, validation rules, and personal-profile management: `docs/PROFILES.md`.

## 5. Architecture

Omega-check follows **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), aligned with the `omega-` suite template (see `omega-scan`/`omega-stress`) and checked by `import-linter` after every change. Full details are in **`docs/ARCHITECTURE.md`**.

```text
src/omega_check/
├── domain/          Pure business logic (scans, targets, services, profiles, reports...)
├── application/     Use cases (commands/queries)
├── ports/           Contracts expected by the application (probers, repositories, exporters...)
├── infrastructure/  Concrete implementations (socket/httpx/cryptography, SQLite; Textual is NOT here)
├── interfaces/      tui/ (Textual) and cli/ (scriptable), with strict functional parity
├── app/             Assembly (DependencyContainer, bootstrap, lifecycle)
├── core/, shared/   Cross-cutting vocabulary and non-business utilities
└── plugins/         Established, empty structure (no confirmed extension axis)
```

Design rules:
- `domain/services/policies.py`: classifies already-collected evidence and never performs network operations.
- `infrastructure/network/`: performs network operations (sockets, `httpx`, `cryptography`) and never judges.
- `interfaces/`: displays data and contains no business logic.
- `infrastructure/exporters/`: reads scan results and never recalculates them.

## 6. Service identification and roles

### Detected protocols

| Protocol | Probe | Collected detail |
|---|---|---|
| HTTP / HTTPS | `httpx` | `Server` banner, authentication headers |
| TLS | `cryptography` (negotiated certificate, including `CERT_NONE`) | Version, cipher, certificate subject/issuer |
| SSH | Raw banner | Software and version (e.g. `OpenSSH 10.4`) |
| VNC (RFB) | Security codes announced by the server | Supported authentication types |
| Generic | Raw banner on an open, unrecognized port | Cautious extraction, no aggressive heuristics |

### Inferred roles

Roles are inferred from the **actually negotiated protocol**, never from a port-number assumption:

| Role | Condition | Confidence |
|---|---|---|
| `web server` | HTTP/HTTPS protocol confirmed | `INFERRED` |
| `shell access` | SSH protocol confirmed | `CORROBORATED` |
| `graphical access` | VNC protocol confirmed | `CORROBORATED` |
| `database` | Port belongs to the system `db` profile range | `INFERRED` |

### Known WAF signatures

Detected through declarative headers (`server`, `x-sdk`); presence is **declared by the target** and never independently verified: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (listed for reference, not strictly an application WAF).

## 7. Confidence policy

Every collected field carries one of these levels:

| Level | Meaning |
|---|---|
| `VERIFIED` | Directly observed protocol fact that the target cannot falsify (e.g. a closed port confirmed by TCP RST, or the TLS version actually negotiated). |
| `DECLARED` | Value self-announced by the target in a field it fully controls (e.g. `Server` banner); plausible but freely falsifiable. |
| `CORROBORATED` | A `DECLARED` value confirmed by an independent signal (e.g. an SSH role after the protocol was actually negotiated). |
| `INFERRED` | Derived from a pattern or heuristic without an explicit target declaration. |
| `UNKNOWN` | No usable evidence, or the target actively hides it. |

## 8. Protection against falsified values

Omega-check does not trust self-declared target data without clearly indicating that fact. A `Server` banner or `X-Powered-By` header remains `DECLARED`, never `VERIFIED`, regardless of plausibility: the target supplies it and can falsify it at will. Only confirmation through an independent channel (the SSH protocol actually negotiated for the “shell access” role, for example) upgrades information to `CORROBORATED`. This distinction, carried by `omega-lib` (`ConfidenceLevel`), is structural: no export or view can hide it.

## 9. Terminal compatibility

The Textual TUI automatically detects terminal capabilities (emulator and size) and adapts its structural stylesheet (`complete`/`standard`/`reduced`/`mono`), without manual flags. CLI mode always remains plain text and independent of the terminal. The policy is shared by the entire `omega-` suite (`omega-lib`, `terminal/policies.py`).

### Profile by detected emulator

| Emulator | Initial profile |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, modern SSH | `reduced` |
| Linux TTY, legacy SSH | `mono` |
| Unrecognized emulator | `reduced` (default fallback) |

### Profile by terminal size

| Minimum size (columns × rows) | Profile ceiling |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| below | `mono` |

The final profile is **the more restrictive of the two** (emulator and size): a full-screen Ghostty resized to 70 columns falls back to `mono`, even if the emulator itself would allow `complete`. Refreshable live with the `r` key.

## 10. Exports

Reports are generated in `var/exports/` by default (runtime path anchored to the project directory; override with `$OMEGA_CHECK_VAR_DIR`) or at the specified path (`--output` in CLI, dialog in TUI). Explicit timestamped filenames are used: `scan-{profile}-{date}.ext`, `scan-custom-{date}.ext` for a personal profile, and `scan-{date}.ext` for free-form input without a profile.

### JSON, source of truth

Complete scan structure (`Scan` + `Host`), strictly JSON-serializable and including confidence levels.

### Text, compact human report

Readable outside the terminal, without ANSI codes.

### HTML, standalone web report

Five themes available (`--theme` in CLI, selector in TUI; follows the active interface theme by default when an equivalent exists). Dedicated layout with an information grid, port-state statistics, and colored badges, in the same visual family as `omega-scan`/`omega-stress`.

## 11. History and comparison

Every scan is persisted in SQLite (`var/db/omega-check.db`): history searchable by target, previous-run details, comparison between two scans (port states), and replay of a scan against the same target without re-entering it.

## 12. Tests

```bash
source .venv/bin/activate
lint-imports        # verifies the Dependency Rule
pytest -q           # 173 tests
ruff check src tests
mypy -p omega_check
```

Structure: `tests/unit/` (domain and application, no real I/O), `tests/integration/` (SQLite/real files, `pytest-httpserver` fake HTTP server, TLS through `trustme`).

## 13. Out of scope

- CVE scanning.
- Active SQLi, XSS, or RCE detection.
- Operating-system fingerprinting.
- Low-level nmap-style scanning techniques (SYN scans, raw packets).
- Crawling.
- Fuzzing.
- Brute-force.
- Simultaneous multi-target scanning.
- Web dashboard.

---

> Omega-check — Scan, identify, qualify, report.  
> A port scanner with explicit confidence, not an assumption disguised as fact.
