<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT License (see LICENSE file) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-check.png" alt="Omega-Check" width="512">
</div>

#  OMEGA-CHECK

**Port, service and network role scanner (single target)**

> Built by [kraynux](https://github.com/kraynux) for [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Official page: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Preview: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interface and exported reports available in **17 languages** — see [Interface languages](#interface-languages).  
**Languages:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** is a TUI + CLI tool that scans the ports of a single network target, identifies the service running on each open port (protocol, software, version, authentication, WAF, TLS) and infers its probable role, without ever performing an active attack. A tool of the `omega-` suite, structured in Clean Architecture — see `docs/ARCHITECTURE.md` for the full technical details.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-check/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-check/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-check/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-check/D.png" width="24%" />
</p>

## 1. Vision and scope

Omega-check is a port scanner geared toward system administration: quickly check what is listening on a machine (your own, the LAN, or an authorized external target), with what, and how much confidence each piece of information deserves.

### What Omega-check does

- Scans a list of ports (system profile, personal profile, or free input) on a single target.
- Identifies the service running on each open port: protocol (HTTP/HTTPS/SSH/TLS/VNC/generic), software and version when they are exposed, authentication requirement.
- Infers a probable role (web server, shell access, graphical access, database) from the protocol actually negotiated, never from a mere port assumption.
- Detects known WAF signatures (Cloudflare, Sucuri, Akamai, Imperva Incapsula) when they are declared in the headers.
- Presents the result in a TUI (Textual) or a scriptable CLI, and through three exports: JSON, text, HTML (5 themes).
- Gives every collected piece of information an explicit confidence level — see [§7](#7-confidence-policy).
- Keeps a persistent scan history that can be replayed and compared over time.
- Lets you pin targets and create personal port profiles, reusable from one scan to the next.

### What Omega-check does not do

- Active vulnerability scanning: no SQLi, XSS or RCE.
- CVE scanning.
- Operating system fingerprinting (the data model has the field, no heuristic fills it in yet).
- Low-level nmap-style scanning techniques (SYN scan, raw packets) — application-level TCP connection only.
- Brute force or fuzzing tool.
- Parallel multi-target scanning.
- Web dashboard.

## 2. Installation

### Requirements

- Python 3.10+
- Internet connection, for the dependencies

### Installation

```bash
[ -d omega-check ] && echo "ℹ️ Already extracted here, step skipped." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Creates the `.venv` virtual environment if it does not already exist.
2. Installs the dependencies (`pip install -e .`; `pyproject.toml` remains the single source of truth).
3. Makes `omega-check.sh` and `install.sh` executable.
4. Adds the `check` alias to `~/.bashrc` and `~/.zshrc` (no duplicate if already present).

### Dependencies

Declared in `pyproject.toml` (no more `requirements.txt`):
- `omega-lib`: the suite's shared library (`ConfidenceLevel`, themes, terminal detection)
- `textual`: TUI interface, themes, automatic adaptation to the terminal
- `httpx`: HTTP/HTTPS probe
- `cryptography`: reading of the negotiated TLS certificate
- `jinja2`: templating for the HTML export
- Development dependencies (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Usage

### Interactive mode (TUI)

Recommended for everyday use — launched without arguments:

```bash
./omega-check.sh
```
if you created the alias, just type `check` in the terminal:
```bash
check
```

Flow: splash screen (closes on a key press or a click) → main menu (Scan / Targets / Profiles / History / Settings / Help) → target input (with a picker of pinned targets) and profile choice (warning for `complet`, a second field for a personal profile or free port input with `CUSTOM`) → scan (indeterminate gauge and live log of network operations) → scan details (ports/services/roles, export) → history/comparison/replay and settings from the main menu. Adaptation to the terminal (colors, size, structural degradation) is automatic.

#### Keyboard shortcuts

| Key | Action |
|---|---|
| `↑` / `↓` | Move between the items of a screen |
| `Tab` / `Shift+Tab` | Move between the fields of a form |
| `Esc` | Back to the previous screen (exit confirmation on the home screen) |
| `t` | Next theme (applied immediately, no confirmation) |
| `r` | Refresh terminal detection |
| `a` | Show help |
| `q` | Quit (with confirmation) |

### Interface languages

The interface is available in 17 languages: French, English, Spanish, Portuguese (Brazil), Italian, German, Dutch, Polish, Russian, Simplified Chinese, Vietnamese, Thai, Indonesian, Japanese, Korean, Hindi and Arabic. The choice is made in Settings ("Langue / Language") and takes effect after the interface restarts; the `OMEGA_CHECK_LANG` variable (for example `OMEGA_CHECK_LANG=en ./omega-check.sh`) forces a language for one session. When launched from omega-suite, omega-check uses the suite's language. On a Linux text console (TTY), languages with a non-Latin script are shown in English for the session. The command line stays in French.

### Contact and support

Help (`a` key) offers a **Contact and support** screen: *Buy me a coffee* (the developer's PayPal page), *Contact support* (email address and the site's contact form, shown in plain text), *Declare myself as a user (anonymous)* and *Check for updates*. The declaration is voluntary, off by default and sent only once: it is used only to count users and, if you wish, their continent or country (closed lists, never free text). It sends a randomly drawn key, the software name (`omega-check`) and its version; never a name, a machine name, a setting, a target or a result. The IP address is not stored in the declarations, but, like any visit, it goes through the security checks and the log of the receiving server. You can withdraw at any time from the same screen (*Stop declaring me*). The update check only reads the list of versions published on the site, and never without a click.

### Scriptable mode (CLI)

Any subcommand triggers CLI mode:

```bash
# Scan a target with a port profile
./omega-check.sh scan 192.168.1.10 --profile minimal

# History (can be filtered by target)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Scan details (text, JSON or HTML) — choice of 5 export themes
./omega-check.sh show <scan_id> --format html --theme omega-base --output report.html

# Compare two scans (port state changes)
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
http://example.org          HTTP URL  (scheme removed before resolution)
https://example.org:8443    HTTPS URL with port  (scheme and port removed)
```

Any scheme and port are removed before DNS resolution (`domain/targets/validation.py::normalize_target_input`) — pasting a whole URL works, only the host is kept.

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
| `iot` | IoT devices, cameras, routers, home automation | no |
| `dev` | Development/lab environments | no |
| `docker` | Docker, Swarm and common containerized services | no |
| `complet` | **Generated on the fly**: sorted, deduplicated union of all the profiles above | no |
| `CUSTOM` | A personal profile created in the **Profiles** screen, and/or free input (`80` / `22,443,8080` / `1000-2000`) — both add up, deduplicated | no |

Full details, validation rules and management of personal profiles: `docs/PROFILES.md`.

## 5. Architecture

Omega-check is structured in **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), aligned with the `omega-` suite template (see `omega-scan`/`omega-stress`) and verified by `import-linter` on every change. The full details live in **`docs/ARCHITECTURE.md`**.

Very short overview:

```text
src/omega_check/
├── domain/          Pure business logic (scans, targets, services, profiles, reports...)
├── application/     Use cases (commands/queries)
├── ports/           Contracts expected by the application (probers, repositories, exporters...)
├── infrastructure/  Concrete implementations (socket/httpx/cryptography, SQLite; Textual is NOT here)
├── interfaces/      tui/ (Textual) and cli/ (scriptable), with strict feature parity
├── app/             Assembly (DependencyContainer, bootstrap, lifecycle)
├── core/, shared/   Cross-cutting vocabulary, non-business utilities
└── plugins/         Structure in place, empty (no confirmed extension axis)
```

Design rules:
- `domain/services/policies.py`: classifies the clues already collected, never does networking.
- `infrastructure/network/`: does networking (sockets, `httpx`, `cryptography`), never judges.
- `interfaces/`: displays, contains no business logic.
- `infrastructure/exporters/`: read the scan result, recompute nothing.

## 6. Service identification and roles

### Detected protocols

| Protocol | Probe | Collected details |
|---|---|---|
| HTTP / HTTPS | `httpx` | `Server` banner, authentication headers |
| TLS | `cryptography` (negotiated certificate, `CERT_NONE` included) | Version, cipher, certificate subject/issuer |
| SSH | Raw banner | Software and version (e.g. `OpenSSH 10.4`) |
| VNC (RFB) | Security codes announced by the server | Supported authentication types |
| Generic | Raw banner on an unrecognized open port | Careful extraction, no aggressive heuristic |

### Inferred roles

Deduced from the protocol **actually negotiated**, never from a port-number assumption:

| Role | Condition | Confidence |
|---|---|---|
| `web server` | HTTP/HTTPS protocol confirmed | `INFERRED` |
| `shell access` | SSH protocol confirmed | `CORROBORATED` |
| `graphical access` | VNC protocol confirmed | `CORROBORATED` |
| `database` | Port within the range of the `db` system profile | `INFERRED` |

### Known WAF signatures

Detected through a declarative header (`server`, `x-sdk`) — presence **declared by the target**, never independently verified: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (listed for information, not strictly an application WAF).

## 7. Confidence policy

Each collected field carries one of these levels:

| Level | Meaning |
|---|---|
| `VERIFIED` | Protocol fact observed directly, which the target cannot forge (e.g. closed port confirmed by a TCP RST, TLS version actually negotiated). |
| `DECLARED` | Value self-announced by the target in a field it fully controls (e.g. `Server` banner) — plausible but forgeable at will. |
| `CORROBORATED` | A `DECLARED` value confirmed by an independent clue (e.g. SSH role, the protocol having actually been negotiated). |
| `INFERRED` | Deduced from a pattern/heuristic, with no explicit declaration from the target. |
| `UNKNOWN` | No usable clue, or actively hidden by the target. |

## 8. Protection against forged values

Omega-check trusts no data self-declared by the target without flagging it explicitly. A `Server` banner or an `X-Powered-By` header stays `DECLARED`, never `VERIFIED`, however plausible — the target itself provides them and can forge them at will. Only confirmation through an independent channel (the SSH protocol actually negotiated for the "shell access" role, for example) moves a piece of information to `CORROBORATED`. This distinction, carried in `omega-lib` (`ConfidenceLevel`), is structural: no export and no view can hide it.

## 9. Terminal compatibility

The TUI (Textual) automatically detects the terminal's capabilities (emulator, size) and adapts its structural stylesheet accordingly (`complete`/`standard`/`reduced`/`mono`), with no manual flag. CLI mode always stays plain text, independent of the terminal. Policy shared by the whole `omega-` suite (`omega-lib`, `terminal/policies.py`).

### Profile according to the detected emulator

| Emulator | Initial profile |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, modern SSH | `reduced` |
| Linux TTY, legacy SSH | `mono` |
| Unrecognized emulator | `reduced` (default fallback) |

### Profile according to the terminal size

| Minimum size (columns × rows) | Profile ceiling |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| below | `mono` |

The final profile is **the more restrictive of the two** (emulator and size) — a full-screen Ghostty resized to 70 columns drops to `mono`, even though its emulator would allow `complete`. Refreshable live with the `r` key.

## 10. Exports

Text and HTML reports are written in the language chosen in Settings ("Export language", by default the interface language); JSON stays data and is not translated. Reports are generated in `var/exports/` by default (runtime path anchored on the project folder, `$OMEGA_CHECK_VAR_DIR` to override it), or at the given path (`--output` in the CLI, a dialog in the TUI). Explicit, timestamped file name: `scan-{profile}-{date}.ext`, `scan-custom-{date}.ext` for a personal profile, `scan-{date}.ext` for free input without a profile.

### JSON, the source of truth

Full structure of the scan (`Scan` + `Host`), strictly JSON-serializable, confidence levels included.

### Text, compact human-readable report

Readable outside a terminal, without ANSI codes.

### HTML, self-contained web report

5 themes to choose from (`--theme` in the CLI, a selector in the TUI; follows the active interface theme by default when an equivalent exists). Dedicated layout: container, info grid, statistics boxes per port state, colored badges — same visual family as `omega-scan`/`omega-stress`.

## 11. History and comparison

Each scan is persisted (SQLite, `var/db/omega-check.db`): history can be browsed by target, details of a past run, comparison between two scans (port state), and replay of a scan on the same target without re-entering it.

## 12. Tests

```bash
source .venv/bin/activate
lint-imports        # checks the Dependency Rule
pytest -q           # 191 tests
ruff check src tests
mypy -p omega_check
```

Structure: `tests/unit/` (domain and application, without real I/O), `tests/integration/` (real SQLite/files, fake HTTP server `pytest-httpserver`, TLS through `trustme`).

## 13. Out of scope

- CVE scanning
- Active detection of SQLi, XSS, RCE
- Operating system fingerprinting
- Low-level nmap-style scanning techniques (SYN scan, raw packets)
- Crawling
- Fuzzing
- Brute force
- Simultaneous multi-target scanning
- Web dashboard

---

> Omega-check — Scan, identify, qualify, report.
> A port scanner with explicit confidence, not a guess dressed up as fact.
