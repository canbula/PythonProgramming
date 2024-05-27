import json
import sqlite3

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Static, Input, DataTable, Label, SelectionList, \
    Button, OptionList
from textual.widgets._data_table import RowKey
from textual.widgets._option_list import Option

from pymetheus.models_pymetheus import Item
from pymetheus.zotero_csl_interop import ITEM_TYPE_NAMES


class ItemsPanel(Static):
    BINDINGS = [
        Binding("ctrl+n", "new_item", "New"),
        Binding("ctrl+d", "duplicate_item", "Duplicate"),
        Binding("ctrl+s", "set_collections", "Collection..."),
        Binding("delete", "delete_item", "Delete"),
    ]

    selected_row_key: reactive[RowKey | None] = reactive(None)

    selected_collection_id: reactive[int | None] = reactive(None)
    search_string: reactive[str] = reactive("")

    class Selected(Message):
        """Sent when the selected item changes"""

        def __init__(self, rowid: str, /):
            super().__init__()
            self.rowid = rowid

    def __init__(self, db_connection: sqlite3.Connection):
        super().__init__()
        self.db_connection = db_connection

    def compose(self) -> ComposeResult:
        with Widget(id="item-menu"):
            yield Input(
                placeholder="Search in all fields...", id="search-item"
            ).data_bind(value=ItemsPanel.search_string)
        yield DataTable(
            id="items-dt",
            cursor_type="row",
            zebra_stripes=True
        )

    @on(Input.Submitted)
    def on_input_submit(self, event: Input.Submitted) -> None:
        event.stop()
        if event.input.id == "search-item":
            self.search_string = event.value

    @on(DataTable.RowSelected)
    def on_select(self, event: DataTable.RowSelected) -> None:
        event.stop()
        self.selected_row_key = event.row_key
        self.post_message(self.Selected(event.row_key.value))

    @on(DataTable.RowHighlighted)
    def on_highlight(self, event: DataTable.RowHighlighted) -> None:
        event.stop()
        self.selected_row_key = event.row_key
        self.post_message(self.Selected(event.row_key.value))

    def on_mount(self) -> None:
        dt = self.query_one("#items-dt", DataTable)
        dt.add_column("Type", key="type")
        dt.add_column("Title", key="title")
        dt.add_column("Creator", key="creator")

        self.watch(self, "selected_collection_id", self.refresh_dt)
        self.watch(self, "search_string", self.refresh_dt)

    def refresh_dt(self) -> None:
        dt = self.query_one("#items-dt", DataTable)
        dt.clear()
        cur = self.db_connection.cursor()
        if self.selected_collection_id is not None:
            items = cur.execute(
                """
                    select item.rowid, item.type, item.field_data, item.creators
                    from collection_entry entry
                    join item on entry.item = item.rowid
                    where entry.collection = ?
                """,
                (self.selected_collection_id,)
            ).fetchall()
        else:
            items = cur.execute("""
                select item.rowid, item.type, item.field_data, item.creators
                from item
            """).fetchall()
        cur.close()

        if self.search_string:
            search_string = self.search_string.casefold()
        else:
            search_string = None
        for i_rowid, i_type, i_fdata, i_creators in items:
            item = Item.from_triplet(
                item_type=i_type,
                field_data=json.loads(i_fdata),
                creators=json.loads(i_creators),
            )
            if (
                    (search_string is None)
                    or item.search(search_string, casefolded=True)
            ):
                dt.add_row(
                    ITEM_TYPE_NAMES[item.type.name],
                    item.field_data.get("title", ""),
                    str(item.get_main_creator() or ""),
                    key=str(i_rowid),
                )
        if dt.rows:
            dt.move_cursor(row=0)
            dt.action_select_cursor()

    def action_duplicate_item(self):
        old_rowid = self.selected_row_key.value
        cur = self.db_connection.cursor()
        i_rowid, i_type, i_fdata, i_creators = cur.execute(
            """
                insert into item (type, field_data, creators)
                select type, field_data, creators
                from item
                where rowid = ?
                limit 1
                returning rowid, type, field_data, creators
            """,
            (old_rowid,)
        ).fetchone()
        self.db_connection.commit()
        dt = self.query_one("#items-dt", DataTable)
        item = Item.from_triplet(
            item_type=i_type,
            field_data=json.loads(i_fdata),
            creators=json.loads(i_creators),
        )
        dt.add_row(
            ITEM_TYPE_NAMES[item.type.name],
            item.field_data.get("title", ""),
            str(item.get_main_creator() or ""),
            key=str(i_rowid),
        )

    def action_delete_item(self):
        if self.selected_row_key is None:
            return

        cur = self.db_connection.cursor()
        cur.execute(
            """
                delete from item
                where rowid = ?
            """,
            (self.selected_row_key.value,)
        )
        self.db_connection.commit()
        cur.close()
        dt = self.query_one("#items-dt", DataTable)
        dt.remove_row(self.selected_row_key)
        self.selected_row_key = None
        dt.action_select_cursor()

    @work
    async def action_set_collections(self):
        await self.app.push_screen_wait(ItemCollectionScreen(
            db_connection=self.db_connection,
            item_rowid=self.selected_row_key.value,
        ))

    @work
    async def action_new_item(self):
        item_type = await self.app.push_screen_wait(
            ItemTypeSelectionScreen()
        )
        if item_type is None:
            return
        cur = self.db_connection.cursor()
        i_rowid, i_type, i_fdata, i_creators = cur.execute(
            """
                insert into item (type, field_data, creators)
                values (?, '{}', '{}')
                returning rowid, type, field_data, creators
            """,
            (item_type,)
        ).fetchone()
        self.db_connection.commit()
        dt = self.query_one("#items-dt", DataTable)
        item = Item.from_triplet(
            item_type=i_type,
            field_data=json.loads(i_fdata),
            creators=json.loads(i_creators),
        )
        dt.add_row(
            ITEM_TYPE_NAMES[item.type.name],
            item.field_data.get("title", ""),
            str(item.get_main_creator() or ""),
            key=str(i_rowid),
        )


class ItemCollectionScreen(ModalScreen):
    def __init__(self, db_connection: sqlite3.Connection, item_rowid: int):
        super().__init__(classes="modal-screen")
        self.db_connection = db_connection
        self.item_rowid = item_rowid

    def compose(self) -> ComposeResult:
        with Widget(classes="modal-dialog"):
            yield Label("Manage collections of item", classes="question")
            with VerticalScroll(classes="checkboxes"):
                cur = self.db_connection.cursor()
                collections = cur.execute("""
                    select rowid, name from collection
                """).fetchall()

                active_collection_rowids = cur.execute(
                    """
                        select c.rowid
                        from collection_entry e
                        join collection c on e.collection = c.rowid
                        where e.item = ?
                    """,
                    (self.item_rowid,)
                ).fetchall()

                yield SelectionList(
                    *[
                        (
                            col_name,
                            col_rowid,
                            (col_rowid,) in active_collection_rowids
                        )
                        for col_rowid, col_name in collections
                    ]
                )
            with Widget(classes="modal-buttons"):
                yield Button("OK", variant="primary", id="ok")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query(SelectionList).first().focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss()
        elif event.button.id == "ok":
            cur = self.db_connection.cursor()
            cur.execute(
                """
                    delete from collection_entry
                    where item = ?
                """,
                (self.item_rowid,)
            )
            for col_rowid in self.query_one(SelectionList).selected:
                cur.execute(
                    """
                        insert into collection_entry (collection, item)
                        values (?, ?)
                    """,
                    (col_rowid, self.item_rowid)
                )
            self.db_connection.commit()
            cur.close()

            self.dismiss()


class ItemTypeSelectionScreen(ModalScreen[str | None]):
    def __init__(self):
        super().__init__(classes="modal-screen")

    selected_type: reactive[str | None] = reactive(None)

    @on(OptionList.OptionHighlighted)
    def highlighted(self, event: OptionList.OptionHighlighted) -> None:
        event.stop()
        self.selected_type = event.option.id

    @on(OptionList.OptionSelected)
    def selected(self, event: OptionList.OptionSelected) -> None:
        event.stop()
        self.selected_type = event.option.id

    def compose(self) -> ComposeResult:
        with Widget(classes="modal-dialog"):
            yield Label("Select the type of item to create", classes="question")
            with VerticalScroll(classes="checkboxes"):
                yield OptionList(
                    *[
                        Option(prompt=human_name, id=codename)
                        for codename, human_name
                        in ITEM_TYPE_NAMES.items()
                    ]
                )
            with Widget(classes="modal-buttons"):
                yield Button("OK", variant="primary", id="ok")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query(OptionList).first().focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "ok":
            self.dismiss(self.selected_type)
