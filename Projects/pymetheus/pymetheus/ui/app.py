import argparse
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Header, Footer

from pymetheus.db import get_connection_from_args
from pymetheus.ui.quit_confirm_screen import QuitConfirmScreen
from pymetheus.ui.widgets.collections_panel import CollectionsPanel
from pymetheus.ui.widgets.fields_panel import FieldsPanel
from pymetheus.ui.widgets.items_panel import ItemsPanel


class PymetheusApp(App):
    TITLE = "pymetheus"

    CSS_PATH = "style/app.tcss"
    BINDINGS = [
        Binding("ctrl+c", "check_quit", show=False, priority=True),
        Binding("ctrl+q", "quit", show=False, priority=True),
        Binding("ctrl+z", "suspend_process", show=False, priority=True),
        Binding(
            "f5", "recompose", "Refresh",
            show=False,
        ),
        Binding("f1", "app.focus('collections-tree')", "Collections"),
        Binding("f2", "app.focus('items-dt')", "Items"),
        Binding("f3", "app.focus('fields-dt')", "Data"),
        Binding("f4", "app.focus('creators-dt')", "Contributors"),
    ]
    ENABLE_COMMAND_PALETTE = False

    selected_collection_id: reactive[str | None] = reactive(None)
    selected_item_rowid: reactive[int | None] = reactive(None)

    @on(CollectionsPanel.Selected)
    def on_collection_selected(self, event: CollectionsPanel.Selected):
        self.selected_collection_id = event.rowid

    @on(ItemsPanel.Selected)
    def on_item_selected(self, event: ItemsPanel.Selected):
        if event.rowid is not None:
            self.selected_item_rowid = int(event.rowid)
        else:
            self.selected_item_rowid = None

    def __init__(self):
        super().__init__()

        main_argparser = argparse.ArgumentParser()

        main_argparser.add_argument(
            "-L", "--library",
            help="Path to the library to use",
            type=Path,
            metavar="LIBRARY_PATH",
        )

        parsed_args = main_argparser.parse_args()
        self.db_path, self.db_connection = get_connection_from_args(parsed_args)
        self.sub_title = self.db_path

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="panel-container"):
            yield CollectionsPanel(self.db_connection)
            yield ItemsPanel(self.db_connection) \
                .data_bind(PymetheusApp.selected_collection_id)
            yield FieldsPanel(self.db_connection) \
                .data_bind(PymetheusApp.selected_item_rowid)
        yield Footer()

    def on_mount(self) -> None:
        footer = self.query_one(Footer)
        footer.upper_case_keys = True
        footer.compact = True
        footer.ctrl_to_caret = True

    async def action_recompose(self) -> None:
        await self.recompose()

    def action_check_quit(self) -> None:
        self.push_screen(QuitConfirmScreen())
