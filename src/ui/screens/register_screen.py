from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Input, Label

from src.ui.screens.position_list_screen import PositionListScreen
from src.ui.screens.error_screen import ErrorScreen

from src.db.utils import DBUtils
from src.helpers import inputs_empty


class RegisterScreen(Screen):

    def __init__(self) -> None:
        super().__init__()
        self.name_input = Input(classes="form-input")
        self.username_input = Input(classes="form-input")
        self.passwd_input = Input(classes="form-input", password=True)
        self.confirm_passwd_input = Input(classes="form-input", password=True)

        self.db_utils = DBUtils()

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="container-parent"):
            yield Label("[b]REGISTER[/]", classes="screen-title")
            with Container(id="register-form"):
                yield Label("[b]Name:[/]", classes="form-label")
                yield self.name_input

                yield Label("[b]Username:[/]", classes="form-label")
                yield self.username_input

                yield Label("[b]Password:[/]", classes="form-label")
                yield self.passwd_input

                yield Label("[b]Retype Password:[/]", classes="form-label")
                yield self.confirm_passwd_input

                yield Button("Cancel", classes="btn", id="btn_cancel_register")
                yield Button("Register", classes="btn", id="btn_continue_register", variant="primary")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_cancel_register":
            self.app.pop_screen()
        if event.button.id == "btn_continue_register":
            if not inputs_empty(
                self.name_input.value,
                self.username_input.value,
                self.passwd_input.value,
                self.confirm_passwd_input.value
            ):
                if self.passwd_input.value == self.confirm_passwd_input.value:
                    if not self.db_utils.username_in_db(self.username_input.value):
                        self.db_utils.add_new_user(
                            self.name_input.value,
                            self.username_input.value,
                            self.passwd_input.value
                        )
                        self.app.switch_screen(PositionListScreen(self.username_input.value, False))
                    else:
                        self.app.push_screen(ErrorScreen("Username already taken"))
                else:
                    self.app.push_screen(ErrorScreen("Passwords do not match"))
            else:
                self.app.push_screen(ErrorScreen("Input must not be empty"))
