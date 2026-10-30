# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran Aide : reference statique des raccourcis et fonctions de l'application.
Adapte du patron screens/help_screen.py d'omega-scan (D-007/D-008) — memes
raccourcis, contenu propre a CHECK pour les sections/profils."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, DataTable, Footer, Header, Static

from omega_check.domain.profiles.defaults import SYSTEM_PROFILES
from omega_check.interfaces.tui.screens._base import OmegaScreen
from omega_check.shared.i18n import _

_SHORTCUTS = (
    (_("Haut / Bas"), _("Naviguer entre les éléments d'un écran")),
    (_("Tab / Maj+Tab"), _("Naviguer entre les champs d'un formulaire")),
    (_("Échap"), _("Retour à l'écran précédent (confirmation de sortie sur l'accueil)")),
    ("t", _("Thème suivant (appliqué immédiatement, sans confirmation)")),
    ("r", _("Rafraîchir la détection du terminal")),
    ("a", _("Cette aide")),
    ("q", _("Quitter (avec confirmation)")),
)

_SECTIONS = (
    (
        _("Scanner"),
        (
            _("Saisir une cible (IP ou hostname) et un profil de ports, puis lancer le scan. "
              "Chaque port OPEN est ensuite identifié (protocole, logiciel, rôle) "
              "automatiquement.")
        ),
    ),
    (
        _("Historique"),
        (
            _("Liste tous les scans passés : détail complet, comparaison entre deux scans "
              "(marquer une référence puis comparer), ou rejouer un scan sur la même cible.")
        ),
    ),
    (
        _("Export"),
        (
            _("Depuis le détail d'un scan : JSON (structure complète), texte (rapport compact) "
              "ou HTML (rapport visuel, thème d'export indépendant du thème de l'interface).")
        ),
    ),
)

_SCOPE_NOTICE = (
    _("Omega-check identifie les services d'une cible unique (scan fixe, pas de dérive vers "
      "d'autres IPs) : ports TCP, protocole, logiciel, authentification, WAF, TLS, rôle "
      "inféré. Jamais de test actif ni d'authentification tentée.")
)


class HelpScreen(OmegaScreen):
    """Reference statique, accessible depuis n'importe quel ecran (touche `a`)."""

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("AIDE"), classes="omega-title")
            yield Static(_("Raccourcis clavier"), classes="omega-subtitle")
            for key, description in _SHORTCUTS:
                yield Static(_("{key:<14} {description}").format(key=key, description=description))
            yield Static("")
            yield Static(_("Fonctions"), classes="omega-subtitle")
            for title, description in _SECTIONS:
                yield Static(f"[b]{title}[/b]\n{description}\n")
            yield Static("")
            yield Static(_("Profils de ports système"), classes="omega-subtitle")
            yield DataTable(id="profile-table")
            yield Static("")
            yield Static(_SCOPE_NOTICE, classes="omega-subtitle")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#profile-table", DataTable)
        table.add_columns(_("Profil"), _("Description"), _("Ports"), _("Épinglé"))
        for profile in SYSTEM_PROFILES.values():
            table.add_row(
                profile.name, profile.description, str(len(profile.ports)), _("oui") if profile.pinned else _("non")
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
