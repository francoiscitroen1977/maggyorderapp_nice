# app.py
"""Main entry point for the NiceGUI application."""

from nicegui import ui
from frontend import (
    config_page,
    main_page,
    process_configured_matches,
)


@ui.page("/")
def home() -> None:
    """Landing page that links to the main views."""
    ui.link("Configure matching", "/configure")
    ui.link("Pre-process matching", "/preprocess")
    ui.link("Process configured matches", "/process")


@ui.page("/configure")
def configure() -> None:
    config_page.config_page()


@ui.page("/preprocess")
def preprocess() -> None:
    main_page.main_page()


@ui.page("/process")
def process() -> None:
    process_configured_matches.process_configured_matches_page()


ui.run(title="Maggys Order App")
