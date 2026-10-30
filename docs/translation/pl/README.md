<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencja MIT (zobacz plik LICENSE) -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**Skaner portów, usług i ról sieciowych (pojedynczy cel)**

> Stworzone przez **kraynux** dla **Omega-server** 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Oficjalna strona: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Podgląd: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interfejs i eksportowane raporty dostępne w **17 językach** — zobacz [Języki interfejsu](#języki-interfejsu).  
**Języki:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** to narzędzie TUI + CLI, które skanuje porty pojedynczego celu sieciowego, rozpoznaje usługę działającą na każdym otwartym porcie (protokół, oprogramowanie, wersja, uwierzytelnianie, WAF, TLS) i wnioskuje jej prawdopodobną rolę, nigdy nie przeprowadzając aktywnego ataku. Narzędzie pakietu `omega-`, zbudowane zgodnie z Clean Architecture — pełne szczegóły techniczne w `docs/ARCHITECTURE.md`.

## 1. Wizja i zakres

Omega-check to skaner portów nastawiony na administrację systemami: szybko sprawdzić, co nasłuchuje na maszynie (własnej, w sieci LAN lub na autoryzowanym celu zewnętrznym), czym, i z jaką pewnością można uznać każdą informację za ustaloną.

### Co robi Omega-check

- Skanuje listę portów (profil systemowy, profil własny lub dowolne wpisanie) na pojedynczym celu.
- Rozpoznaje usługę działającą na każdym otwartym porcie: protokół (HTTP/HTTPS/SSH/TLS/VNC/ogólny), oprogramowanie i wersję, gdy są ujawnione, wymóg uwierzytelnienia.
- Wnioskuje prawdopodobną rolę (serwer WWW, dostęp do powłoki, dostęp graficzny, baza danych) na podstawie faktycznie wynegocjowanego protokołu, nigdy na podstawie samego przypuszczenia z numeru portu.
- Wykrywa znane sygnatury WAF (Cloudflare, Sucuri, Akamai, Imperva Incapsula), gdy są zadeklarowane w nagłówkach.
- Przedstawia wynik w TUI (Textual) lub w skryptowalnym CLI oraz w trzech eksportach: JSON, tekst, HTML (5 motywów).
- Nadaje każdej zebranej informacji wyraźny poziom pewności — zobacz [§7](#7-zasady-pewności).
- Prowadzi trwałą historię skanów, którą można odtwarzać i porównywać w czasie.
- Pozwala przypinać cele i tworzyć własne profile portów, wielokrotnego użytku między skanami.

### Czego Omega-check nie robi

- Aktywnego skanowania podatności: bez SQLi, XSS czy RCE.
- Skanowania CVE.
- Rozpoznawania systemu operacyjnego (model danych przewiduje to pole, na razie żadna heurystyka go nie wypełnia).
- Niskopoziomowych technik skanowania w stylu nmap (skan SYN, surowe pakiety) — tylko połączenie TCP na poziomie aplikacji.
- Narzędzia do brute force ani fuzzingu.
- Równoległego skanowania wielu celów.
- Panelu WWW.

## 2. Instalacja

### Wymagania

- Python 3.10+
- Połączenie z Internetem, dla zależności

### Instalacja

```bash
[ -d omega-check ] && echo "ℹ️ Już tu rozpakowano, krok pominięty." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Tworzy środowisko wirtualne `.venv`, jeśli jeszcze nie istnieje.
2. Instaluje zależności (`pip install -e .`; `pyproject.toml` pozostaje jedynym źródłem prawdy).
3. Nadaje plikom `omega-check.sh` i `install.sh` prawo wykonywania.
4. Dodaje alias `check` do `~/.bashrc` i `~/.zshrc` (bez duplikatu, jeśli już istnieje).

### Zależności

Zadeklarowane w `pyproject.toml` (już bez `requirements.txt`):
- `omega-lib`: wspólna biblioteka pakietu (`ConfidenceLevel`, motywy, wykrywanie terminala)
- `textual`: interfejs TUI, motywy, automatyczne dopasowanie do terminala
- `httpx`: sonda HTTP/HTTPS
- `cryptography`: odczyt wynegocjowanego certyfikatu TLS
- `jinja2`: szablony dla eksportu HTML
- Zależności deweloperskie (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Użycie

### Tryb interaktywny (TUI)

Zalecany do codziennego użytku — uruchamiany bez argumentów:

```bash
./omega-check.sh
```
jeśli utworzono alias, wystarczy wpisać `check` w terminalu:
```bash
check
```

Przebieg: ekran startowy (zamyka się klawiszem lub kliknięciem) → menu główne (Skanuj / Cele / Profile / Historia / Ustawienia / Pomoc) → wprowadzenie celu (z wyborem przypiętych celów) i wybór profilu (ostrzeżenie przy `complet`, drugie pole na profil własny lub dowolne wpisanie portów przy `CUSTOM`) → skan (nieokreślony wskaźnik postępu i bieżący dziennik operacji sieciowych) → szczegóły skanu (porty/usługi/role, eksport) → historia/porównanie/ponowne uruchomienie i ustawienia z menu głównego. Dopasowanie do terminala (kolory, rozmiar, uproszczenie struktury) jest automatyczne.

#### Skróty klawiszowe

| Klawisz | Działanie |
|---|---|
| `↑` / `↓` | Przechodzenie między elementami ekranu |
| `Tab` / `Shift+Tab` | Przechodzenie między polami formularza |
| `Esc` | Powrót do poprzedniego ekranu (potwierdzenie wyjścia na ekranie głównym) |
| `t` | Następny motyw (stosowany od razu, bez potwierdzenia) |
| `r` | Odświeżenie wykrywania terminala |
| `a` | Wyświetlenie pomocy |
| `q` | Wyjście (z potwierdzeniem) |

### Języki interfejsu

Interfejs jest dostępny w 17 językach: francuskim, angielskim, hiszpańskim, portugalskim (Brazylia), włoskim, niemieckim, niderlandzkim, polskim, rosyjskim, chińskim uproszczonym, wietnamskim, tajskim, indonezyjskim, japońskim, koreańskim, hindi i arabskim. Wyboru dokonuje się w Ustawieniach („Langue / Language”), a zmiana obowiązuje po ponownym uruchomieniu interfejsu; zmienna `OMEGA_CHECK_LANG` (na przykład `OMEGA_CHECK_LANG=pl ./omega-check.sh`) wymusza język na czas jednej sesji. Uruchomiony z omega-suite, omega-check przejmuje język pakietu. W tekstowej konsoli Linuksa (TTY) języki o piśmie innym niż łacińskie są na czas sesji wyświetlane po angielsku. Wiersz poleceń pozostaje po francusku.

### Tryb skryptowy (CLI)

Każde podpolecenie włącza tryb CLI:

```bash
# Skanowanie celu z profilem portów
./omega-check.sh scan 192.168.1.10 --profile minimal

# Historia (z filtrowaniem według celu)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Szczegóły skanu (tekst, JSON lub HTML) — do wyboru 5 motywów eksportu
./omega-check.sh show <scan_id> --format html --theme omega-base --output raport.html

# Porównanie dwóch skanów (zmiany stanu portów)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Własne profile portów
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "Mój profil"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### Akceptowane formaty celu

```text
192.168.1.10                IPv4
example.org                 Nazwa hosta
http://example.org          URL HTTP  (schemat usuwany przed rozwiązaniem nazwy)
https://example.org:8443    URL HTTPS z portem  (schemat i port usuwane)
```

Schemat i ewentualny port są usuwane przed rozwiązaniem DNS (`domain/targets/validation.py::normalize_target_input`) — wklejenie całego URL działa, zachowywany jest tylko host.

## 4. Profile skanowania

| Profil | Opis | Przypięty |
|---|---|---|
| `minimal` | Bardzo szybki skan: SSH + HTTP + HTTPS (22, 80, 443) | tak |
| `classic` | Klasyczne usługi Internetu/LAN (37 portów) | tak |
| `web` | Usługi WWW i alternatywne | nie |
| `db` | Bazy danych i usługi danych | nie |
| `remote` | Dostęp zdalny — powłoka, pulpit, RustDesk | nie |
| `mail` | Usługi pocztowe | nie |
| `dns` | Usługi DNS | nie |
| `iot` | Urządzenia IoT, kamery, routery, automatyka domowa | nie |
| `dev` | Środowiska deweloperskie/laboratoryjne | nie |
| `docker` | Docker, Swarm i typowe usługi w kontenerach | nie |
| `complet` | **Generowany na bieżąco**: posortowana suma wszystkich powyższych profili, bez duplikatów | nie |
| `CUSTOM` | Własny profil utworzony na ekranie **Profile** i/lub dowolne wpisanie (`80` / `22,443,8080` / `1000-2000`) — oba się sumują, bez duplikatów | nie |

Pełne szczegóły, zasady walidacji i zarządzanie własnymi profilami: `docs/PROFILES.md`.

## 5. Architektura

Omega-check jest zbudowany zgodnie z **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), wzorowaną na szablonie pakietu `omega-` (zobacz `omega-scan`/`omega-stress`) i sprawdzaną przez `import-linter` przy każdej zmianie. Wszystkie szczegóły znajdują się w **`docs/ARCHITECTURE.md`**.

Bardzo krótki przegląd:

```text
src/omega_check/
├── domain/          Czysta logika biznesowa (skany, cele, usługi, profile, raporty...)
├── application/     Przypadki użycia (commands/queries)
├── ports/           Kontrakty oczekiwane przez aplikację (sondy, repozytoria, eksportery...)
├── infrastructure/  Konkretne implementacje (socket/httpx/cryptography, SQLite; Textual NIE jest tutaj)
├── interfaces/      tui/ (Textual) i cli/ (skryptowalne), ze ścisłą równością funkcji
├── app/             Składanie (DependencyContainer, bootstrap, cykl życia)
├── core/, shared/   Wspólne słownictwo, narzędzia niezwiązane z logiką biznesową
└── plugins/         Struktura przygotowana, pusta (brak potwierdzonej osi rozszerzeń)
```

Zasady projektowe:
- `domain/services/policies.py`: klasyfikuje już zebrane wskazówki, nigdy nie korzysta z sieci.
- `infrastructure/network/`: korzysta z sieci (gniazda, `httpx`, `cryptography`), nigdy nie ocenia.
- `interfaces/`: wyświetla, nie zawiera żadnej logiki biznesowej.
- `infrastructure/exporters/`: czytają wynik skanu, niczego nie przeliczają.

## 6. Rozpoznawanie usług i role

### Wykrywane protokoły

| Protokół | Sonda | Zbierane szczegóły |
|---|---|---|
| HTTP / HTTPS | `httpx` | Baner `Server`, nagłówki uwierzytelniania |
| TLS | `cryptography` (wynegocjowany certyfikat, łącznie z `CERT_NONE`) | Wersja, szyfr, podmiot/wystawca certyfikatu |
| SSH | Surowy baner | Oprogramowanie i wersja (np. `OpenSSH 10.4`) |
| VNC (RFB) | Kody bezpieczeństwa ogłaszane przez serwer | Obsługiwane rodzaje uwierzytelniania |
| Ogólny | Surowy baner na nierozpoznanym otwartym porcie | Ostrożna ekstrakcja, bez agresywnej heurystyki |

### Wnioskowane role

Wyprowadzane z **faktycznie wynegocjowanego** protokołu, nigdy z przypuszczenia na podstawie numeru portu:

| Rola | Warunek | Pewność |
|---|---|---|
| `serwer WWW` | Potwierdzony protokół HTTP/HTTPS | `INFERRED` |
| `dostęp do powłoki` | Potwierdzony protokół SSH | `CORROBORATED` |
| `dostęp graficzny` | Potwierdzony protokół VNC | `CORROBORATED` |
| `baza danych` | Port w zakresie profilu systemowego `db` | `INFERRED` |

### Znane sygnatury WAF

Wykrywane na podstawie nagłówka deklaratywnego (`server`, `x-sdk`) — obecność **zadeklarowana przez cel**, nigdy niezależnie weryfikowana: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (wymieniony informacyjnie, nie jest to ściśle WAF aplikacyjny).

## 7. Zasady pewności

Każde zebrane pole ma jeden z tych poziomów:

| Poziom | Znaczenie |
|---|---|
| `VERIFIED` | Fakt protokołowy zaobserwowany bezpośrednio, którego cel nie może sfałszować (np. zamknięty port potwierdzony przez TCP RST, faktycznie wynegocjowana wersja TLS). |
| `DECLARED` | Wartość ogłoszona przez sam cel w polu, które w pełni kontroluje (np. baner `Server`) — wiarygodna, ale dowolnie fałszowalna. |
| `CORROBORATED` | Wartość `DECLARED` potwierdzona niezależną wskazówką (np. rola SSH, ponieważ protokół faktycznie został wynegocjowany). |
| `INFERRED` | Wyprowadzona z wzorca/heurystyki, bez wyraźnej deklaracji celu. |
| `UNKNOWN` | Brak użytecznej wskazówki lub aktywnie ukryte przez cel. |

## 8. Ochrona przed sfałszowanymi wartościami

Omega-check nie ufa żadnym danym zadeklarowanym przez sam cel, nie zaznaczając tego wyraźnie. Baner `Server` czy nagłówek `X-Powered-By` pozostaje `DECLARED`, nigdy `VERIFIED`, bez względu na wiarygodność — dostarcza je sam cel i może je dowolnie fałszować. Tylko potwierdzenie niezależnym kanałem (na przykład faktycznie wynegocjowany protokół SSH dla roli „dostęp do powłoki”) podnosi informację do `CORROBORATED`. To rozróżnienie, zapisane w `omega-lib` (`ConfidenceLevel`), jest strukturalne: żaden eksport ani widok nie może go ukryć.

## 9. Zgodność z terminalami

TUI (Textual) automatycznie wykrywa możliwości terminala (emulator, rozmiar) i odpowiednio dostosowuje swój strukturalny arkusz stylów (`complete`/`standard`/`reduced`/`mono`), bez ręcznej opcji. Tryb CLI zawsze pozostaje zwykłym tekstem, niezależnie od terminala. Zasada wspólna dla całego pakietu `omega-` (`omega-lib`, `terminal/policies.py`).

### Profil według wykrytego emulatora

| Emulator | Profil początkowy |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, nowoczesne SSH | `reduced` |
| TTY Linuksa, starsze SSH | `mono` |
| Nierozpoznany emulator | `reduced` (domyślna wartość zapasowa) |

### Profil według rozmiaru terminala

| Minimalny rozmiar (kolumny × wiersze) | Górna granica profilu |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| poniżej | `mono` |

Ostateczny profil to **bardziej restrykcyjny z dwóch** (emulator i rozmiar) — Ghostty na pełnym ekranie zmniejszony do 70 kolumn spada do `mono`, choć jego emulator pozwalałby na `complete`. Można go odświeżyć na bieżąco klawiszem `r`.

## 10. Eksporty

Raporty tekstowe i HTML są zapisywane w języku wybranym w Ustawieniach („Język eksportów”, domyślnie język interfejsu); JSON pozostaje danymi i nie jest tłumaczony. Raporty są domyślnie tworzone w `var/exports/` (ścieżka robocza zakotwiczona w folderze projektu, `$OMEGA_CHECK_VAR_DIR`, aby ją zmienić) albo pod wskazaną ścieżką (`--output` w CLI, okno dialogowe w TUI). Jednoznaczna nazwa pliku ze znacznikiem czasu: `scan-{profil}-{data}.ext`, `scan-custom-{data}.ext` dla profilu własnego, `scan-{data}.ext` dla dowolnego wpisania bez profilu.

### JSON, źródło prawdy

Pełna struktura skanu (`Scan` + `Host`), ściśle serializowalna do JSON, łącznie z poziomami pewności.

### Tekst, zwięzły raport do czytania

Czytelny poza terminalem, bez kodów ANSI.

### HTML, samodzielny raport WWW

5 motywów do wyboru (`--theme` w CLI, wybór w TUI; domyślnie podąża za aktywnym motywem interfejsu, jeśli istnieje odpowiednik). Własny układ: kontener, siatka informacji, ramki statystyk według stanu portu, kolorowe odznaki — ta sama rodzina wizualna co `omega-scan`/`omega-stress`.

## 11. Historia i porównanie

Każdy skan jest zapisywany (SQLite, `var/db/omega-check.db`): historia przeglądana według celu, szczegóły dawnego uruchomienia, porównanie dwóch skanów (stan portów) i ponowne uruchomienie skanu na tym samym celu bez ponownego wpisywania.

## 12. Testy

```bash
source .venv/bin/activate
lint-imports        # sprawdza Dependency Rule
pytest -q           # 191 testów
ruff check src tests
mypy -p omega_check
```

Struktura: `tests/unit/` (domena i aplikacja, bez prawdziwych operacji wejścia/wyjścia), `tests/integration/` (prawdziwe SQLite/pliki, pozorowany serwer HTTP `pytest-httpserver`, TLS przez `trustme`).

## 13. Poza zakresem

- Skanowanie CVE
- Aktywne wykrywanie SQLi, XSS, RCE
- Rozpoznawanie systemu operacyjnego
- Niskopoziomowe techniki skanowania w stylu nmap (skan SYN, surowe pakiety)
- Crawling
- Fuzzing
- Brute force
- Jednoczesne skanowanie wielu celów
- Panel WWW

---

> Omega-check — Skanować, rozpoznawać, oceniać, raportować.
> Skaner portów z wyraźnie określoną pewnością, a nie przypuszczenie przebrane za fakt.
