# Architecture technique

Clean Architecture à 9 couches, identique dans son principe à `omega-scan`/`omega-stress` (voir `~/DEV/SUITE/DECISIONS_ARCHITECTURE.md`, décisions D-000 et D-007 pour le rationnel du choix et la manière dont les contrats ont été portés).

## Dependency Rule

```
app                                     -- racine de composition
infrastructure | interfaces | plugins   -- adaptateurs, indépendants entre eux
application                             -- cas d'usage (commands/queries)
ports                                   -- contrats (Protocol)
domain                                  -- métier pur
core                                    -- vocabulaire transverse
```

Une couche ne peut importer que les couches strictement en dessous d'elle dans cette liste (l'extérieur dépend de l'intérieur, jamais l'inverse). Vérifié à chaque modification par `import-linter` (`lint-imports`), 6 contrats :

1. **Dependency Rule** (`type = "layers"`) : l'ordre ci-dessus.
2. **`interfaces` ne dépend jamais directement de `infrastructure`** : la CLI/TUI passe toujours par `application/`, jamais de raccourci vers un adaptateur concret.
3. **`textual` confiné à `interfaces.tui`** (pas encore utilisé, TUI non commencé).
4. **`sqlite3` confiné à `infrastructure.storage.sqlite`**.
5. **`httpx` confiné à `infrastructure.network`**.
6. **`jinja2` confiné à `infrastructure.exporters.html_exporter`**.

## Pourquoi `Protocol` et pas `ABC`

Tous les ports (`ports/*.py`) sont des `typing.Protocol`, pas des `abc.ABC`. Les implémentations ne héritent pas explicitement du port — typage structurel, juste une docstring notant quel port est implémenté (ex. `"""Implemente ports/scan_repository.py::ScanRepository."""`). C'était une erreur corrigée en cours de route en Phase 2 (voir mémoire de session) : la première version de `ProfileRepository` utilisait `ABC`, incohérent avec le reste de la suite.

## Bounded contexts de `domain/`

| Sous-package | Contenu | Remarque |
|---|---|---|
| `domain/scans/` | `Scan`, cycle de vie d'un scan | |
| `domain/targets/` | `Host`, validation "scan fixe" | |
| `domain/services/` | `Port`, `Service`, `RoleElement`, `TransportLayer`, règles (`policies.py`), fusion de sondes (`service.py`) | Nommé `services/`, pas `ports/` — évite la collision avec la couche hexagonale `ports/`. |
| `domain/profiles/` | `Profile`, profils système, règles de validation | |
| `domain/reports/` | Comparaison de scans | |

`domain/services/policies.py` consolide ce qui serait ailleurs séparé en `role_rules.py`/`architecture_rules.py`/`confidence_rules.py` — un seul fichier, cohérent avec `OMEGA-CHECK_ARBORESCENCE.md` §1.

## Le pipeline de scan (vue d'ensemble)

```
CLI (scan_command)
  └─ application/commands/run_scan.py
       ├─ ports/dns_resolver.py                → résolution de la cible
       ├─ ports/port_prober.py (par port)       → open/closed/filtered
       └─ pour chaque port OPEN :
            application/commands/probe_service.py
              ├─ domain/services/policies.py::classify_probe_strategy(port)
              ├─ ports/http_prober.py + ports/tls_prober.py (HTTPS)
              │    → domain/services/service.py::merge_probes
              ├─ ports/ssh_prober.py / ports/vnc_prober.py / ports/generic_banner_prober.py
              └─ domain/services/service.py::enrich_with_role_and_layers
                   ├─ domain/services/policies.py::infer_role
                   └─ domain/services/policies.py::build_transport_layers
       └─ ports/scan_repository.py::save() + save_host()   → persistance SQLite
```

## Limites connues (documentées, pas des oublis)

- **Détection de reverse proxy / cache HTTP** (headers `X-Forwarded-*`, `Via`, `Age`, `X-Cache`) : non implémentée. `Service` ne conserve pas les en-têtes HTTP bruts (seulement des champs déjà interprétés) — l'implémenter demanderait d'étendre `infrastructure/network/httpx_http_prober.py` et `Service` en amont.
- **Chaînes de rôles inter-ports** (ex. NGINX:80 → Lighttpd:8080 sur le même host) : dépend de la même détection de proxy manquante ci-dessus.
- **Authentification SSH** : seul le banner est lu (protocole/logiciel/version). L'énumération des méthodes d'authentification demanderait un échange de clés SSH partiel, hors-scope.
- **VNC** : la sonde s'arrête après la négociation des security types, avant toute tentative d'authentification (sonde passive, pas d'identifiants à essayer).
- **Système de thèmes HTML** : un seul thème intégré. Un système à plusieurs thèmes (comme `omega-scan`/`omega-stress`) sera pertinent une fois le TUI construit, pour la cohérence visuelle CLI/TUI/HTML.

## Bibliothèque partagée (`omega-lib`)

`ConfidenceLevel` et les utilitaires transverses (`clock`, `ids`, `typing`) viennent de `~/DEV/LIB/omega-lib`, installé en dépendance éditable — voir D-005. Depuis la construction du TUI (D-008), `omega-lib` porte aussi tout le système de thème (`theme/{models,policies,service}.py` — catalogue de 10 thèmes TUI + 5 thèmes d'export, identique à `omega-scan`/`omega-stress`) et de détection terminal (`terminal/*`, `infrastructure/terminal/*`, ports `terminal_detector`/`settings_store`) : ces modules étaient déjà documentés dans `omega-scan` comme "identiques à omega-stress", donc mûrs pour la mutualisation dès que CHECK en avait besoin, plutôt que dupliqués une 3e fois.

Le reste (probes, modèles `Scan`/`Host`/`Port`/`Service`) reste dupliqué entre `omega-check` et les futurs `omega-deep`/`omega-fold`, décision assumée pour éviter la sur-généralisation avant d'avoir plusieurs implémentations réelles à comparer.

## Interface TUI

`interfaces/tui/` suit le même patron que `omega-scan`/`omega-stress` : `app.py` (résout thème + profil de rendu au démarrage, enchaîne splash → accueil), `screens/_base.py::OmegaScreen` (retour `Échap` uniforme), `controllers/startup_controller.py`, `rendering/{stylesheet_loader,textual_theme_builder}.py`. Les feuilles de style (`styles/{base,complete,standard,reduced,mono}.tcss`) sont portées verbatim — mêmes classes `.omega-btn-frame`/`.omega-actions`/etc., même séparation décoration (bordure, jamais recolorée)/interactivité (fond `$accent` au survol/focus) qui évite le bug de bordure carrée documenté dans `base.tcss`.

Différences assumées avec `omega-scan` (voir D-008 pour le détail) : pas d'écran de gestion des cibles épinglées (pas de concept d'autorisation persistée chez CHECK), pas de gestion de profils depuis le TUI, pas de relai de log en direct pendant un scan, artwork du splash simplifié (texte plutôt que glyphes dessinés lettre par lettre — l'alphabet dessiné d'omega-scan ne couvre pas C/H/K).
