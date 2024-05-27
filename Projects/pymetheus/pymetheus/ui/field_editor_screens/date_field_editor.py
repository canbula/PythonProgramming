import datetime

from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Label, Input, Button


class DateFieldEditor(ModalScreen[str | None]):
    def __init__(self, initial: str | None):
        super().__init__(classes="modal-screen")
        if initial:
            self.y, self.m, self.d = tuple(int(x) for x in initial.split("-"))
        else:
            today = datetime.date.today()
            self.y, self.m, self.d = today.year, today.month, today.day

    def compose(self) -> ComposeResult:
        with Widget(classes="modal-dialog"):
            yield Label("Edit date", classes="question")
            with ScrollableContainer(classes="modal-content"):
                yield Label("Date:")
                yield Input(
                    value=f"{self.y:04d}-{self.m:02d}-{self.d:02d}",
                    id="new-date",
                    placeholder="YYYY-MM-DD",
                )
            with Widget(classes="modal-buttons"):
                yield Button("OK", variant="primary", id="ok")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#new-date", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "ok":
            try:
                y, m, d = self.query_one("#new-date", Input).value.split("-")
                y, m, d = int(y), int(m), int(d)
            except ValueError as e:
                self.app.notify(
                    "Invalid date format. Use YYYY-MM-DD.",
                    severity="error",
                    timeout=5.0
                )
                self.dismiss(None)
                return
            try:
                datetime.date(year=y, month=m, day=d)
            except ValueError as e:
                self.app.notify(str(e), severity="error", timeout=5.0)
                self.dismiss(None)
                return
            self.dismiss(f"{y:04d}-{m:02d}-{d:02d}")
