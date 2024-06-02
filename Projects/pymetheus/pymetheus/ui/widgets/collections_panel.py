import json
import sqlite3

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Tree, Label, Input, Button
from textual.widgets._tree import TreeNode

from pymetheus.citeproc_serializer import serialize_item
from pymetheus.models_pymetheus import Item


class CollectionsPanel(Tree):
    BINDINGS = [
        Binding("ctrl+n", "create_coll", "Create"),
        Binding("ctrl+s", "export_coll", "Export"),
        Binding("ctrl+r", "rename_coll", "Rename"),
        Binding("delete", "delete_coll", "Delete"),
    ]

    selected_node: reactive[TreeNode | None] = reactive(None)

    class Selected(Message):
        """Sent when the selected collection changes"""

        def __init__(self, rowid: int | None, /):
            super().__init__()
            self.rowid = rowid

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        event.stop()
        self.selected_node = event.node
        self.post_message(self.Selected(event.node.data))

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        event.stop()
        self.selected_node = event.node
        self.post_message(self.Selected(event.node.data))

    @on(Tree.NodeCollapsed)
    def on_collapsed(self, event: Tree.NodeCollapsed) -> None:
        event.stop()
        if event.node == self.root:
            self.root.expand()
            self.select_node(self.root)
            self.post_message(self.Selected(self.root.data))

    def __init__(self, db_connection: sqlite3.Connection):
        super().__init__(label="My Library", data=None, id="collections-tree")
        self.db_connection = db_connection

    def on_mount(self):
        cur = self.db_connection.cursor()
        cols = cur.execute("""
            select rowid, name from collection
        """).fetchall()
        for rowid, col_name in cols:
            self.root.add_leaf(col_name, data=rowid)
        cur.close()
        self.root.expand()
        self.select_node(self.root)
        self.post_message(self.Selected(self.root.data))

    def action_delete_coll(self):
        node: TreeNode = self.selected_node
        if node.data is None:
            return

        cur = self.db_connection.cursor()
        cur.execute(
            """
                delete from collection
                where rowid = ?
            """,
            (node.data,)
        )
        self.db_connection.commit()
        cur.close()
        node.remove()
        self.action_select_cursor()

    @work
    async def action_rename_coll(self):
        node: TreeNode = self.selected_node
        if not node or not node.data:
            return

        new = await self.app.push_screen_wait(
            RenameCollectionScreen(str(node.label))
        )
        if new is None:
            return

        cur = self.db_connection.cursor()
        cur.execute(
            """
                update collection
                set name = ?
                where rowid = ?
            """,
            (new, node.data)
        )
        self.db_connection.commit()
        node.label = new

    @work
    async def action_create_coll(self):
        cur = self.db_connection.cursor()
        counter = 1
        while True:
            new_name = f"Collection {counter}"
            if not cur.execute(
                    """
                    select 1
                    from collection
                    where name = ?
                """,
                    (new_name,)
            ).fetchone():
                break
            counter += 1

        rowid, = cur.execute(
            """
                insert into collection (name)
                values (?)
                returning rowid
            """,
            (new_name,)
        ).fetchone()
        self.db_connection.commit()
        self.root.add_leaf(new_name, data=rowid)

    @work
    async def action_export_coll(self):
        node: TreeNode = self.selected_node
        if not node or not node.data:
            return

        ids_to_items = {}
        cur = self.db_connection.cursor()
        items = cur.execute(
            """
                select item.rowid, item.type, item.field_data, item.creators
                from item
                join collection_entry entry on item.rowid = entry.item
                where entry.collection = ?
            """,
            (node.data,)
        ).fetchall()
        cur.close()
        for i_rowid, i_type, i_fdata, i_creators in items:
            item = Item.from_triplet(
                item_type=i_type,
                field_data=json.loads(i_fdata),
                creators=json.loads(i_creators)
            )
            item_bibid = item.try_to_generate_id()
            if not item_bibid:
                item_bibid = f"item{i_rowid}"
            if item_bibid in ids_to_items:
                counter = 1
                while True:
                    new_bibid = f"{item_bibid}_{counter}"
                    if new_bibid not in ids_to_items:
                        item_bibid = new_bibid
                        break
                    counter += 1
            ids_to_items[item_bibid] = item
        serialized_items = []
        for bibid, item in ids_to_items.items():
            item_dict = serialize_item(item)
            item_dict["id"] = bibid
            serialized_items.append(item_dict)
        with open(f"{node.label}.json", "w") as f:
            json.dump(serialized_items, f, indent=4, ensure_ascii=False)
        self.app.notify(
            f"Collection {node.label} exported to {node.label}.json",
            timeout=10.0,
        )


class RenameCollectionScreen(ModalScreen[str | None]):
    def __init__(self, initial_name: str):
        super().__init__(classes="modal-screen")

        self.initial_name = initial_name

    def compose(self) -> ComposeResult:
        with Widget(classes="modal-dialog"):
            yield Label("New name for collection", classes="question")
            with ScrollableContainer(classes="modal-content"):
                yield Label("New name:")
                yield Input(
                    value=self.initial_name,
                    id="new-name",
                    placeholder="Collection name"
                )
            with Widget(classes="modal-buttons"):
                yield Button("OK", variant="primary", id="ok")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#new-name", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "ok":
            new_name = self.query_one("#new-name", Input).value
            self.dismiss(new_name)
