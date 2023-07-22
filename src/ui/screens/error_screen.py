from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Grid
from textual.widgets import Label, Button


class ErrorScreen(ModalScreen):

    def __init__(self, error_msg) -> None:
        super().__init__()
        self.error_msg = error_msg

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.error_msg, id="question"),
            Button("Retry", variant="error", id="btn-retry"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-retry":
            self.app.pop_screen()