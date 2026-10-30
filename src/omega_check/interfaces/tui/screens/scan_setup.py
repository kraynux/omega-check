# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran de saisie : cible, profil de ports. Adapte du patron
screens/scan_setup.py d'omega-scan (D-007/D-008) — simplifie : CHECK n'a
pas de concept de cibles autorisees (pas de garde-fou d'autorisation, le
'scan fixe' de CHECK n'est pas le meme garde-fou que celui d'omega-scan) —
mais reprend son picker de cibles epinglees (menu Cibles) pour prefiller
`#target-input`.

Le profil CUSTOM (retour utilisateur, 2e round) revele deux champs
facultatifs, sans selecteur de mode supplementaire : un Select de profils
personnels (crees dans l'ecran Profils) et/ou une saisie libre de ports
('80' / '22,443,8080' / '1000-2000', voir
domain/profiles/policies.py::parse_port_spec). Les deux se cumulent
(retour utilisateur, 3e round) — voir _launch_custom()."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Select, Static

from omega_check.application.queries.list_profiles import get_profile, list_profiles
from omega_check.application.queries.list_targets import list_targets
from omega_check.domain.profiles.defaults import SYSTEM_PROFILES
from omega_check.domain.profiles.exceptions import DuplicatePortsError, InvalidPortError
from omega_check.domain.profiles.models import Profile
from omega_check.domain.profiles.policies import normalize_ports, parse_port_spec
from omega_check.interfaces.tui.screens._base import OmegaScreen
from omega_check.interfaces.tui.screens.confirm import ConfirmScreen
from omega_check.interfaces.tui.screens.scan_progress import ScanProgressScreen
from omega_check.shared.i18n import _

if TYPE_CHECKING:
    from omega_check.app.dependency_container import DependencyContainer

_CUSTOM = "CUSTOM"
_FREE_TARGET_ENTRY = "__free_entry__"
_NO_CUSTOM_PROFILE = "__none__"
_NO_CUSTOM_PROFILE_LABEL = _("Profil ou Saisie libre ci-dessous")


class ScanSetupScreen(OmegaScreen):
    """Formulaire de lancement d'un scan."""

    def __init__(self, *, container: DependencyContainer) -> None:
        super().__init__()
        self._container = container

    def compose(self) -> ComposeResult:
        pinned = list_targets(target_repository=self._container.target_repository)
        system_profile_names = (*sorted(SYSTEM_PROFILES), "complet")

        yield Header()
        with Vertical(classes="omega-form-panel"):
            yield Static(_("SCANNER UNE CIBLE"), classes="omega-title")

            yield Static(_("Cible"), classes="omega-subtitle")
            if pinned:
                yield Select(
                    [(_("(saisie libre ci-dessous)"), _FREE_TARGET_ENTRY)]
                    + [(_("* {host}").format(host=t.host), t.host) for t in pinned],
                    value=_FREE_TARGET_ENTRY,
                    id="target-picker",
                )
            yield Input(placeholder=_("ex. 192.168.1.10, example.org"), id="target-input")

            yield Static(_("Profil"), classes="omega-subtitle")
            yield Select(
                [(name, name) for name in system_profile_names] + [(_("Personnalisé (CUSTOM)"), _CUSTOM)],
                value="minimal",
                id="profile-select",
            )

            custom_profiles = {
                name: p for name, p in list_profiles(self._container.profile_repository).items()
                if p.origin == "user"
            }
            yield Select(
                [(_NO_CUSTOM_PROFILE_LABEL, _NO_CUSTOM_PROFILE)]
                + [(name, name) for name in sorted(custom_profiles)],
                value=_NO_CUSTOM_PROFILE,
                id="custom-profile-select",
                classes="omega-hidden",
            )
            yield Input(
                placeholder=_("ex. 80  /  22,443,8080  /  1000-2000"),
                id="custom-ports-input",
                classes="omega-hidden",
            )

            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Lancer"), id="launch", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retour"), id="back")

            yield Static("", id="profile-detail", classes="omega-hint")
        yield Footer()

    def on_mount(self) -> None:
        self._update_profile_detail("minimal")

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "target-picker":
            if event.value != _FREE_TARGET_ENTRY:
                self.query_one("#target-input", Input).value = str(event.value)
            return

        if event.select.id == "profile-select":
            is_custom = event.value == _CUSTOM
            self.query_one("#custom-profile-select", Select).set_class(not is_custom, "omega-hidden")
            self.query_one("#custom-ports-input", Input).set_class(not is_custom, "omega-hidden")
            self._update_profile_detail(None if is_custom else str(event.value))

    def _update_profile_detail(self, profile_name: str | None) -> None:
        detail = self.query_one("#profile-detail", Static)
        if profile_name is None:
            detail.update(_("Profil personnalisé : choisissez un de vos profils ou saisissez "
                            "des ports."))
            return

        profile = get_profile(self._container.profile_repository, profile_name)
        ports_str = ", ".join(str(p) for p in profile.ports)
        detail.update(_("{description}\nPorts ({count}) : {ports_str}").format(description=_(profile.description), count=len(profile.ports), ports_str=ports_str))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return
        if event.button.id != "launch":
            return

        target = self.query_one("#target-input", Input).value.strip()
        if not target:
            self.app.notify(_("Saisissez une cible."), severity="warning")
            return

        profile_name = str(self.query_one("#profile-select", Select).value)

        if profile_name == _CUSTOM:
            self._launch_custom(target)
            return

        if profile_name == "complet":
            self.app.push_screen(
                ConfirmScreen(
                    title=_("PROFIL COMPLET"),
                    message=_("Ce profil est exhaustif (union de tous les profils système) : "
                              "le scan peut être long. Continuer ?"),
                ),
                lambda confirmed: self._launch_if_confirmed(confirmed, target, profile_name),
            )
            return

        self._launch(target=target, profile_name=profile_name)

    def _launch_if_confirmed(self, confirmed: bool | None, target: str, profile_name: str) -> None:
        if confirmed:
            self._launch(target=target, profile_name=profile_name)

    def _launch_custom(self, target: str) -> None:
        """Les deux champs facultatifs se cumulent (retour utilisateur,
        3e round : ne pas s'ecraser l'un l'autre) — l'union est dedupliquee
        silencieusement (normalize_ports), sans rejeter un doublon entre les
        deux sources (contrairement a parse_port_spec seul, qui rejette
        toujours un doublon interne a la saisie libre elle-meme : un
        chevauchement profil/saisie est benin, un doublon tape deux fois
        dans le meme champ reste une erreur de saisie)."""
        ports: list[int] = []
        profile_name: str | None = None
        profile_origin: str | None = None

        custom_profile_name = str(self.query_one("#custom-profile-select", Select).value)
        if custom_profile_name != _NO_CUSTOM_PROFILE:
            profile: Profile = get_profile(self._container.profile_repository, custom_profile_name)
            ports.extend(profile.ports)
            profile_name, profile_origin = profile.name, profile.origin

        ports_raw = self.query_one("#custom-ports-input", Input).value.strip()
        if ports_raw:
            try:
                ports.extend(parse_port_spec(ports_raw))
            except (ValueError, InvalidPortError, DuplicatePortsError) as exc:
                self.app.notify(_("Ports invalides : {exc}").format(exc=exc), severity="warning")
                return

        if not ports:
            self.app.notify(_("Choisissez un profil personnalisé ou saisissez des ports."), severity="warning")
            return

        self._launch(
            target=target, ports=normalize_ports(ports), profile_name=profile_name, profile_origin=profile_origin
        )

    def _launch(
        self,
        *,
        target: str,
        profile_name: str | None = None,
        profile_origin: str | None = None,
        ports: list[int] | None = None,
    ) -> None:
        self.app.push_screen(
            ScanProgressScreen(
                container=self._container,
                target=target,
                profile_name=profile_name,
                profile_origin=profile_origin,
                ports=ports,
            )
        )
