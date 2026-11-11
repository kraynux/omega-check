<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT-licentie (zie het bestand LICENSE) -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**Scanner van poorten, diensten en netwerkrollen (één doel)**

> Gemaakt door [kraynux](https://github.com/kraynux) voor [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Officiële pagina: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Voorbeeld: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interface en geëxporteerde rapporten beschikbaar in **17 talen** — zie [Talen van de interface](#talen-van-de-interface).  
**Talen:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** is een TUI- en CLI-tool die de poorten van één netwerkdoel scant, de dienst op elke open poort identificeert (protocol, software, versie, authenticatie, WAF, TLS) en de waarschijnlijke rol afleidt, zonder ooit een actieve aanval uit te voeren. Tool van de suite `omega-`, opgebouwd volgens Clean Architecture — zie `docs/ARCHITECTURE.md` voor alle technische details.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-check/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-check/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-check/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-check/D.png" width="24%" />
</p>

## 1. Visie en reikwijdte

Omega-check is een poortscanner voor systeembeheer: snel nagaan wat er op een machine luistert (de eigen machine, het LAN of een toegestaan extern doel), waarmee, en met hoeveel vertrouwen elk gegeven als vaststaand mag gelden.

### Wat Omega-check doet

- Scant een lijst poorten (systeemprofiel, persoonlijk profiel of vrije invoer) op één doel.
- Identificeert de dienst op elke open poort: protocol (HTTP/HTTPS/SSH/TLS/VNC/generiek), software en versie als die zichtbaar zijn, authenticatievereiste.
- Leidt een waarschijnlijke rol af (webserver, shelltoegang, grafische toegang, database) uit het werkelijk onderhandelde protocol, nooit uit een simpele aanname op basis van de poort.
- Herkent bekende WAF-handtekeningen (Cloudflare, Sucuri, Akamai, Imperva Incapsula) wanneer ze in de headers worden gedeclareerd.
- Toont het resultaat in de TUI (Textual) of in een scriptbare CLI, en via drie exports: JSON, tekst, HTML (5 thema's).
- Geeft elk verzameld gegeven een expliciet vertrouwensniveau — zie [§7](#7-vertrouwensbeleid).
- Bewaart een blijvende geschiedenis van scans, opnieuw uit te voeren en in de tijd te vergelijken.
- Laat doelen vastpinnen en persoonlijke poortprofielen aanmaken, herbruikbaar van scan tot scan.

### Wat Omega-check niet doet

- Actief scannen op kwetsbaarheden: geen SQLi, XSS of RCE.
- CVE-scans.
- Herkenning van het besturingssysteem (het datamodel voorziet het veld, nog geen enkele heuristiek vult het in).
- Low-level scantechnieken in nmap-stijl (SYN-scan, ruwe pakketten) — alleen TCP-verbindingen op applicatieniveau.
- Brute-force- of fuzzingtool.
- Parallel scannen van meerdere doelen.
- Webdashboard.

## 2. Installatie

### Vereisten

- Python 3.10+
- Internetverbinding, voor de afhankelijkheden

### Installatie

```bash
[ -d omega-check ] && echo "ℹ️ Hier al uitgepakt, stap overgeslagen." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Maakt de virtuele omgeving `.venv` aan als die nog niet bestaat.
2. Installeert de afhankelijkheden (`pip install -e .`; `pyproject.toml` blijft de enige bron van waarheid).
3. Maakt `omega-check.sh` en `install.sh` uitvoerbaar.
4. Voegt de alias `check` toe aan `~/.bashrc` en `~/.zshrc` (zonder dubbel als hij er al staat).

### Afhankelijkheden

Gedeclareerd in `pyproject.toml` (geen `requirements.txt` meer):
- `omega-lib`: gedeelde bibliotheek van de suite (`ConfidenceLevel`, thema's, terminaldetectie)
- `textual`: TUI-interface, thema's, automatische aanpassing aan de terminal
- `httpx`: HTTP/HTTPS-sonde
- `cryptography`: uitlezen van het onderhandelde TLS-certificaat
- `jinja2`: templates voor de HTML-export
- Ontwikkelafhankelijkheden (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Gebruik

### Interactieve modus (TUI)

Aanbevolen voor dagelijks gebruik — gestart zonder argumenten:

```bash
./omega-check.sh
```
als u de alias hebt aangemaakt, typ dan gewoon `check` in de terminal:
```bash
check
```

Verloop: startscherm (sluit met een toets of een klik) → hoofdmenu (Scannen / Doelen / Profielen / Geschiedenis / Instellingen / Help) → invoer van het doel (met keuzelijst van vastgepinde doelen) en keuze van het profiel (waarschuwing bij `complet`, een tweede veld voor een persoonlijk profiel of een vrije poortinvoer bij `CUSTOM`) → scan (onbepaalde voortgangsbalk en live verslag van de netwerkbewerkingen) → details van de scan (poorten/diensten/rollen, export) → geschiedenis/vergelijking/opnieuw uitvoeren en instellingen vanuit het hoofdmenu. De aanpassing aan de terminal (kleuren, grootte, structurele vereenvoudiging) gebeurt automatisch.

#### Sneltoetsen

| Toets | Actie |
|---|---|
| `↑` / `↓` | Tussen de elementen van een scherm bewegen |
| `Tab` / `Shift+Tab` | Tussen de velden van een formulier bewegen |
| `Esc` | Terug naar het vorige scherm (bevestiging om af te sluiten op het startscherm) |
| `t` | Volgend thema (direct toegepast, zonder bevestiging) |
| `r` | Terminaldetectie vernieuwen |
| `a` | Help tonen |
| `q` | Afsluiten (met bevestiging) |

### Talen van de interface

De interface is beschikbaar in 17 talen: Frans, Engels, Spaans, Portugees (Brazilië), Italiaans, Duits, Nederlands, Pools, Russisch, vereenvoudigd Chinees, Vietnamees, Thai, Indonesisch, Japans, Koreaans, Hindi en Arabisch. De keuze gebeurt in de Instellingen („Langue / Language”) en geldt na een herstart van de interface; de variabele `OMEGA_CHECK_LANG` (bijvoorbeeld `OMEGA_CHECK_LANG=nl ./omega-check.sh`) legt voor één sessie een taal op. Gestart vanuit omega-suite neemt omega-check de taal van de suite over. Op een Linux-tekstconsole (TTY) worden talen met een niet-Latijns schrift voor die sessie in het Engels getoond. De opdrachtregel blijft in het Frans.

### Contact en ondersteuning

De hulp (toets `a`) biedt een scherm **Contact en ondersteuning**: *Trakteer op een koffie* (PayPal-pagina van de ontwikkelaar), *Contact opnemen met ondersteuning* (e-mailadres en contactformulier van de site, leesbaar weergegeven), *Mij aanmelden als gebruiker (anoniem)* en *Updates controleren*. De aanmelding is vrijwillig, standaard uitgeschakeld en wordt maar één keer verzonden: ze dient alleen om de gebruikers te tellen en, als u dat wilt, hun continent of land (gesloten lijsten, nooit vrije tekst). Ze verzendt een willekeurig gekozen sleutel, de naam van de software (`omega-check`) en de versie; nooit een naam, een machinenaam, een instelling, een doel of een resultaat. Het IP-adres wordt niet opgeslagen in de aanmeldingen, maar gaat, zoals bij elk bezoek, door de beveiligingscontroles en het logboek van de ontvangende server. Intrekken kan op elk moment vanuit hetzelfde scherm (*Mij niet meer aanmelden*). De updatecontrole leest alleen de lijst van versies die op de site gepubliceerd zijn, en nooit zonder klik.

### Scriptbare modus (CLI)

Elke subopdracht activeert de CLI-modus:

```bash
# Een doel scannen met een poortprofiel
./omega-check.sh scan 192.168.1.10 --profile minimal

# Geschiedenis (te filteren op doel)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Details van een scan (tekst, JSON of HTML) — keuze uit 5 exportthema's
./omega-check.sh show <scan_id> --format html --theme omega-base --output rapport.html

# Twee scans vergelijken (wijzigingen in poortstatus)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Persoonlijke poortprofielen
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "Mijn profiel"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### Geaccepteerde doelformaten

```text
192.168.1.10                IPv4
example.org                 Hostnaam
http://example.org          HTTP-URL  (schema verwijderd vóór de resolutie)
https://example.org:8443    HTTPS-URL met poort  (schema en poort verwijderd)
```

Het schema en een eventuele poort worden vóór de DNS-resolutie verwijderd (`domain/targets/validation.py::normalize_target_input`) — een volledige URL plakken werkt, alleen de host blijft over.

## 4. Scanprofielen

| Profiel | Beschrijving | Vastgepind |
|---|---|---|
| `minimal` | Supersnelle scan: SSH + HTTP + HTTPS (22, 80, 443) | ja |
| `classic` | Klassieke internet-/LAN-diensten (37 poorten) | ja |
| `web` | Webdiensten en alternatieven | nee |
| `db` | Databases en datadiensten | nee |
| `remote` | Toegang op afstand — shell, bureaublad, RustDesk | nee |
| `mail` | Maildiensten | nee |
| `dns` | DNS-diensten | nee |
| `iot` | IoT-apparaten, camera's, routers, domotica | nee |
| `dev` | Ontwikkel-/labomgevingen | nee |
| `docker` | Docker, Swarm en gangbare diensten in containers | nee |
| `complet` | **Ter plekke gegenereerd**: gesorteerde, ontdubbelde vereniging van alle bovenstaande profielen | nee |
| `CUSTOM` | Een persoonlijk profiel aangemaakt in het scherm **Profielen**, en/of een vrije invoer (`80` / `22,443,8080` / `1000-2000`) — beide tellen samen, ontdubbeld | nee |

Volledige details, validatieregels en beheer van de persoonlijke profielen: `docs/PROFILES.md`.

## 5. Architectuur

Omega-check is opgebouwd volgens **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), afgestemd op het sjabloon van de suite `omega-` (zie `omega-scan`/`omega-stress`) en bij elke wijziging gecontroleerd door `import-linter`. Alle details staan in **`docs/ARCHITECTURE.md`**.

Zeer kort overzicht:

```text
src/omega_check/
├── domain/          Pure bedrijfslogica (scans, doelen, diensten, profielen, rapporten...)
├── application/     Use cases (commands/queries)
├── ports/           Contracten die de applicatie verwacht (sondes, repositories, exporteurs...)
├── infrastructure/  Concrete implementaties (socket/httpx/cryptography, SQLite; Textual staat hier NIET)
├── interfaces/      tui/ (Textual) en cli/ (scriptbaar), met strikte functionele gelijkwaardigheid
├── app/             Samenstelling (DependencyContainer, bootstrap, levenscyclus)
├── core/, shared/   Gedeeld vocabulaire, niet-bedrijfsmatige hulpmiddelen
└── plugins/         Structuur aanwezig, leeg (geen bevestigde uitbreidingsas)
```

Ontwerpregels:
- `domain/services/policies.py`: deelt de al verzamelde aanwijzingen in, doet nooit netwerkverkeer.
- `infrastructure/network/`: doet het netwerkverkeer (sockets, `httpx`, `cryptography`), oordeelt nooit.
- `interfaces/`: toont, bevat geen bedrijfslogica.
- `infrastructure/exporters/`: lezen het scanresultaat, herberekenen niets.

## 6. Identificatie van diensten en rollen

### Herkende protocollen

| Protocol | Sonde | Verzamelde details |
|---|---|---|
| HTTP / HTTPS | `httpx` | `Server`-banner, authenticatieheaders |
| TLS | `cryptography` (onderhandeld certificaat, `CERT_NONE` inbegrepen) | Versie, cipher, onderwerp/uitgever van het certificaat |
| SSH | Ruwe banner | Software en versie (bijv. `OpenSSH 10.4`) |
| VNC (RFB) | Door de server aangekondigde beveiligingscodes | Ondersteunde authenticatietypen |
| Generiek | Ruwe banner op een niet herkende open poort | Voorzichtige extractie, geen agressieve heuristiek |

### Afgeleide rollen

Afgeleid uit het **werkelijk onderhandelde** protocol, nooit uit een aanname op basis van het poortnummer:

| Rol | Voorwaarde | Vertrouwen |
|---|---|---|
| `webserver` | HTTP/HTTPS-protocol bevestigd | `INFERRED` |
| `shelltoegang` | SSH-protocol bevestigd | `CORROBORATED` |
| `grafische toegang` | VNC-protocol bevestigd | `CORROBORATED` |
| `database` | Poort binnen het bereik van het systeemprofiel `db` | `INFERRED` |

### Bekende WAF-handtekeningen

Herkend via een declaratieve header (`server`, `x-sdk`) — aanwezigheid **gedeclareerd door het doel**, nooit onafhankelijk geverifieerd: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (ter informatie vermeld, strikt genomen geen applicatie-WAF).

## 7. Vertrouwensbeleid

Elk verzameld veld draagt een van deze niveaus:

| Niveau | Betekenis |
|---|---|
| `VERIFIED` | Direct waargenomen protocolfeit dat het doel niet kan vervalsen (bijv. gesloten poort bevestigd door een TCP-RST, werkelijk onderhandelde TLS-versie). |
| `DECLARED` | Waarde die het doel zelf aankondigt in een veld dat het volledig beheert (bijv. `Server`-banner) — aannemelijk maar naar believen te vervalsen. |
| `CORROBORATED` | Een `DECLARED`-waarde bevestigd door een onafhankelijke aanwijzing (bijv. SSH-rol, omdat het protocol werkelijk onderhandeld is). |
| `INFERRED` | Afgeleid uit een patroon/heuristiek, zonder uitdrukkelijke declaratie van het doel. |
| `UNKNOWN` | Geen bruikbare aanwijzing, of actief verborgen door het doel. |

## 8. Bescherming tegen vervalste waarden

Omega-check vertrouwt geen enkel door het doel zelf gedeclareerd gegeven zonder dat uitdrukkelijk aan te geven. Een `Server`-banner of een `X-Powered-By`-header blijft `DECLARED`, nooit `VERIFIED`, hoe aannemelijk ook — het doel levert ze zelf en kan ze naar believen vervalsen. Alleen een bevestiging via een onafhankelijk kanaal (het werkelijk onderhandelde SSH-protocol voor de rol „shelltoegang”, bijvoorbeeld) brengt een gegeven naar `CORROBORATED`. Dit onderscheid, vastgelegd in `omega-lib` (`ConfidenceLevel`), is structureel: geen enkele export en geen enkele weergave kan het verbergen.

## 9. Compatibiliteit met terminals

De TUI (Textual) detecteert automatisch de mogelijkheden van de terminal (emulator, grootte) en past zijn structurele stijlblad daarop aan (`complete`/`standard`/`reduced`/`mono`), zonder handmatige optie. De CLI-modus blijft altijd platte tekst, onafhankelijk van de terminal. Beleid dat de hele suite `omega-` deelt (`omega-lib`, `terminal/policies.py`).

### Profiel volgens de gedetecteerde emulator

| Emulator | Beginprofiel |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, moderne SSH | `reduced` |
| Linux-TTY, oudere SSH | `mono` |
| Niet herkende emulator | `reduced` (standaard terugvaloptie) |

### Profiel volgens de grootte van de terminal

| Minimale grootte (kolommen × regels) | Profielplafond |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| kleiner | `mono` |

Het uiteindelijke profiel is **het strengste van de twee** (emulator en grootte) — een Ghostty op volledig scherm, verkleind tot 70 kolommen, zakt terug naar `mono`, ook al zou zijn emulator `complete` toestaan. Live te vernieuwen met de toets `r`.

## 10. Exports

Tekst- en HTML-rapporten worden geschreven in de taal die in de Instellingen gekozen is („Taal van de exports”, standaard die van de interface); JSON blijft data en wordt niet vertaald. De rapporten worden standaard aangemaakt in `var/exports/` (runtimepad verankerd in de projectmap, `$OMEGA_CHECK_VAR_DIR` om het te overschrijven), of op het opgegeven pad (`--output` in de CLI, dialoogvenster in de TUI). Duidelijke bestandsnaam met tijdstempel: `scan-{profiel}-{datum}.ext`, `scan-custom-{datum}.ext` voor een persoonlijk profiel, `scan-{datum}.ext` voor een vrije invoer zonder profiel.

### JSON, de bron van waarheid

Volledige structuur van de scan (`Scan` + `Host`), strikt JSON-serialiseerbaar, vertrouwensniveaus inbegrepen.

### Tekst, compact leesbaar rapport

Leesbaar buiten de terminal, zonder ANSI-codes.

### HTML, zelfstandig webrapport

5 thema's naar keuze (`--theme` in de CLI, keuzelijst in de TUI; volgt standaard het actieve interfacethema als er een equivalent bestaat). Eigen opmaak: container, informatieraster, statistiekvakken per poortstatus, gekleurde badges — dezelfde visuele familie als `omega-scan`/`omega-stress`.

## 11. Geschiedenis en vergelijking

Elke scan wordt opgeslagen (SQLite, `var/db/omega-check.db`): geschiedenis raadpleegbaar per doel, details van een eerdere uitvoering, vergelijking tussen twee scans (poortstatus) en opnieuw uitvoeren van een scan op hetzelfde doel zonder het opnieuw in te voeren.

## 12. Tests

```bash
source .venv/bin/activate
lint-imports        # controleert de Dependency Rule
pytest -q           # 191 tests
ruff check src tests
mypy -p omega_check
```

Structuur: `tests/unit/` (domein en applicatie, zonder echte I/O), `tests/integration/` (echte SQLite/bestanden, nagebootste HTTP-server `pytest-httpserver`, TLS via `trustme`).

## 13. Buiten de reikwijdte

- CVE-scans
- Actieve detectie van SQLi, XSS, RCE
- Herkenning van het besturingssysteem
- Low-level scantechnieken in nmap-stijl (SYN-scan, ruwe pakketten)
- Crawling
- Fuzzing
- Brute force
- Gelijktijdig scannen van meerdere doelen
- Webdashboard

---

> Omega-check — Scannen, identificeren, kwalificeren, rapporteren.
> Een poortscanner met expliciet vertrouwen, geen aanname vermomd als feit.
