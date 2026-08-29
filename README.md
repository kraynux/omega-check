#  OMEGA-CHECK

**Scanneur de ports, services et rôles réseau (cible unique)**

Élaboré par kraynux pour Omega-server
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)
Page officiel :
[OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-check/) 
Apercu :
[Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

---

Omega-check est un outil TUI + CLI qui scanne les ports d'une cible réseau unique, identifie le service qui tourne sur chaque port ouvert (protocole, logiciel, version, authentification, WAF, TLS) et infère son rôle probable, sans jamais effectuer d'attaque active. Quatrième outil de la suite `omega-` (après `omega-fire`, `omega-stress` et `omega-scan`), structuré en Clean Architecture — voir `docs/ARCHITECTURE.md` pour le détail technique complet.

## 1. Vision et périmètre

Omega-check est un scanneur de ports orienté administration système : vérifier rapidement ce qui écoute sur une machine (la sienne, le LAN, ou une cible externe autorisée), avec quoi, et depuis combien de confiance chaque information peut être tenue pour acquise.

### Ce que fait Omega-check

- Scanne une liste de ports (profil système, profil personnel, ou saisie libre) sur une cible unique.
- Identifie le service tournant sur chaque port ouvert : protocole (HTTP/HTTPS/SSH/TLS/VNC/générique), logiciel et version quand ils sont exposés, exigence d'authentification.
- Infère un rôle probable (serveur web, accès shell, accès graphique, base de données) à partir du protocole réellement négocié, jamais d'une simple supposition de port.
- Détecte les signatures de WAF connues (Cloudflare, Sucuri, Akamai, Imperva Incapsula) quand elles sont déclarées dans les en-têtes.
- Restitue le résultat en TUI (Textual) ou en CLI scriptable, et via trois exports : JSON, texte, HTML (5 thèmes).
- Qualifie chaque information collectée d'un niveau de confiance explicite — voir [§7](#7-politique-de-confiance).
- Conserve un historique persistant des scans, rejouable et comparable dans le temps.
- Permet d'épingler des cibles et de créer des profils de ports personnels, réutilisables d'un scan à l'autre.

### Ce qu'Omega-check ne fait pas

- Scan de vulnérabilités actives, pas de SQLi, XSS ou RCE.
- Scan de CVE.
- Prise d'empreinte du système d'exploitation (le modèle de données prévoit le champ, aucune heuristique ne le renseigne à ce jour).
- Techniques de scan bas niveau façon nmap (SYN scan, paquets bruts) — connexion TCP applicative uniquement.
- Outil de bruteforce ou de fuzzing.
- Scan multi-cibles parallèle.
- Dashboard web.

## 2. Installation

### Prérequis

- Python 3.10+
- Connexion Internet, pour les dépendances

### Installation

```bash
[ -d omega-check ] && echo "ℹ️ Déjà extrait ici, étape ignorée." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh` :

1. Crée l'environnement virtuel `.venv` s'il n'existe pas déjà.
2. Installe les dépendances (`pip install -e .`, `pyproject.toml` reste l'unique source de vérité).
3. Rend `omega-check.sh` et `install.sh` exécutables.
4. Ajoute l'alias `check` à `~/.bashrc` et `~/.zshrc` (sans doublon si déjà présent).

### Dépendances

Déclarées dans `pyproject.toml` (plus de `requirements.txt`) :
- `omega-lib` : bibliothèque partagée de la suite (`ConfidenceLevel`, thèmes, détection de terminal)
- `textual` : interface TUI, thèmes, adaptation automatique au terminal
- `httpx` : sonde HTTP/HTTPS
- `cryptography` : lecture du certificat TLS négocié
- `jinja2` : templating pour l'export HTML
- Dépendances de développement (`pip install -e ".[dev]"`) : `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Utilisation

### Mode interactif (TUI)

Recommandé pour l'usage quotidien — lancé sans argument :

```bash
./omega-check.sh
```
si vous avez créé l'alias, tapez juste `check` dans le terminal :
```bash
check
```

Parcours : écran de démarrage (se ferme sur une touche ou un clic) → menu principal (Scanner / Cibles / Profils / Historique / Réglages / Aide) → saisie de la cible (avec picker de cibles épinglées) et choix du profil (avertissement si `complet`, deuxième champ pour un profil personnel ou une saisie libre de ports si `CUSTOM`) → scan (jauge indéterminée et déroulé des opérations réseau en direct) → détail du scan (ports/services/rôles, export) → historique/comparaison/rejeu et réglages depuis le menu principal. L'adaptation au terminal (couleurs, taille, dégradation structurelle) est automatique.

#### Raccourcis clavier

| Touche | Action |
|---|---|
| `↑` / `↓` | Naviguer entre les éléments d'un écran |
| `Tab` / `Maj+Tab` | Naviguer entre les champs d'un formulaire |
| `Échap` | Retour à l'écran précédent (confirmation de sortie sur l'accueil) |
| `t` | Thème suivant (appliqué immédiatement, sans confirmation) |
| `r` | Rafraîchir la détection du terminal |
| `a` | Afficher l'aide |
| `q` | Quitter (avec confirmation) |

### Mode scriptable (CLI)

Toute sous-commande déclenche le mode CLI :

```bash
# Scanner une cible avec un profil de ports
./omega-check.sh scan 192.168.1.10 --profile minimal

# Historique (filtrable par cible)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Détail d'un scan (texte, JSON ou HTML) — 5 thèmes d'export au choix
./omega-check.sh show <scan_id> --format html --theme omega-base --output rapport.html

# Comparer deux scans (changements d'état de port)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Profils de ports personnels
./omega-check.sh profile list
./omega-check.sh profile create labo --ports 22,80,443 --description "Mon profil"
./omega-check.sh profile edit labo --ports 22,80,443,8080
./omega-check.sh profile pin labo
./omega-check.sh profile unpin labo
./omega-check.sh profile delete labo
```

### Formats de cible acceptés

```text
192.168.1.10                IPv4
example.org                 Hostname
http://example.org          URL HTTP  (schéma retiré avant résolution)
https://example.org:8443    URL HTTPS avec port  (schéma et port retirés)
```

Le schéma et le port éventuels sont retirés avant résolution DNS (`domain/targets/validation.py::normalize_target_input`) — coller une URL entière fonctionne, seul l'hôte est conservé.

## 4. Profils de scan

| Profil | Description | Épinglé |
|---|---|---|
| `minimal` | Scan ultra-rapide : SSH + HTTP + HTTPS (22, 80, 443) | oui |
| `classic` | Services classiques Internet/LAN (37 ports) | oui |
| `web` | Services web et alternatives | non |
| `db` | Bases de données et services de données | non |
| `remote` | Accès distants — shell, bureau, RustDesk | non |
| `mail` | Services de messagerie | non |
| `dns` | Services DNS | non |
| `iot` | Équipements IoT, caméras, box, domotique | non |
| `dev` | Environnements de développement/lab | non |
| `docker` | Docker, Swarm et services courants en conteneurs | non |
| `complet` | **Généré à la volée** : union triée et dédupliquée de tous les profils ci-dessus | non |
| `CUSTOM` | Un profil personnel créé dans l'écran **Profils**, et/ou une saisie libre (`80` / `22,443,8080` / `1000-2000`) — les deux se cumulent, dédoublonnés | non |

Détail complet, règles de validation et gestion des profils personnels : `docs/PROFILES.md`.

## 5. Architecture

Omega-check est structuré en **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alignée sur le gabarit de la suite `omega-` (voir `omega-scan`/`omega-stress`) et vérifiée par `import-linter` à chaque modification. Le détail complet vit dans **`docs/ARCHITECTURE.md`**.

Vue d'ensemble très courte :

```text
src/omega_check/
├── domain/          Logique métier pure (scans, cibles, services, profils, rapports...)
├── application/     Cas d'usage (commands/queries)
├── ports/           Contrats attendus par l'application (probers, repositories, exporters...)
├── infrastructure/  Implémentations concrètes (socket/httpx/cryptography, SQLite, Textual n'est PAS ici)
├── interfaces/      tui/ (Textual) et cli/ (scriptable), à parité fonctionnelle stricte
├── app/             Assemblage (DependencyContainer, bootstrap, cycle de vie)
├── core/, shared/   Vocabulaire transverse, utilitaires non métier
└── plugins/         Structure posée, vide (aucun axe d'extension confirmé)
```

Règles de conception :
- `domain/services/policies.py` : classifie les indices déjà collectés, ne fait jamais de réseau.
- `infrastructure/network/` : fait du réseau (sockets, `httpx`, `cryptography`), ne juge jamais.
- `interfaces/` : affiche, ne contient aucune logique métier.
- `infrastructure/exporters/` : lisent le résultat de scan, ne recalculent rien.

## 6. Identification de service et rôles

### Protocoles détectés

| Protocole | Sonde | Détail collecté |
|---|---|---|
| HTTP / HTTPS | `httpx` | Bannière `Server`, en-têtes d'authentification |
| TLS | `cryptography` (certificat négocié, `CERT_NONE` inclus) | Version, cipher, sujet/émetteur du certificat |
| SSH | Bannière brute | Logiciel et version (ex. `OpenSSH 10.4`) |
| VNC (RFB) | Codes de sécurité annoncés par le serveur | Types d'authentification supportés |
| Générique | Bannière brute sur port ouvert non reconnu | Extraction prudente, pas d'heuristique agressive |

### Rôles inférés

Déduits du protocole **réellement négocié**, jamais d'une supposition de numéro de port :

| Rôle | Condition | Confiance |
|---|---|---|
| `serveur web` | Protocole HTTP/HTTPS confirmé | `INFERRED` |
| `accès shell` | Protocole SSH confirmé | `CORROBORATED` |
| `accès graphique` | Protocole VNC confirmé | `CORROBORATED` |
| `base de données` | Port dans la plage du profil système `db` | `INFERRED` |

### Signatures WAF connues

Détectées via en-tête déclaratif (`server`, `x-sdk`) — présence **déclarée par la cible**, jamais vérifiée indépendamment : Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (répertorié à titre indicatif, pas un WAF applicatif à proprement parler).

## 7. Politique de confiance

Chaque champ collecté porte un niveau parmi :

| Niveau | Signification |
|---|---|
| `VERIFIED` | Fait protocolaire observé directement, non falsifiable par la cible (ex : port fermé confirmé par RST TCP, version TLS réellement négociée). |
| `DECLARED` | Valeur auto-annoncée par la cible dans un champ qu'elle contrôle entièrement (ex : bannière `Server`) — plausible mais falsifiable à volonté. |
| `CORROBORATED` | Une valeur `DECLARED` confirmée par un indice indépendant (ex : rôle SSH, le protocole ayant réellement été négocié). |
| `INFERRED` | Déduit d'un pattern/heuristique, sans déclaration explicite de la cible. |
| `UNKNOWN` | Aucun indice exploitable, ou activement masqué par la cible. |

## 8. Protection contre les valeurs falsifiées

Omega-check ne fait confiance à aucune donnée auto-déclarée par la cible sans le signaler explicitement. Une bannière `Server` ou un en-tête `X-Powered-By` reste `DECLARED`, jamais `VERIFIED`, quelle que soit sa plausibilité — c'est la cible elle-même qui les fournit, elle peut les falsifier à volonté. Seule une confirmation par un canal indépendant (le protocole SSH réellement négocié pour le rôle « accès shell », par exemple) fait passer une information en `CORROBORATED`. Cette distinction, portée dans `omega-lib` (`ConfidenceLevel`), est structurelle : aucun export ni aucune vue ne peut l'occulter.

## 9. Compatibilité terminaux

Le TUI (Textual) détecte automatiquement les capacités du terminal (émulateur, taille) et adapte sa feuille de style structurelle en conséquence (`complete`/`standard`/`reduced`/`mono`), sans flag manuel. Le mode CLI reste toujours en texte simple, indépendant du terminal. Politique partagée par toute la suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Profil selon l'émulateur détecté

| Émulateur | Profil initial |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderne | `reduced` |
| TTY Linux, SSH legacy | `mono` |
| Émulateur non reconnu | `reduced` (repli par défaut) |

### Profil selon la taille du terminal

| Taille minimale (colonnes × lignes) | Plafond de profil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| en dessous | `mono` |

Le profil final retenu est **le plus restrictif des deux** (émulateur et taille) — un Ghostty en plein écran redimensionné à 70 colonnes redescend en `mono`, même si son émulateur autoriserait `complete`. Rafraîchissable en direct par la touche `r`.

## 10. Exports

Les rapports sont générés dans `var/exports/` par défaut (chemin runtime ancré sur le dossier du projet, `$OMEGA_CHECK_VAR_DIR` pour le surcharger), ou au chemin indiqué (`--output` en CLI, boîte de dialogue en TUI). Nom de fichier explicite et horodaté : `scan-{profil}-{date}.ext`, `scan-custom-{date}.ext` pour un profil personnel, `scan-{date}.ext` pour une saisie libre sans profil.

### JSON, source de vérité

Structure complète du scan (`Scan` + `Host`), strictement JSON-sérialisable, niveaux de confiance inclus.

### Texte, rapport humain compact

Lisible hors terminal, sans codes ANSI.

### HTML, rapport web autonome

5 thèmes au choix (`--theme` en CLI, sélecteur en TUI ; suit le thème d'interface actif par défaut quand un équivalent existe). Mise en page dédiée : conteneur, grille d'infos, encarts de statistiques par état de port, badges colorés — même famille visuelle que `omega-scan`/`omega-stress`.

## 11. Historique et comparaison

Chaque scan est persisté (SQLite, `var/db/omega-check.db`) : historique consultable par cible, détail d'un run passé, comparaison entre deux scans (état des ports), et rejeu d'un scan sur la même cible sans ressaisie.

## 12. Tests

```bash
source .venv/bin/activate
lint-imports        # verifie la Dependency Rule
pytest -q           # 173 tests
ruff check src tests
mypy -p omega_check
```

Structure : `tests/unit/` (domaine et application, sans I/O réelle), `tests/integration/` (SQLite/fichiers réels, serveur HTTP factice `pytest-httpserver`, TLS via `trustme`).

## 13. Hors périmètre

- Scan de CVE
- Détection active de SQLi, XSS, RCE
- Prise d'empreinte du système d'exploitation
- Techniques de scan bas niveau façon nmap (SYN scan, paquets bruts)
- Crawling
- Fuzzing
- Bruteforce
- Scan multi-cibles simultané
- Dashboard web

---

> Omega-check — Scanner, identifier, qualifier, rapporter.
> Un scanneur de ports avec une confiance explicite, pas une supposition déguisée en fait.
