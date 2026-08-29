# Copyright (c) 2026 kraynux - Licence MIT
"""Composition ASCII de l'ecran de demarrage. Logo fourni par l'utilisateur,
voir ~/DEV/CHECK/ascii.txt et ~/DEV/CHECK/nouveau splash.png (visuel de
reference, logo redessine en round 2) — caracteres non modifies.

Alignement : chaque ligne est centree via `str.center(_WIDTH)` (largeur de
la boite OMEGA-CHECK, l'element le plus large) plutot que de reproduire les
espaces d'indentation du fichier source — meme raisonnement que le premier
correctif de centrage (chaque ligne est deja symetrique en elle-meme, les
centrer toutes sur le meme axe restaure la forme voulue). Round 2 : plus de
ligne vide entre la boite OMEGA-CHECK et le motif decoratif du bas, ni
entre ce motif et la tagline (retour utilisateur).

Couleur par jetons de theme Rich/Textual (`$accent`=vif, `$foreground`
=clair) directement dans le markup — pas des couleurs hex figees a la
construction (meme mecanisme que widgets/home_wordmark.py, reactif au
changement de theme). Regles de couleur fournies/confirmees par
l'utilisateur (voir ascii.txt) :
- cadres/"containers" (boites de bordure) : clair.
- texte "LINUX SERVER CHECK" : vif.
- bandeau OMEGA-CHECK (3 lignes, dans sa boite) : vif / clair / vif,
  meme repartition que widgets/home_wordmark.py.
- tagline du bas : les "|" separateurs vifs, les mots clairs — INVERSE
  de la convention d'omega-scan (mots vifs, "|" clairs) : choix
  deliberement different pour CHECK, pas une erreur de copie.
- pyramide et motif decoratif du bas (blocs ╠▓╣/░) : clair (retour
  utilisateur round 2, corrige le vif par defaut du premier jet)."""
from __future__ import annotations

from textual.widgets import Static

_WIDTH = 84
"""Largeur de la boite OMEGA-CHECK (l'element le plus large) : axe de
centrage commun a tout le logo."""


def _centered(line: str) -> str:
    return line.center(_WIDTH)


def _split_frame(line: str, frame_char: str = "│") -> str:
    """Ligne du type '│ texte │' (deja centree) -> cadre clair, texte vif."""
    prefix, _, rest = line.partition(frame_char)
    inner, _, suffix = rest.rpartition(frame_char)
    return f"{prefix}[$foreground]{frame_char}[/][$accent]{inner}[/][$foreground]{frame_char}{suffix}[/]"


def _wordmark_line(line: str, color: str, frame_char: str = "│") -> str:
    """Ligne du bandeau OMEGA-CHECK a l'interieur de sa boite : cadre
    clair, contenu dans la couleur demandee (vif/clair selon la ligne)."""
    prefix, _, rest = line.partition(frame_char)
    inner, _, suffix = rest.rpartition(frame_char)
    return f"{prefix}[$foreground]{frame_char}[/][{color}]{inner}[/][$foreground]{frame_char}{suffix}[/]"


def _tagline(line: str) -> str:
    """'SCAN | PORTS | ...' -> mots clairs, '|' vifs."""
    parts = line.split("|")
    colored = [f"[$foreground]{part}[/]" for part in parts]
    return "[$accent]|[/]".join(colored)


_LINUX_BOX = (
    "┌────────────────────────┐",
    "│   LINUX SERVER CHECK   │",
    "└────────────────────────┘",
)

_SMALL_PYRAMID = (
    "╔╗",
    "░╠▓▓▓╣╠▓▓▓╣░",
    "░╠▓▓▓▓▓╣v1.0╠▓▓▓▓▓╣░",
)

_OMEGA_BOX = (
    "┌──────────────────────────────────────────────────────────────────────────────────┐",
    "│ ┌╦═══╦┐ ┌╦═╦═╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐   ┌╦═══╦┐ ┌╦   ╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╗╔══┐ │",
    "│ │║   ║│ │║ ║ ║│ ├╬══    │║  ═╦┐ ├╬═══╬┤ ═ │║      ├╬═══╬┤ ├╬══    │║      │╠╩╗   │",
    "│ └╩═══╩┘ └╩   ╩┘ └╩═══╩┘ └╩═══╩┘ └╩   ╩┘   └╩═══╩┘ └╩   ╩┘ └╩═══╩┘ └╩═══╩┘ └╝ ╚═┘ │",
    "└──────────────────────────────────────────────────────────────────────────────────┘",
)

_BIG_DIAMOND = (
    "░╠▓▓╣   ╠▓╣░     ╔╗     ░╠▓╣   ╠▓▓╣░",
    "░╠══════════╣░  ░╠═╣╠═╣░  ░╠══════════╣░",
    "░╠▓▓╣   ╠▓╣░     ╚╝     ░╠▓╣   ╠▓▓╣░",
    "░╠▓╣   ╠▓╣░          ░╠▓╣   ╠▓╣░",
    "░╠▓╣   ╠▓╣░   ╔╗   ░╠▓╣   ╠▓╣░",
    "░╠▓╣   ╠▓▓▓▓▓╣╠▓▓▓▓▓╣   ╠▓╣░",
    "░╠▓╣       ║║       ╠▓╣░",
    "░╠▓▓▓▓▓▓▓╣╠▓▓▓▓▓▓▓╣░",
    "░╠▓▓▓╣╠▓▓▓╣░",
    "╚╝",
)

_TAGLINE = "SCAN | PORTS | SERVICES | RULES | EXPORT"

_LINES: tuple[str, ...] = (
    f"[$foreground]{_centered(_LINUX_BOX[0])}[/]",
    _split_frame(_centered(_LINUX_BOX[1])),
    f"[$foreground]{_centered(_LINUX_BOX[2])}[/]",
    f"[$foreground]{_centered(_SMALL_PYRAMID[0])}[/]",
    f"[$foreground]{_centered(_SMALL_PYRAMID[1])}[/]",
    f"[$foreground]{_centered(_SMALL_PYRAMID[2])}[/]",
    f"[$foreground]{_centered(_OMEGA_BOX[0])}[/]",
    _wordmark_line(_centered(_OMEGA_BOX[1]), "$accent"),
    _wordmark_line(_centered(_OMEGA_BOX[2]), "$foreground"),
    _wordmark_line(_centered(_OMEGA_BOX[3]), "$accent"),
    f"[$foreground]{_centered(_OMEGA_BOX[4])}[/]",
    *[f"[$foreground]{_centered(row)}[/]" for row in _BIG_DIAMOND],
    _tagline(_centered(_TAGLINE)),
)

_MARKUP = "\n".join(_LINES)


class SplashHero(Static):
    """Bloc decoratif de l'ecran de demarrage (screens/splash.py)."""

    def __init__(self) -> None:
        super().__init__(_MARKUP, classes="omega-splash-hero")
