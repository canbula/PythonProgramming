import json
import sqlite3

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Static, DataTable, OptionList, Label, Button
from textual.widgets._option_list import Option

from pymetheus.models_zotero import ItemType
from pymetheus.ui.field_editor_screens.date_field_editor import DateFieldEditor
from pymetheus.ui.field_editor_screens.standard_field_editor import \
    StandardFieldEditor
from pymetheus.ui.field_editor_screens.name_editor import NameEditor
from pymetheus.models_pymetheus import Item, NameData
from pymetheus.zotero_csl_interop import FIELD_NAMES, ITEM_TYPE_NAMES, \
    CREATOR_TYPE_NAMES, is_field_date


class FieldsPanel(Static):
    BINDINGS = [
        Binding("ctrl+n", "add_creator", "Add Creator"),
        Binding("ctrl+e", "edit_field", "Edit"),
        Binding("delete", "clear_field", "Clear"),
    ]

    selected_item_rowid: reactive[int | None] = reactive(None)
    item_object: reactive[Item | None] = reactive(None)

    selected_field_name: reactive[str | None] = reactive(None)
    selected_creator: reactive[tuple[str, int] | None] = reactive(None)

    def __init__(self, db_connection: sqlite3.Connection):
        super().__init__()
        self.db_connection = db_connection

    def compose(self) -> ComposeResult:
        yield DataTable(
            id="fields-dt",
            cursor_type="row",
            zebra_stripes=True,
        )
        yield DataTable(
            id="creators-dt",
            cursor_type="row",
            zebra_stripes=True,
        )

    def on_mount(self) -> None:
        fields = self.query_one("#fields-dt", DataTable)
        fields.add_column("Field", key="field")
        fields.add_column("Value", key="value")

        creators = self.query_one("#creators-dt", DataTable)
        creators.add_column("Contribution", key="type")
        creators.add_column("Name", key="name")

    def watch_selected_item_rowid(self, value: int | None) -> None:
        field_dt = self.query_one("#fields-dt", DataTable)
        field_dt.clear()
        creator_dt = self.query_one("#creators-dt", DataTable)
        creator_dt.clear()
        if value is None:
            return
        cur = self.db_connection.cursor()
        data = cur.execute(
            """
                select type, field_data, creators
                from item
                where rowid = ?
            """,
            (value,)
        ).fetchone()
        cur.close()
        if data is None:
            return
        i_type, i_fdata, i_creators = data
        item = Item.from_triplet(
            item_type=i_type,
            field_data=json.loads(i_fdata),
            creators=json.loads(i_creators),
        )
        self.item_object = item
        field_dt.add_row(
            FIELD_NAMES["itemType"],
            ITEM_TYPE_NAMES[item.type.name],
            key="itemType",
        )
        for any_field in item.type.fields:
            field_dt.add_row(
                FIELD_NAMES[any_field.name],
                item.field_data.get(any_field.name, None),
                key=any_field.base_field
            )
        if field_dt.rows:
            field_dt.move_cursor(row=0)
            field_dt.action_select_cursor()
        for creator_type in item.type.creator_types:
            if creator_type in item.creators:
                for i, creator in enumerate(item.creators[creator_type]):
                    creator_dt.add_row(
                        CREATOR_TYPE_NAMES[creator_type],
                        str(creator),
                        key=f"{creator_type}.{i}"
                    )
        if creator_dt.rows:
            creator_dt.move_cursor(row=0)
            creator_dt.action_select_cursor()

    @on(DataTable.RowHighlighted)
    def on_dt_row_highlight(self, event: DataTable.RowHighlighted):
        event.stop()
        fields = self.query_one("#fields-dt", DataTable)
        creators = self.query_one("#creators-dt", DataTable)
        if event.data_table == fields:
            self.selected_field_name = event.row_key.value
        elif event.data_table == creators:
            creator_type, index = event.row_key.value.split(".")
            self.selected_creator = (creator_type, int(index))

    def update_item_wo_commit(self, item: Item, rowid: int) -> None:
        item_dict = item.as_dict()

        self.db_connection.execute(
            """
                update item
                set type = ?, field_data = ?, creators = ?
                where rowid = ?
            """,
            (
                item_dict["type"],
                json.dumps(item_dict["field_data"], ensure_ascii=False),
                json.dumps(item_dict["creators"], ensure_ascii=False),
                rowid,
            )
        )

    async def action_clear_field(self) -> None:
        if self.selected_item_rowid is None:
            return
        if self.item_object is None:
            return

        fields = self.query_one("#fields-dt", DataTable)
        creators = self.query_one("#creators-dt", DataTable)

        if fields.has_focus:
            if self.selected_field_name == "itemType":
                return
            item: Item = self.item_object
            if self.selected_field_name not in item.field_data:
                await fields.recompose()
                return
            del item.field_data[self.selected_field_name]
            self.update_item_wo_commit(item, self.selected_item_rowid)
            self.db_connection.commit()
            fields.update_cell(self.selected_field_name, "value", None)
            return
        elif creators.has_focus:
            item: Item = self.item_object
            sel_c_type, sel_c_index = self.selected_creator
            if sel_c_type not in item.creators or not item.creators[sel_c_type]:
                await creators.recompose()
                return
            del item.creators[sel_c_type][sel_c_index]
            if not item.creators[sel_c_type]:
                del item.creators[sel_c_type]
            self.update_item_wo_commit(item, self.selected_item_rowid)
            self.db_connection.commit()
            creators.remove_row(f"{sel_c_type}.{sel_c_index}")
            return

    @work
    async def action_edit_field(self) -> None:
        if self.selected_item_rowid is None:
            return
        if self.item_object is None:
            return

        fields = self.query_one("#fields-dt", DataTable)
        creators = self.query_one("#creators-dt", DataTable)

        if fields.has_focus:
            if self.selected_field_name == "itemType":
                return
            item: Item = self.item_object
            initial_value = item.field_data.get(self.selected_field_name, None)
            if is_field_date(self.selected_field_name):
                new_value = await self.app.push_screen_wait(
                    DateFieldEditor(initial_value)
                )
            else:
                new_value = await self.app.push_screen_wait(
                    StandardFieldEditor(
                        initial_value,
                        fields.get_cell(self.selected_field_name, "field")
                    )
                )
            if new_value is None:
                return
            item.field_data[self.selected_field_name] = new_value
            self.update_item_wo_commit(item, self.selected_item_rowid)
            self.db_connection.commit()
            fields.update_cell(
                self.selected_field_name,
                "value",
                new_value
            )
            return
        elif creators.has_focus:
            item: Item = self.item_object
            sel_c_type, sel_c_index = self.selected_creator
            if sel_c_type not in item.creators or not item.creators[sel_c_type]:
                return
            initial_value = item.creators[sel_c_type][sel_c_index]
            new_value = await self.app.push_screen_wait(
                NameEditor(
                    initial_value,
                )
            )
            if new_value is None:
                return
            if new_value.empty():
                del item.creators[sel_c_type][sel_c_index]
                if not item.creators[sel_c_type]:
                    del item.creators[sel_c_type]
                self.update_item_wo_commit(item, self.selected_item_rowid)
                self.db_connection.commit()
                creators.remove_row(f"{sel_c_type}.{sel_c_index}")
                return
            item.creators[sel_c_type][sel_c_index] = new_value
            self.update_item_wo_commit(item, self.selected_item_rowid)
            self.db_connection.commit()
            creators.update_cell(
                f"{sel_c_type}.{sel_c_index}",
                "name",
                str(new_value)
            )
            return

    @work
    async def action_add_creator(self) -> None:
        if self.selected_item_rowid is None:
            return
        if self.item_object is None:
            return

        creators = self.query_one("#creators-dt", DataTable)
        item: Item = self.item_object
        creator_type = await self.app.push_screen_wait(
            CreatorTypeSelectionScreen(item.type)
        )
        if creator_type is None:
            return
        if creator_type not in item.creators:
            item.creators[creator_type] = []
        item.creators[creator_type].append(NameData())
        self.update_item_wo_commit(item, self.selected_item_rowid)
        self.db_connection.commit()
        creators.add_row(
            CREATOR_TYPE_NAMES[creator_type],
            "",
            key=f"{creator_type}.{len(item.creators[creator_type]) - 1}"
        )


class CreatorTypeSelectionScreen(ModalScreen[str | None]):
    def __init__(self, item_type: ItemType):
        super().__init__(classes="modal-screen")
        self.item_type = item_type

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
            yield Label("Select the type of contributor to create",
                        classes="question")
            yield OptionList(
                *[
                    Option(prompt=CREATOR_TYPE_NAMES[codename], id=codename)
                    for codename in self.item_type.creator_types
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
