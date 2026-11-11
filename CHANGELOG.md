# Changelog

Format inspiré de [Keep a Changelog](https://keepachangelog.com/).

## [1.6.0] — non publiée (2026-11-09)

### Ajouté

- **Aide → « Contact et support »** (repris d'omega-serv et d'omega-log), depuis l'aide (touche `a`) :
  payer un café (page PayPal), contacter le support (mail et formulaire de contact du site, affichés en
  clair ; aucun formulaire dans l'outil, aucun mail envoyé), se déclarer utilisateur anonyme, vérifier les
  mises à jour. Sans session graphique (SSH), l'adresse s'affiche au lieu d'ouvrir le navigateur.
- **Déclaration anonyme, une seule fois** (omega-check n'a pas de service qui enverrait chaque jour) : clé
  tirée au hasard, nom et version de l'outil, continent et pays facultatifs (listes fermées, jamais de
  texte libre) ; le message exact est affiché avant l'envoi. Rien n'est enregistré si la réception est
  injoignable. « Ne plus me déclarer » supprime l'entrée à la réception et la clé locale
  (`var/declaration.json`, jamais livrée dans l'archive).
- **Vérifier les mises à jour** : compare la version installée à la liste publiée sur le site
  (`download/sha.txt`), seulement sur clic ; « Voir les nouveautés » ouvre le fichier de la dernière
  version.
- README ×17 : section « Contact et support ».
- README ×17 : captures A-D (accueil, menu, détail d'un scan, historique) dans chaque langue ; site en 17 langues (index et readme.html).

### Modifié

- Écrans « Contact et support » et « Se déclarer » partagés dans omega-lib, avec leurs traductions
  (17 langues) : le même écran dans tous les outils omega.

### Corrigé

- Réglages : l'écran est centré comme dans le reste de la suite (le bloc « Langue / Language » prenait
  toute la largeur et repoussait tout à gauche).
- Réglages : plus de notification à l'ouverture de l'écran (« Comme l'interface », profil de rendu) ;
  seul un vrai changement est enregistré et annoncé.
- Langues : les 16 traductions sont validées, la mention « en test » disparaît du sélecteur.

## [1.5.0] — 2026-10-29

### Ajouté

- Interface en 17 langues (français, anglais, espagnol, portugais (Brésil), italien, allemand, néerlandais, polonais, russe, chinois simplifié, vietnamien, thaï, indonésien, japonais, coréen, hindi et arabe) : Réglages → « Langue / Language », appliquée après un redémarrage de l'interface ; variable `OMEGA_CHECK_LANG` pour forcer une langue le temps d'une session. Lancé depuis omega-suite, l'outil prend la langue de la suite.
- Réglage « Langue des exports » (« Comme l'interface » par défaut) : les rapports HTML et texte s'écrivent dans la langue choisie ; en arabe, le rapport HTML se lit de droite à gauche. Les exports JSON et CSV restent des données (clés et valeurs inchangées).

### Modifié

- Accents rétablis dans tous les textes français de l'interface et des rapports.
- Les résultats enregistrés en français sont retraduits à l'affichage et dans les exports.
- La ligne de commande reste en français.

## [Unreleased]

### Corrigé

- Réglages : « Supprimer les exports » et « Supprimer les screenshots » vident le dossier **choisi** dans les champs Export / Captures (et plus toujours le dossier par défaut), avec le chemin exact dans la confirmation ; l'export propose désormais aussi ce dossier (le réglage était enregistré mais jamais relu). Seul le contenu est supprimé, liens symboliques non suivis, dossiers système/personnels et dossier de l'application refusés, éléments non supprimables signalés, suppression en arrière-plan (correctif 2026-10-27 commun à la suite).

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
