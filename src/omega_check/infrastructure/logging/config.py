# Copyright (c) 2026 kraynux - Licence MIT
"""Configuration du logger applicatif technique (stdlib logging). Porte
depuis omega-scan/omega-stress (D-007/D-008) — CHECK en etait jusqu'ici
completement depourvu : `application/commands/run_scan.py` emet deja des
`logging.getLogger("omega_check.scan").info(...)` (relayes en direct vers
le RichLog de l'ecran de progression TUI, voir
interfaces/tui/screens/scan_progress.py), mais sans handler de fichier
configure nulle part, ces lignes ne survivaient jamais a l'ecran de
progression — aucune trace apres coup, en TUI comme en CLI.

Le logger 'omega_check.scan' est un enfant de 'omega_check' (nom
configure ici) : ses records remontent naturellement (propagation stdlib
par defaut) jusqu'au handler fichier installe ici, sans rien changer a
run_scan.py ni au relai TUI existant."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

LOGGER_NAME = "omega_check"
APP_LOG_FILENAME = "app.log"
DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging(*, log_path: Path, level: int = logging.INFO, console: bool = True) -> logging.Logger:
    """Configure et retourne le logger applicatif nomme 'omega_check', avec
    un handler fichier (toujours actif) et un handler console optionnel.
    Idempotent : rappeler cette fonction remplace les handlers existants
    plutot que d'en accumuler (utile en tests).

    `console=False` sous le TUI (voir app/bootstrap.py) : Textual controle
    l'ecran en mode alternatif, une ecriture directe sur stderr pendant un
    scan corromprait son rendu (defilement, curseur/spinner desynchronise)
    — meme raisonnement/bug deja documente chez omega-scan."""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False  # evite une double emission si le root logger est configure ailleurs (ex. pytest)

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
