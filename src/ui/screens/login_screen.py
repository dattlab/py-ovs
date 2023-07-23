from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label

from src.db.utils import DBUtils
from src.ui.screens.position_list_screen import PositionListScreen
from src.ui.screens.error_screen import ErrorScreen


class LoginScreen(Screen):

    def __init__(self):
        super().__init__()
        self.username_input = Input(classes="form-input")
        self.passwd_input = Input(classes="form-input", password=True)
        self.db_utils = DBUtils()

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="container-parent"):
            yield Label("[b]LOGIN[/]", classes="screen-title")
            with Container(id="login-form"):
                yield Label("[b]Username:[/]", classes="form-label")
                yield self.username_input

                yield Label("[b]Password:[/]", classes="form-label")
                yield self.passwd_input

                yield Button("Cancel", classes="btn", id="btn_cancel_login")
                yield Button("Login", classes="btn", id="btn_continue_login", variant="primary")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_cancel_login":
            self.app.pop_screen()
        if event.button.id == "btn_continue_login":
            if self.username_input.value != "" and self.passwd_input.value != "":
                if self.db_utils.valid_credential(self.username_input.value, self.passwd_input.value):
                    user_data = self.db_utils.user_collection.find_one({"username": self.username_input.value})
                    self.app.switch_screen(PositionListScreen(user_data["username"], user_data["is_admin"]))
                else:
                    self.app.push_screen(ErrorScreen("Invalid credentials"))
            else:
                self.app.push_screen(ErrorScreen("Input must not be empty"))
