# Changelog

Format inspiré de [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Ajouté

- Fondations : arborescence 9 couches, `ConfidenceLevel`/`PortState`/`ScanMode`/`ScanStatus`, gestion des profils de ports (système + utilisateur).
- Scan de ports TCP (open/closed/filtered) avec résolution DNS.
- Identification de service : HTTP/HTTPS (fingerprint logiciel, authentification, WAF, TLS), SSH, VNC, banner générique.
- Inférence de rôle par service et reconstruction de la pile protocolaire.
- Persistance SQLite complète (scans, hosts, ports, services).
- Historique des scans, comparaison de deux scans, export JSON/TXT/HTML.
- CLI complète : `scan`, `history`, `show`, `compare`, `profile list/create/edit/delete/pin/unpin`.

### Limites connues

- Pas de détection de reverse proxy / cache HTTP (nécessiterait la conservation des en-têtes HTTP bruts).
- Pas de chaînes de rôles inter-ports.
- SSH : méthodes d'authentification non énumérées (banner seulement).
- Un seul thème HTML intégré (pas de système de thèmes multiples).
- Pas encore de TUI.
