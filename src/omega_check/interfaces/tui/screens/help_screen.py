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

_SHORTCUTS = (
    ("Haut / Bas", "Naviguer entre les elements d'un ecran"),
    ("Tab / Maj+Tab", "Naviguer entre les champs d'un formulaire"),
    ("Echap", "Retour a l'ecran precedent (confirmation de sortie sur l'accueil)"),
    ("t", "Theme suivant (applique immediatement, sans confirmation)"),
    ("r", "Rafraichir la detection du terminal"),
    ("a", "Cette aide"),
    ("q", "Quitter (avec confirmation)"),
)

_SECTIONS = (
    (
        "Scanner",
        (
            "Saisir une cible (IP ou hostname) et un profil de ports, puis lancer le scan. "
            "Chaque port OPEN est ensuite identifie (protocole, logiciel, role) automatiquement."
        ),
    ),
    (
        "Historique",
        (
            "Liste tous les scans passes : detail complet, comparaison entre deux scans "
            "(marquer une reference puis comparer), ou rejouer un scan sur la meme cible."
        ),
    ),
    (
        "Export",
        (
            "Depuis le detail d'un scan : JSON (structure complete), texte (rapport compact) "
            "ou HTML (rapport visuel, theme d'export independant du theme de l'interface)."
        ),
    ),
)

_SCOPE_NOTICE = (
    "Omega-check identifie les services d'une cible unique (scan fixe, pas de derive "
    "vers d'autres IPs) : ports TCP, protocole, logiciel, authentification, WAF, TLS, "
    "role inferer. Jamais de test actif ni d'authentification tentee."
)


class HelpScreen(OmegaScreen):
    """Reference statique, accessible depuis n'importe quel ecran (touche `a`)."""

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes="omega-panel"):
            yield Static("AIDE", classes="omega-title")
            yield Static("Raccourcis clavier", classes="omega-subtitle")
            for key, description in _SHORTCUTS:
                yield Static(f"{key:<14} {description}")
            yield Static("")
            yield Static("Fonctions", classes="omega-subtitle")
            for title, description in _SECTIONS:
                yield Static(f"[b]{title}[/b]\n{description}\n")
            yield Static("")
            yield Static("Profils de ports systeme", classes="omega-subtitle")
            yield DataTable(id="profile-table")
            yield Static("")
            yield Static(_SCOPE_NOTICE, classes="omega-subtitle")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button("Retour", id="back")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#profile-table", DataTable)
        table.add_columns("Profil", "Description", "Ports", "Epingle")
        for profile in SYSTEM_PROFILES.values():
            table.add_row(
                profile.name, profile.description, str(len(profile.ports)), "oui" if profile.pinned else "non"
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
