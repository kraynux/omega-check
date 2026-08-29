# Exemples d'usage

## Scanner une cible

```bash
$ omega-check scan 127.0.0.1 --profile minimal
Scan 03b76155c0cb4faa84402fbd144d1cb0 — cible 127.0.0.1 (127.0.0.1) — statut completed
3 port(s) scanne(s) :
     22/tcp — open     [verified]
         └─ SSH OpenSSH 10.4, role=acces shell [corroborated]
     80/tcp — closed   [verified]
    443/tcp — closed   [verified]
```

Un port `filtered` apparaît quand la cible ne répond pas dans le délai (`--timeout`, défaut 1s) après épuisement des tentatives — comportement typique d'un pare-feu qui droppe silencieusement, mais pas une certitude (`INFERRED`, jamais `VERIFIED`).

## Consulter l'historique

```bash
$ omega-check history --target 127.0.0.1 --limit 5
03b76155c0cb4faa84402fbd144d1cb0  2026-08-29T06:47:50+00:00  127.0.0.1 (127.0.0.1)  completed
```

## Exporter un rapport

```bash
# Texte détaillé sur stdout
omega-check show 03b76155c0cb4faa84402fbd144d1cb0

# JSON complet (structure de l'agrégat Scan + Host, exploitable par un autre outil)
omega-check show 03b76155c0cb4faa84402fbd144d1cb0 --format json

# HTML, écrit dans un fichier
omega-check show 03b76155c0cb4faa84402fbd144d1cb0 --format html --output rapport.html
```

## Comparer deux scans dans le temps

```bash
$ omega-check scan 192.168.1.10 --profile web   # scan initial
$ omega-check scan 192.168.1.10 --profile web   # quelques jours plus tard
$ omega-check compare <scan_id_ancien> <scan_id_recent>
Comparaison <scan_id_ancien> -> <scan_id_recent>
Ports presents seulement dans <scan_id_recent> : [8443]
Changements d'etat :
  port 8080 : closed -> open
```

Utile pour repérer un port qui s'est ouvert entre deux scans d'une même cible (dérive de configuration, service oublié, etc.).

## Créer un profil de ports sur mesure

```bash
$ omega-check profile create labo --ports 22,2222,8080 --description "Bastion + app interne"
Profil 'labo' cree (3 port(s)).

$ omega-check scan 10.0.0.5 --profile labo
```

## Workflow typique (audit périodique)

```bash
# 1. Scan initial de référence (noter le scan_id affiché)
omega-check scan target.example --profile complet

# 2. Scans réguliers (cron, etc.)
omega-check scan target.example --profile complet

# 3. Comparaison avec la référence pour détecter une dérive
omega-check history --target target.example
omega-check compare <id_baseline> <id_dernier_scan>
```
