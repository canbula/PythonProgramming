from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Label, Input, Button


class StandardFieldEditor(ModalScreen[str | None]):
    def __init__(self, initial: str | None, field_name: str):
        super().__init__(classes="modal-screen")
        self.initial = initial
        self.field_name = field_name

    def compose(self) -> ComposeResult:
        with Widget(classes="modal-dialog"):
            yield Label(f"Edit {self.field_name}", classes="question")
            with ScrollableContainer(classes="modal-content"):
                yield Label(f"{self.field_name}:")
                yield Input(
                    value=self.initial,
                    id="new-value",
                    placeholder=self.field_name,
                )
            with Widget(classes="modal-buttons"):
                yield Button("OK", variant="primary", id="ok")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#new-value", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "ok":
            self.dismiss(self.query_one("#new-value", Input).value)
