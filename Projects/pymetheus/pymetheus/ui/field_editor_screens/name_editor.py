from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Label, Input, Button

from pymetheus.models_pymetheus import NameData


class NameEditor(ModalScreen[NameData | None]):
    def __init__(self, initial: NameData):
        super().__init__(classes="modal-screen")
        self.initial = initial

    def compose(self) -> ComposeResult:
        with Widget(classes="modal-dialog"):
            yield Label("Edit name", classes="question")
            with VerticalScroll(classes="modal-content"):
                yield Label("Dropping:")
                yield Input(
                    value=self.initial.dropping_particle,
                    id="new-dropping-particle",
                    placeholder="Dropping Particle",
                )
                yield Label("Given:")
                yield Input(
                    value=self.initial.given,
                    id="new-given",
                    placeholder="Given Name",
                )
                yield Label("Non-Dropping:")
                yield Input(
                    value=self.initial.non_dropping_particle,
                    id="new-non-dropping-particle",
                    placeholder="Non-Dropping Particle",
                )
                yield Label("Family:")
                yield Input(
                    value=self.initial.family,
                    id="new-family",
                    placeholder="Family Name",
                )
                yield Label("Suffix:")
                yield Input(
                    value=self.initial.suffix,
                    id="new-suffix",
                    placeholder="Suffix",
                )
                yield Label("Literal:")
                yield Input(
                    value=self.initial.literal,
                    id="new-literal",
                    placeholder="Literal",
                )
            with Widget(classes="modal-buttons"):
                yield Button("OK", variant="primary", id="ok")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#new-given", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "ok":
            new = NameData(
                family=self.query_one("#new-family", Input).value,
                given=self.query_one("#new-given", Input).value,
                suffix=self.query_one("#new-suffix", Input).value,
                dropping_particle=(
                    self.query_one("#new-dropping-particle", Input).value
                ),
                non_dropping_particle=(
                    self.query_one("#new-non-dropping-particle", Input).value
                ),
                literal=self.query_one("#new-literal", Input).value,
            )
            self.dismiss(new)
