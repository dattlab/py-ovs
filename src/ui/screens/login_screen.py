from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label

from src.ui.screens.position_list_screen import PositionListScreen
from src.ui.screens.error_screen import ErrorScreen


class LoginScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="container-parent"):
            yield Label("[b]LOGIN[/]", classes="screen-title")
            with Container(id="login-form"):
                yield Label("[b]Username:[/]", classes="form-label")
                yield Input(classes="form-input")

                yield Label("[b]Password:[/]", classes="form-label")
                yield Input(classes="form-input", password=True)

                yield Button("Cancel", classes="btn", id="btn_cancel_login")
                yield Button("Login", classes="btn", id="btn_continue_login", variant="primary")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_cancel_login":
            self.app.pop_screen()
        if event.button.id == "btn_continue_login":
            self.app.switch_screen(PositionListScreen())
            # self.app.push_screen(ErrorScreen("Pangit"))
