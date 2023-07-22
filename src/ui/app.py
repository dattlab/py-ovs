from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Button, Header, Footer

from src.ui.screens.login_screen import LoginScreen
from src.ui.screens.register_screen import RegisterScreen


class VotingSystem(App):

    CSS_PATH = "app.css"

    BINDINGS = [
        Binding("ctrl+c", "quit", "Exit", show=True, priority=True)
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="container-parent"):
            with Container():
                yield Button("Login", classes="btn", id="btn_to_login_screen", variant="primary")
                yield Button("Register", classes="btn", id="btn_to_register_screen", variant="primary")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_to_login_screen":
            self.push_screen(LoginScreen())
        if event.button.id == "btn_to_register_screen":
            self.push_screen(RegisterScreen())
