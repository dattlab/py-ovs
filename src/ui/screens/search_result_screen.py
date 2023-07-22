from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Header, Footer, Label, Button


class SearchResultScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label("[b]SEARCH RESULTS[/]", classes="screen-title")

        with Container(classes="container-parent"):
            with Container(id="search-result-details"):
                with Container(classes="user-result-details"):
                    yield Label("123", classes="user-result-details__item", id="user-result-details__id")
                    yield Label("Candidate Name", classes="user-result-details__item")
                    yield Label("username1", classes="user-result-details__item")

                with Container(classes="user-voted-candidates"):
                    yield Label("[b]Vote Status[/]", id="user-voted-candidates__title")

                    yield Label("[b]President[/]", classes="user-voted-candidate__item")
                    # TODO: SHOW "N/A" IF THE USER DIDN'T VOTE YET
                    yield Label("Candidate name", classes="user-voted-candidate__item")

                    yield Label("[b]Vice President[/]", classes="user-voted-candidate__item")
                    # TODO: SHOW "N/A" IF THE USER DIDN'T VOTE YET
                    yield Label("Candidate name", classes="user-voted-candidate__item")

                    yield Label("[b]Secretary[/]", classes="user-voted-candidate__item")
                    # TODO: SHOW "N/A" IF THE USER DIDN'T VOTE YET
                    yield Label("Candidate name", classes="user-voted-candidate__item")

                yield Button("Back", id="btn-quit-search-result")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-quit-search-result":
            self.app.pop_screen()
