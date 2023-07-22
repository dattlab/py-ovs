from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Header, Footer, Label, Button


class CandidateListScreen(Screen):

    def __init__(self, poll_name):
        super().__init__()
        self.poll_name = poll_name

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label(f"[b]CANDIDATES FOR\n{self.poll_name.upper()}[/]", classes="screen-title")

        with Container(classes="container-parent"):
            with Container(id="candidate-list"):
                with Container(classes="candidate-list__item"):
                    # TODO: SHOW THIS INSTEAD OF BUTTON FOR ADMIN ACCOUNTS
                    yield Label("123", classes="candidate-list__vote-count")
                    # yield Button("Vote", classes="vote-btn", variant="primary")
                    yield Label("Candidate 1", classes="candidate-list__name")

                with Container(classes="candidate-list__item"):
                    # TODO: SHOW THIS INSTEAD OF BUTTON FOR ADMIN ACCOUNTS
                    yield Label("123", classes="candidate-list__vote-count")
                    # yield Button("Vote", classes="vote-btn", variant="primary")
                    yield Label("Candidate 2", classes="candidate-list__name")

                with Container(classes="candidate-list__item"):
                    # TODO: SHOW THIS INSTEAD OF BUTTON FOR ADMIN ACCOUNTS
                    yield Label("123", classes="candidate-list__vote-count")
                    # yield Button("Vote", classes="vote-btn", variant="primary")
                    yield Label("Candidate 3", classes="candidate-list__name")

                with Container(classes="candidate-list__item"):
                    # TODO: SHOW THIS INSTEAD OF BUTTON FOR ADMIN ACCOUNTS
                    yield Label("123", classes="candidate-list__vote-count")
                    # yield Button("Vote", classes="vote-btn", variant="primary")
                    yield Label("Candidate 4", classes="candidate-list__name")

                with Container(classes="candidate-list__item"):
                    # TODO: SHOW THIS INSTEAD OF BUTTON FOR ADMIN ACCOUNTS
                    yield Label("123", classes="candidate-list__vote-count")
                    # yield Button("Vote", classes="vote-btn", variant="primary")
                    yield Label("Candidate 5", classes="candidate-list__name")

                yield Button("Back", id="btn-back")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()
