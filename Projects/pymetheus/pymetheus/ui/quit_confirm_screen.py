from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Label, Button


class QuitConfirmScreen(ModalScreen):
    def __init__(self):
        super().__init__(classes="modal-screen")

    def compose(self) -> ComposeResult:
        with Widget(classes="modal-dialog"):
            yield Label("Are you sure you want to quit?", classes="question")
            yield Widget(classes="modal-content")
            with Widget(classes="modal-buttons"):
                yield Button("Quit", variant="error", id="quit")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.dismiss()
