from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Input, Label

from src.ui.screens.position_list_screen import PositionListScreen


class RegisterScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="container-parent"):
            yield Label("[b]REGISTER[/]", classes="screen-title")
            with Container(id="register-form"):
                yield Label("[b]Name:[/]", classes="form-label")
                yield Input(classes="form-input")

                yield Label("[b]Username:[/]", classes="form-label")
                yield Input(classes="form-input")

                yield Label("[b]Password:[/]", classes="form-label")
                yield Input(classes="form-input", password=True)

                yield Label("[b]Retype Password:[/]", classes="form-label")
                yield Input(classes="form-input", password=True)

                yield Button("Cancel", classes="btn", id="btn_cancel_register")
                yield Button("Register", classes="btn", id="btn_continue_register", variant="primary")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_cancel_register":
            self.app.pop_screen()
        if event.button.id == "btn_continue_register":
            self.app.switch_screen(PositionListScreen())
