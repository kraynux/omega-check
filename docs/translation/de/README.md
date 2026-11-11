<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT-Lizenz (siehe Datei LICENSE) -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**Scanner für Ports, Dienste und Netzwerkrollen (einzelnes Ziel)**

> Entwickelt von [kraynux](https://github.com/kraynux) für [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Offizielle Seite: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Vorschau: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Oberfläche und exportierte Berichte in **17 Sprachen** verfügbar — siehe [Sprachen der Oberfläche](#sprachen-der-oberfläche).  
**Sprachen:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** ist ein TUI- und CLI-Werkzeug, das die Ports eines einzelnen Netzwerkziels scannt, den Dienst auf jedem offenen Port identifiziert (Protokoll, Software, Version, Authentifizierung, WAF, TLS) und seine wahrscheinliche Rolle ableitet, ohne jemals einen aktiven Angriff auszuführen. Werkzeug der Suite `omega-`, aufgebaut nach Clean Architecture — siehe `docs/ARCHITECTURE.md` für alle technischen Details.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-check/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-check/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-check/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-check/D.png" width="24%" />
</p>

## 1. Vision und Umfang

Omega-check ist ein Port-Scanner für die Systemadministration: schnell prüfen, was auf einer Maschine lauscht (der eigenen, im LAN oder auf einem autorisierten externen Ziel), womit, und mit welchem Vertrauen jede Information als gesichert gelten kann.

### Was Omega-check tut

- Scannt eine Portliste (Systemprofil, persönliches Profil oder freie Eingabe) auf einem einzelnen Ziel.
- Identifiziert den Dienst auf jedem offenen Port: Protokoll (HTTP/HTTPS/SSH/TLS/VNC/generisch), Software und Version, sofern sichtbar, Authentifizierungspflicht.
- Leitet eine wahrscheinliche Rolle ab (Webserver, Shell-Zugang, grafischer Zugang, Datenbank) — aus dem tatsächlich ausgehandelten Protokoll, nie aus einer bloßen Port-Vermutung.
- Erkennt bekannte WAF-Signaturen (Cloudflare, Sucuri, Akamai, Imperva Incapsula), wenn sie in den Headern deklariert sind.
- Zeigt das Ergebnis in der TUI (Textual) oder in der skriptfähigen CLI und über drei Exporte: JSON, Text, HTML (5 Themes).
- Versieht jede gesammelte Information mit einer ausdrücklichen Vertrauensstufe — siehe [§7](#7-vertrauensrichtlinie).
- Führt einen dauerhaften Scan-Verlauf, der wiederholt und über die Zeit verglichen werden kann.
- Erlaubt es, Ziele anzuheften und persönliche Portprofile anzulegen, die von Scan zu Scan wiederverwendbar sind.

### Was Omega-check nicht tut

- Aktives Schwachstellen-Scannen: kein SQLi, XSS oder RCE.
- CVE-Scannen.
- Betriebssystem-Fingerprinting (das Datenmodell sieht das Feld vor, bisher füllt es keine Heuristik).
- Low-Level-Scantechniken im Stil von nmap (SYN-Scan, Rohpakete) — nur TCP-Verbindungen auf Anwendungsebene.
- Brute-Force- oder Fuzzing-Werkzeug.
- Paralleles Scannen mehrerer Ziele.
- Web-Dashboard.

## 2. Installation

### Voraussetzungen

- Python 3.10+
- Internetverbindung, für die Abhängigkeiten

### Installation

```bash
[ -d omega-check ] && echo "ℹ️ Hier bereits entpackt, Schritt übersprungen." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Legt die virtuelle Umgebung `.venv` an, falls sie noch nicht existiert.
2. Installiert die Abhängigkeiten (`pip install -e .`; `pyproject.toml` bleibt die einzige maßgebliche Quelle).
3. Macht `omega-check.sh` und `install.sh` ausführbar.
4. Fügt den Alias `check` zu `~/.bashrc` und `~/.zshrc` hinzu (ohne Duplikat, falls schon vorhanden).

### Abhängigkeiten

Deklariert in `pyproject.toml` (kein `requirements.txt` mehr):
- `omega-lib`: gemeinsame Bibliothek der Suite (`ConfidenceLevel`, Themes, Terminalerkennung)
- `textual`: TUI-Oberfläche, Themes, automatische Anpassung an das Terminal
- `httpx`: HTTP/HTTPS-Sonde
- `cryptography`: Auslesen des ausgehandelten TLS-Zertifikats
- `jinja2`: Templates für den HTML-Export
- Entwicklungsabhängigkeiten (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Verwendung

### Interaktiver Modus (TUI)

Empfohlen für den täglichen Gebrauch — ohne Argumente gestartet:

```bash
./omega-check.sh
```
wenn Sie den Alias angelegt haben, tippen Sie einfach `check` im Terminal:
```bash
check
```

Ablauf: Startbildschirm (schließt sich per Tastendruck oder Klick) → Hauptmenü (Scannen / Ziele / Profile / Verlauf / Einstellungen / Hilfe) → Eingabe des Ziels (mit Auswahl angehefteter Ziele) und Wahl des Profils (Warnung bei `complet`, ein zweites Feld für ein persönliches Profil oder eine freie Porteingabe bei `CUSTOM`) → Scan (unbestimmte Fortschrittsanzeige und Live-Protokoll der Netzwerkvorgänge) → Scan-Details (Ports/Dienste/Rollen, Export) → Verlauf/Vergleich/Wiederholung und Einstellungen über das Hauptmenü. Die Anpassung an das Terminal (Farben, Größe, strukturelle Reduzierung) erfolgt automatisch.

#### Tastenkürzel

| Taste | Aktion |
|---|---|
| `↑` / `↓` | Zwischen den Elementen eines Bildschirms wechseln |
| `Tab` / `Umschalt+Tab` | Zwischen den Feldern eines Formulars wechseln |
| `Esc` | Zurück zum vorherigen Bildschirm (Bestätigung zum Beenden auf dem Startbildschirm) |
| `t` | Nächstes Theme (sofort angewendet, ohne Bestätigung) |
| `r` | Terminalerkennung aktualisieren |
| `a` | Hilfe anzeigen |
| `q` | Beenden (mit Bestätigung) |

### Sprachen der Oberfläche

Die Oberfläche ist in 17 Sprachen verfügbar: Französisch, Englisch, Spanisch, Portugiesisch (Brasilien), Italienisch, Deutsch, Niederländisch, Polnisch, Russisch, vereinfachtes Chinesisch, Vietnamesisch, Thailändisch, Indonesisch, Japanisch, Koreanisch, Hindi und Arabisch. Die Auswahl erfolgt in den Einstellungen („Langue / Language“) und gilt nach einem Neustart der Oberfläche; die Variable `OMEGA_CHECK_LANG` (zum Beispiel `OMEGA_CHECK_LANG=de ./omega-check.sh`) erzwingt eine Sprache für eine Sitzung. Aus omega-suite gestartet, übernimmt omega-check die Sprache der Suite. Auf einer Linux-Textkonsole (TTY) werden Sprachen mit nicht lateinischer Schrift für die Sitzung auf Englisch angezeigt. Die Kommandozeile bleibt auf Französisch.

### Kontakt und Support

Die Hilfe (Taste `a`) bietet einen Bildschirm **Kontakt und Support**: *Einen Kaffee spendieren* (PayPal-Seite des Entwicklers), *Support kontaktieren* (E-Mail-Adresse und Kontaktformular der Website, im Klartext angezeigt), *Mich als Nutzer melden (anonym)* und *Updates prüfen*. Die Meldung ist freiwillig, standardmäßig deaktiviert und wird nur ein einziges Mal gesendet: Sie dient nur dazu, die Nutzer zu zählen und, wenn gewünscht, ihren Kontinent oder ihr Land (geschlossene Listen, nie Freitext). Gesendet werden ein zufällig gezogener Schlüssel, der Name der Software (`omega-check`) und ihre Version; nie ein Name, ein Rechnername, eine Einstellung, ein Ziel oder ein Ergebnis. Die IP-Adresse wird in den Meldungen nicht gespeichert, durchläuft aber wie jeder Besuch die Sicherheitsprüfungen und das Protokoll des Empfangsservers. Rückzug jederzeit über denselben Bildschirm (*Mich nicht mehr melden*). Die Update-Prüfung liest nur die Liste der auf der Website veröffentlichten Versionen, und nie ohne Klick.

### Skriptfähiger Modus (CLI)

Jeder Unterbefehl aktiviert den CLI-Modus:

```bash
# Ein Ziel mit einem Portprofil scannen
./omega-check.sh scan 192.168.1.10 --profile minimal

# Verlauf (nach Ziel filterbar)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Details eines Scans (Text, JSON oder HTML) — 5 Export-Themes zur Auswahl
./omega-check.sh show <scan_id> --format html --theme omega-base --output bericht.html

# Zwei Scans vergleichen (Änderungen des Portzustands)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Persönliche Portprofile
./omega-check.sh profile list
./omega-check.sh profile create labor --ports 22,80,443 --description "Mein Profil"
./omega-check.sh profile edit labor --ports 22,80,443,8080
./omega-check.sh profile pin labor
./omega-check.sh profile unpin labor
./omega-check.sh profile delete labor
```

### Akzeptierte Zielformate

```text
192.168.1.10                IPv4
example.org                 Hostname
http://example.org          HTTP-URL  (Schema vor der Auflösung entfernt)
https://example.org:8443    HTTPS-URL mit Port  (Schema und Port entfernt)
```

Schema und gegebenenfalls Port werden vor der DNS-Auflösung entfernt (`domain/targets/validation.py::normalize_target_input`) — eine komplette URL einzufügen funktioniert, nur der Host bleibt erhalten.

## 4. Scan-Profile

| Profil | Beschreibung | Angeheftet |
|---|---|---|
| `minimal` | Ultraschneller Scan: SSH + HTTP + HTTPS (22, 80, 443) | ja |
| `classic` | Klassische Internet-/LAN-Dienste (37 Ports) | ja |
| `web` | Webdienste und Alternativen | nein |
| `db` | Datenbanken und Datendienste | nein |
| `remote` | Fernzugriffe — Shell, Desktop, RustDesk | nein |
| `mail` | Maildienste | nein |
| `dns` | DNS-Dienste | nein |
| `iot` | IoT-Geräte, Kameras, Router, Hausautomation | nein |
| `dev` | Entwicklungs-/Laborumgebungen | nein |
| `docker` | Docker, Swarm und übliche Dienste in Containern | nein |
| `complet` | **Spontan erzeugt**: sortierte, duplikatfreie Vereinigung aller obigen Profile | nein |
| `CUSTOM` | Ein im Bildschirm **Profile** angelegtes persönliches Profil und/oder eine freie Eingabe (`80` / `22,443,8080` / `1000-2000`) — beides addiert sich, ohne Duplikate | nein |

Vollständige Details, Validierungsregeln und Verwaltung der persönlichen Profile: `docs/PROFILES.md`.

## 5. Architektur

Omega-check ist nach **Clean Architecture** aufgebaut (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), angelehnt an die Vorlage der Suite `omega-` (siehe `omega-scan`/`omega-stress`) und bei jeder Änderung durch `import-linter` geprüft. Alle Details stehen in **`docs/ARCHITECTURE.md`**.

Sehr kurzer Überblick:

```text
src/omega_check/
├── domain/          Reine Fachlogik (Scans, Ziele, Dienste, Profile, Berichte...)
├── application/     Anwendungsfälle (commands/queries)
├── ports/           Von der Anwendung erwartete Verträge (Sonden, Repositories, Exporter...)
├── infrastructure/  Konkrete Implementierungen (socket/httpx/cryptography, SQLite; Textual ist NICHT hier)
├── interfaces/      tui/ (Textual) und cli/ (skriptfähig), mit strikter Funktionsgleichheit
├── app/             Zusammenbau (DependencyContainer, Bootstrap, Lebenszyklus)
├── core/, shared/   Übergreifendes Vokabular, fachfremde Hilfsmittel
└── plugins/         Struktur angelegt, leer (keine bestätigte Erweiterungsachse)
```

Entwurfsregeln:
- `domain/services/policies.py`: klassifiziert die bereits gesammelten Hinweise, greift nie aufs Netzwerk zu.
- `infrastructure/network/`: greift aufs Netzwerk zu (Sockets, `httpx`, `cryptography`), bewertet nie.
- `interfaces/`: zeigt an, enthält keine Fachlogik.
- `infrastructure/exporters/`: lesen das Scan-Ergebnis, berechnen nichts neu.

## 6. Dienstidentifikation und Rollen

### Erkannte Protokolle

| Protokoll | Sonde | Gesammelte Details |
|---|---|---|
| HTTP / HTTPS | `httpx` | `Server`-Banner, Authentifizierungs-Header |
| TLS | `cryptography` (ausgehandeltes Zertifikat, `CERT_NONE` eingeschlossen) | Version, Cipher, Subjekt/Aussteller des Zertifikats |
| SSH | Rohes Banner | Software und Version (z. B. `OpenSSH 10.4`) |
| VNC (RFB) | Vom Server angekündigte Sicherheitscodes | Unterstützte Authentifizierungsarten |
| Generisch | Rohes Banner auf einem nicht erkannten offenen Port | Vorsichtige Extraktion, keine aggressive Heuristik |

### Abgeleitete Rollen

Abgeleitet aus dem **tatsächlich ausgehandelten** Protokoll, nie aus einer Vermutung anhand der Portnummer:

| Rolle | Bedingung | Vertrauen |
|---|---|---|
| `Webserver` | HTTP/HTTPS-Protokoll bestätigt | `INFERRED` |
| `Shell-Zugang` | SSH-Protokoll bestätigt | `CORROBORATED` |
| `grafischer Zugang` | VNC-Protokoll bestätigt | `CORROBORATED` |
| `Datenbank` | Port im Bereich des Systemprofils `db` | `INFERRED` |

### Bekannte WAF-Signaturen

Erkannt über einen deklarativen Header (`server`, `x-sdk`) — Präsenz **vom Ziel deklariert**, nie unabhängig überprüft: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (zur Information aufgeführt, streng genommen keine Anwendungs-WAF).

## 7. Vertrauensrichtlinie

Jedes gesammelte Feld trägt eine dieser Stufen:

| Stufe | Bedeutung |
|---|---|
| `VERIFIED` | Direkt beobachtete Protokolltatsache, die das Ziel nicht fälschen kann (z. B. geschlossener Port, durch TCP-RST bestätigt, tatsächlich ausgehandelte TLS-Version). |
| `DECLARED` | Vom Ziel selbst angekündigter Wert in einem Feld, das es vollständig kontrolliert (z. B. `Server`-Banner) — plausibel, aber beliebig fälschbar. |
| `CORROBORATED` | Ein `DECLARED`-Wert, der durch einen unabhängigen Hinweis bestätigt wird (z. B. SSH-Rolle, da das Protokoll tatsächlich ausgehandelt wurde). |
| `INFERRED` | Aus einem Muster/einer Heuristik abgeleitet, ohne ausdrückliche Angabe des Ziels. |
| `UNKNOWN` | Kein verwertbarer Hinweis oder vom Ziel aktiv verborgen. |

## 8. Schutz vor gefälschten Werten

Omega-check vertraut keinen vom Ziel selbst deklarierten Daten, ohne dies ausdrücklich zu kennzeichnen. Ein `Server`-Banner oder ein `X-Powered-By`-Header bleibt `DECLARED`, nie `VERIFIED`, so plausibel er auch sein mag — das Ziel selbst liefert sie und kann sie beliebig fälschen. Nur eine Bestätigung über einen unabhängigen Kanal (etwa das tatsächlich ausgehandelte SSH-Protokoll für die Rolle „Shell-Zugang“) hebt eine Information auf `CORROBORATED`. Diese Unterscheidung, getragen von `omega-lib` (`ConfidenceLevel`), ist strukturell: Kein Export und keine Ansicht kann sie verbergen.

## 9. Terminal-Kompatibilität

Die TUI (Textual) erkennt automatisch die Fähigkeiten des Terminals (Emulator, Größe) und passt ihr strukturelles Stylesheet entsprechend an (`complete`/`standard`/`reduced`/`mono`), ohne manuelle Option. Der CLI-Modus bleibt immer einfacher Text, unabhängig vom Terminal. Richtlinie der gesamten Suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Profil nach erkanntem Emulator

| Emulator | Anfangsprofil |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, modernes SSH | `reduced` |
| Linux-TTY, älteres SSH | `mono` |
| Nicht erkannter Emulator | `reduced` (Standard-Rückfall) |

### Profil nach Terminalgröße

| Mindestgröße (Spalten × Zeilen) | Profil-Obergrenze |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| darunter | `mono` |

Das endgültige Profil ist **das strengere der beiden** (Emulator und Größe) — ein Ghostty im Vollbild, auf 70 Spalten verkleinert, fällt auf `mono` zurück, obwohl sein Emulator `complete` erlauben würde. Live aktualisierbar mit der Taste `r`.

## 10. Exporte

Text- und HTML-Berichte werden in der in den Einstellungen gewählten Sprache geschrieben („Sprache der Exporte“, standardmäßig die der Oberfläche); JSON bleibt Daten und wird nicht übersetzt. Die Berichte werden standardmäßig in `var/exports/` erzeugt (Laufzeitpfad im Projektordner verankert, mit `$OMEGA_CHECK_VAR_DIR` überschreibbar) oder unter dem angegebenen Pfad (`--output` in der CLI, Dialog in der TUI). Eindeutiger Dateiname mit Zeitstempel: `scan-{profil}-{datum}.ext`, `scan-custom-{datum}.ext` für ein persönliches Profil, `scan-{datum}.ext` für eine freie Eingabe ohne Profil.

### JSON, die maßgebliche Quelle

Vollständige Struktur des Scans (`Scan` + `Host`), streng JSON-serialisierbar, Vertrauensstufen eingeschlossen.

### Text, kompakter lesbarer Bericht

Außerhalb des Terminals lesbar, ohne ANSI-Codes.

### HTML, eigenständiger Webbericht

5 Themes zur Auswahl (`--theme` in der CLI, Auswahlfeld in der TUI; folgt standardmäßig dem aktiven Oberflächen-Theme, wenn es eine Entsprechung gibt). Eigenes Layout: Container, Informationsraster, Statistikkästen pro Portzustand, farbige Abzeichen — dieselbe visuelle Familie wie `omega-scan`/`omega-stress`.

## 11. Verlauf und Vergleich

Jeder Scan wird gespeichert (SQLite, `var/db/omega-check.db`): Verlauf nach Ziel einsehbar, Details eines früheren Laufs, Vergleich zweier Scans (Portzustand) und Wiederholung eines Scans auf demselben Ziel ohne erneute Eingabe.

## 12. Tests

```bash
source .venv/bin/activate
lint-imports        # prüft die Dependency Rule
pytest -q           # 191 Tests
ruff check src tests
mypy -p omega_check
```

Struktur: `tests/unit/` (Domain und Anwendung, ohne echte E/A), `tests/integration/` (echte SQLite-Datenbank/Dateien, simulierter HTTP-Server `pytest-httpserver`, TLS über `trustme`).

## 13. Außerhalb des Umfangs

- CVE-Scannen
- Aktive Erkennung von SQLi, XSS, RCE
- Betriebssystem-Fingerprinting
- Low-Level-Scantechniken im Stil von nmap (SYN-Scan, Rohpakete)
- Crawling
- Fuzzing
- Brute Force
- Gleichzeitiges Scannen mehrerer Ziele
- Web-Dashboard

---

> Omega-check — Scannen, identifizieren, einstufen, berichten.
> Ein Port-Scanner mit ausdrücklichem Vertrauen, keine als Tatsache verkleidete Vermutung.
