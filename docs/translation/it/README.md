<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licenza MIT (vedi il file LICENSE) -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**Scanner di porte, servizi e ruoli di rete (destinazione singola)**

> Realizzato da [kraynux](https://github.com/kraynux) per [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Pagina ufficiale: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Anteprima: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interfaccia e report esportati disponibili in **17 lingue** — vedi [Lingue dell'interfaccia](#lingue-dellinterfaccia).  
**Lingue:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** è uno strumento TUI + CLI che analizza le porte di una singola destinazione di rete, identifica il servizio in esecuzione su ogni porta aperta (protocollo, software, versione, autenticazione, WAF, TLS) e ne deduce il ruolo probabile, senza mai effettuare un attacco attivo. Strumento della suite `omega-`, strutturato in Clean Architecture — vedi `docs/ARCHITECTURE.md` per tutti i dettagli tecnici.

## 1. Visione e perimetro

Omega-check è uno scanner di porte orientato all'amministrazione di sistema: verificare rapidamente cosa è in ascolto su una macchina (la propria, la LAN o una destinazione esterna autorizzata), con cosa, e con quanta fiducia ogni informazione può essere considerata acquisita.

### Cosa fa Omega-check

- Analizza un elenco di porte (profilo di sistema, profilo personale o inserimento libero) su una destinazione singola.
- Identifica il servizio in esecuzione su ogni porta aperta: protocollo (HTTP/HTTPS/SSH/TLS/VNC/generico), software e versione quando sono esposti, necessità di autenticazione.
- Deduce un ruolo probabile (server web, accesso shell, accesso grafico, database) dal protocollo realmente negoziato, mai da una semplice supposizione basata sulla porta.
- Rileva le firme di WAF note (Cloudflare, Sucuri, Akamai, Imperva Incapsula) quando sono dichiarate nelle intestazioni.
- Presenta il risultato in TUI (Textual) o in CLI scriptabile, e tramite tre esportazioni: JSON, testo, HTML (5 temi).
- Attribuisce a ogni informazione raccolta un livello di fiducia esplicito — vedi [§7](#7-politica-di-fiducia).
- Conserva una cronologia persistente delle scansioni, ripetibile e confrontabile nel tempo.
- Permette di fissare destinazioni e creare profili di porte personali, riutilizzabili da una scansione all'altra.

### Cosa non fa Omega-check

- Scansione attiva delle vulnerabilità: niente SQLi, XSS o RCE.
- Scansione di CVE.
- Rilevamento del sistema operativo (il modello di dati prevede il campo, nessuna euristica lo compila per ora).
- Tecniche di scansione a basso livello in stile nmap (SYN scan, pacchetti grezzi) — solo connessione TCP applicativa.
- Strumento di forza bruta o di fuzzing.
- Scansione parallela di più destinazioni.
- Dashboard web.

## 2. Installazione

### Prerequisiti

- Python 3.10+
- Connessione a Internet, per le dipendenze

### Installazione

```bash
[ -d omega-check ] && echo "ℹ️ Già estratto qui, passaggio saltato." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Crea l'ambiente virtuale `.venv` se non esiste già.
2. Installa le dipendenze (`pip install -e .`; `pyproject.toml` resta l'unica fonte di verità).
3. Rende eseguibili `omega-check.sh` e `install.sh`.
4. Aggiunge l'alias `check` a `~/.bashrc` e `~/.zshrc` (senza duplicati se già presente).

### Dipendenze

Dichiarate in `pyproject.toml` (niente più `requirements.txt`):
- `omega-lib`: libreria condivisa della suite (`ConfidenceLevel`, temi, rilevamento del terminale)
- `textual`: interfaccia TUI, temi, adattamento automatico al terminale
- `httpx`: sonda HTTP/HTTPS
- `cryptography`: lettura del certificato TLS negoziato
- `jinja2`: template per l'esportazione HTML
- Dipendenze di sviluppo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Utilizzo

### Modalità interattiva (TUI)

Consigliata per l'uso quotidiano — avviata senza argomenti:

```bash
./omega-check.sh
```
se hai creato l'alias, digita semplicemente `check` nel terminale:
```bash
check
```

Percorso: schermata iniziale (si chiude con un tasto o un clic) → menu principale (Scansiona / Obiettivi / Profili / Cronologia / Impostazioni / Aiuto) → inserimento della destinazione (con selettore delle destinazioni fissate) e scelta del profilo (avviso con `complet`, un secondo campo per un profilo personale o un inserimento libero di porte con `CUSTOM`) → scansione (indicatore indeterminato e registro delle operazioni di rete in tempo reale) → dettaglio della scansione (porte/servizi/ruoli, esportazione) → cronologia/confronto/ripetizione e impostazioni dal menu principale. L'adattamento al terminale (colori, dimensioni, degradazione strutturale) è automatico.

#### Scorciatoie da tastiera

| Tasto | Azione |
|---|---|
| `↑` / `↓` | Spostarsi tra gli elementi di una schermata |
| `Tab` / `Maiusc+Tab` | Spostarsi tra i campi di un modulo |
| `Esc` | Tornare alla schermata precedente (conferma di uscita nella schermata iniziale) |
| `t` | Tema successivo (applicato subito, senza conferma) |
| `r` | Aggiornare il rilevamento del terminale |
| `a` | Mostrare l'aiuto |
| `q` | Uscire (con conferma) |

### Lingue dell'interfaccia

L'interfaccia è disponibile in 17 lingue: francese, inglese, spagnolo, portoghese (Brasile), italiano, tedesco, olandese, polacco, russo, cinese semplificato, vietnamita, thailandese, indonesiano, giapponese, coreano, hindi e arabo. La scelta si fa nelle Impostazioni («Langue / Language») e vale dopo il riavvio dell'interfaccia; la variabile `OMEGA_CHECK_LANG` (per esempio `OMEGA_CHECK_LANG=it ./omega-check.sh`) impone una lingua per una sessione. Avviato da omega-suite, omega-check usa la lingua della suite. In una console di testo Linux (TTY), le lingue con scrittura non latina vengono mostrate in inglese per la sessione. La riga di comando resta in francese.

### Modalità scriptabile (CLI)

Qualsiasi sottocomando attiva la modalità CLI:

```bash
# Analizzare una destinazione con un profilo di porte
./omega-check.sh scan 192.168.1.10 --profile minimal

# Cronologia (filtrabile per destinazione)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Dettaglio di una scansione (testo, JSON o HTML) — 5 temi di esportazione a scelta
./omega-check.sh show <scan_id> --format html --theme omega-base --output report.html

# Confrontare due scansioni (cambiamenti di stato delle porte)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Profili di porte personali
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "Il mio profilo"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### Formati di destinazione accettati

```text
192.168.1.10                IPv4
example.org                 Nome host
http://example.org          URL HTTP  (schema rimosso prima della risoluzione)
https://example.org:8443    URL HTTPS con porta  (schema e porta rimossi)
```

Lo schema e l'eventuale porta vengono rimossi prima della risoluzione DNS (`domain/targets/validation.py::normalize_target_input`) — incollare un URL intero funziona, viene conservato solo l'host.

## 4. Profili di scansione

| Profilo | Descrizione | Fissato |
|---|---|---|
| `minimal` | Scansione rapidissima: SSH + HTTP + HTTPS (22, 80, 443) | sì |
| `classic` | Servizi classici Internet/LAN (37 porte) | sì |
| `web` | Servizi web e alternative | no |
| `db` | Database e servizi di dati | no |
| `remote` | Accessi remoti — shell, desktop, RustDesk | no |
| `mail` | Servizi di posta | no |
| `dns` | Servizi DNS | no |
| `iot` | Dispositivi IoT, telecamere, router, domotica | no |
| `dev` | Ambienti di sviluppo/laboratorio | no |
| `docker` | Docker, Swarm e servizi comuni in container | no |
| `complet` | **Generato al volo**: unione ordinata e senza duplicati di tutti i profili qui sopra | no |
| `CUSTOM` | Un profilo personale creato nella schermata **Profili**, e/o un inserimento libero (`80` / `22,443,8080` / `1000-2000`) — i due si sommano, senza duplicati | no |

Dettaglio completo, regole di validazione e gestione dei profili personali: `docs/PROFILES.md`.

## 5. Architettura

Omega-check è strutturato in **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), allineata al modello della suite `omega-` (vedi `omega-scan`/`omega-stress`) e verificata da `import-linter` a ogni modifica. Tutti i dettagli sono in **`docs/ARCHITECTURE.md`**.

Panoramica molto breve:

```text
src/omega_check/
├── domain/          Logica di business pura (scansioni, destinazioni, servizi, profili, report...)
├── application/     Casi d'uso (commands/queries)
├── ports/           Contratti attesi dall'applicazione (sonde, repository, esportatori...)
├── infrastructure/  Implementazioni concrete (socket/httpx/cryptography, SQLite; Textual NON è qui)
├── interfaces/      tui/ (Textual) e cli/ (scriptabile), con parità funzionale rigorosa
├── app/             Assemblaggio (DependencyContainer, bootstrap, ciclo di vita)
├── core/, shared/   Vocabolario trasversale, utilità non di business
└── plugins/         Struttura predisposta, vuota (nessun asse di estensione confermato)
```

Regole di progettazione:
- `domain/services/policies.py`: classifica gli indizi già raccolti, non fa mai rete.
- `infrastructure/network/`: fa rete (socket, `httpx`, `cryptography`), non giudica mai.
- `interfaces/`: mostra, non contiene alcuna logica di business.
- `infrastructure/exporters/`: leggono il risultato della scansione, non ricalcolano nulla.

## 6. Identificazione dei servizi e ruoli

### Protocolli rilevati

| Protocollo | Sonda | Dettaglio raccolto |
|---|---|---|
| HTTP / HTTPS | `httpx` | Banner `Server`, intestazioni di autenticazione |
| TLS | `cryptography` (certificato negoziato, `CERT_NONE` incluso) | Versione, cifrario, soggetto/emittente del certificato |
| SSH | Banner grezzo | Software e versione (es. `OpenSSH 10.4`) |
| VNC (RFB) | Codici di sicurezza annunciati dal server | Tipi di autenticazione supportati |
| Generico | Banner grezzo su porta aperta non riconosciuta | Estrazione prudente, nessuna euristica aggressiva |

### Ruoli dedotti

Ricavati dal protocollo **realmente negoziato**, mai da una supposizione basata sul numero di porta:

| Ruolo | Condizione | Fiducia |
|---|---|---|
| `server web` | Protocollo HTTP/HTTPS confermato | `INFERRED` |
| `accesso shell` | Protocollo SSH confermato | `CORROBORATED` |
| `accesso grafico` | Protocollo VNC confermato | `CORROBORATED` |
| `database` | Porta nell'intervallo del profilo di sistema `db` | `INFERRED` |

### Firme WAF note

Rilevate tramite un'intestazione dichiarativa (`server`, `x-sdk`) — presenza **dichiarata dalla destinazione**, mai verificata in modo indipendente: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (elencato a titolo indicativo, non è propriamente un WAF applicativo).

## 7. Politica di fiducia

Ogni campo raccolto porta uno di questi livelli:

| Livello | Significato |
|---|---|
| `VERIFIED` | Fatto di protocollo osservato direttamente, che la destinazione non può falsificare (es.: porta chiusa confermata da un RST TCP, versione TLS realmente negoziata). |
| `DECLARED` | Valore autodichiarato dalla destinazione in un campo che controlla interamente (es.: banner `Server`) — plausibile ma falsificabile a piacere. |
| `CORROBORATED` | Un valore `DECLARED` confermato da un indizio indipendente (es.: ruolo SSH, essendo il protocollo realmente negoziato). |
| `INFERRED` | Dedotto da uno schema/euristica, senza dichiarazione esplicita della destinazione. |
| `UNKNOWN` | Nessun indizio utilizzabile, oppure nascosto attivamente dalla destinazione. |

## 8. Protezione contro i valori falsificati

Omega-check non si fida di alcun dato autodichiarato dalla destinazione senza segnalarlo esplicitamente. Un banner `Server` o un'intestazione `X-Powered-By` resta `DECLARED`, mai `VERIFIED`, per quanto plausibile — è la destinazione stessa a fornirli e può falsificarli a piacere. Solo una conferma tramite un canale indipendente (il protocollo SSH realmente negoziato per il ruolo «accesso shell», per esempio) porta un'informazione a `CORROBORATED`. Questa distinzione, gestita in `omega-lib` (`ConfidenceLevel`), è strutturale: nessuna esportazione e nessuna vista possono nasconderla.

## 9. Compatibilità con i terminali

La TUI (Textual) rileva automaticamente le capacità del terminale (emulatore, dimensioni) e adatta di conseguenza il suo foglio di stile strutturale (`complete`/`standard`/`reduced`/`mono`), senza opzioni manuali. La modalità CLI resta sempre in testo semplice, indipendente dal terminale. Politica condivisa da tutta la suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Profilo secondo l'emulatore rilevato

| Emulatore | Profilo iniziale |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderno | `reduced` |
| TTY Linux, SSH datato | `mono` |
| Emulatore non riconosciuto | `reduced` (ripiego predefinito) |

### Profilo secondo le dimensioni del terminale

| Dimensione minima (colonne × righe) | Tetto del profilo |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| al di sotto | `mono` |

Il profilo finale è **il più restrittivo dei due** (emulatore e dimensioni) — un Ghostty a schermo intero ridimensionato a 70 colonne scende a `mono`, anche se il suo emulatore consentirebbe `complete`. Aggiornabile in tempo reale con il tasto `r`.

## 10. Esportazioni

I report testo e HTML vengono scritti nella lingua scelta nelle Impostazioni («Lingua delle esportazioni», per impostazione predefinita quella dell'interfaccia); il JSON resta un dato, non tradotto. I report vengono generati in `var/exports/` per impostazione predefinita (percorso di esecuzione ancorato alla cartella del progetto, `$OMEGA_CHECK_VAR_DIR` per sovrascriverlo), oppure nel percorso indicato (`--output` in CLI, finestra di dialogo in TUI). Nome di file esplicito e con data e ora: `scan-{profilo}-{data}.ext`, `scan-custom-{data}.ext` per un profilo personale, `scan-{data}.ext` per un inserimento libero senza profilo.

### JSON, fonte di verità

Struttura completa della scansione (`Scan` + `Host`), rigorosamente serializzabile in JSON, livelli di fiducia inclusi.

### Testo, report leggibile compatto

Leggibile fuori dal terminale, senza codici ANSI.

### HTML, report web autonomo

5 temi a scelta (`--theme` in CLI, selettore in TUI; segue per impostazione predefinita il tema attivo dell'interfaccia quando esiste un equivalente). Impaginazione dedicata: contenitore, griglia di informazioni, riquadri di statistiche per stato della porta, badge colorati — stessa famiglia visiva di `omega-scan`/`omega-stress`.

## 11. Cronologia e confronto

Ogni scansione viene salvata (SQLite, `var/db/omega-check.db`): cronologia consultabile per destinazione, dettaglio di un'esecuzione passata, confronto tra due scansioni (stato delle porte) e ripetizione di una scansione sulla stessa destinazione senza reinserirla.

## 12. Test

```bash
source .venv/bin/activate
lint-imports        # verifica la Dependency Rule
pytest -q           # 191 test
ruff check src tests
mypy -p omega_check
```

Struttura: `tests/unit/` (dominio e applicazione, senza I/O reale), `tests/integration/` (SQLite/file reali, server HTTP fittizio `pytest-httpserver`, TLS tramite `trustme`).

## 13. Fuori perimetro

- Scansione di CVE
- Rilevamento attivo di SQLi, XSS, RCE
- Rilevamento del sistema operativo
- Tecniche di scansione a basso livello in stile nmap (SYN scan, pacchetti grezzi)
- Crawling
- Fuzzing
- Forza bruta
- Scansione simultanea di più destinazioni
- Dashboard web

---

> Omega-check — Analizzare, identificare, qualificare, riferire.
> Uno scanner di porte con una fiducia esplicita, non una supposizione travestita da fatto.
