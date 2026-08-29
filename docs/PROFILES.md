# Profils de ports

Un profil est un nom associé à une liste de ports à scanner. Deux origines :

- **Système** (`origin = "system"`) : fournis avec l'outil, lecture seule, définis dans `domain/profiles/defaults.py`.
- **Utilisateur** (`origin = "user"`) : créés/modifiés/supprimés via `omega-check profile ...`, persistés en JSON (`~/.config/omega-check/user_profiles.json` par défaut).

Un profil utilisateur ne peut pas porter le nom d'un profil système (noms réservés, voir `domain/profiles/policies.py::ensure_name_not_reserved`).

## Profils système

| Nom | Description | Épinglé |
|---|---|---|
| `minimal` | Scan ultra-rapide : SSH + HTTP + HTTPS (22, 80, 443) | oui |
| `classic` | Services classiques Internet/LAN (37 ports) | oui |
| `web` | Services web et alternatives (80, 443, 8000-10443) | non |
| `db` | Bases de données et services de données (MySQL, PostgreSQL, MongoDB, Redis, etc.) | non |
| `remote` | Accès distants — shell, bureau, RustDesk | non |
| `mail` | Services de messagerie (SMTP, IMAP, POP3) | non |
| `dns` | Services DNS (53, 853, 5353) | non |
| `iot` | Équipements IoT, caméras, box, domotique | non |
| `dev` | Environnements de développement/lab | non |
| `docker` | Docker, Swarm et services courants en conteneurs | non |
| `complet` | **Généré dynamiquement** : union triée et dédupliquée de tous les profils ci-dessus | non |

`complet` n'existe pas comme entrée statique : `domain/profiles/defaults.py::build_complete_profile()` le recalcule à chaque appel à partir des profils système ci-dessus, pour rester automatiquement à jour si un profil système évolue.

## Gestion des profils utilisateur

```bash
omega-check profile list
omega-check profile create <nom> --ports <p1,p2,...> [--description <texte>] [--pin]
omega-check profile edit <nom> [--description <texte>] [--ports <p1,p2,...>]
omega-check profile delete <nom>
omega-check profile pin <nom>
omega-check profile unpin <nom>
```

Règles de validation (`domain/profiles/policies.py`) :

- Chaque port doit être compris entre 1 et 65535.
- Pas de doublons dans la liste de ports d'un même profil.
- Le nom ne doit pas être un nom de profil système (ni `complet`).

`pin`/`unpin` ne s'appliquent qu'aux profils utilisateur : le statut épinglé d'un profil système est fixé une fois pour toutes dans `defaults.py`, il ne se persiste pas.
