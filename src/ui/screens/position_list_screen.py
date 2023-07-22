from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, ScrollableContainer
from textual.widgets import Label, Header, Footer, Button, Input

from src.ui.screens.candidate_list_screen import CandidateListScreen
from src.ui.screens.search_result_screen import SearchResultScreen

class PositionListScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label("[b]ONGOING ELECTION[/]", classes="screen-title")

        with Container(classes="container-parent"):
            with Container(id="position-list"):

                with Container(classes="position-card"):
                    with Container(classes="position-card__info"):
                        yield Label("[b]President[/]")

                        # TODO: CHANGE ITS LABEL TO CANDIDATE NAME
                        # THAT USER VOTED AFTER VOTING
                        yield Label("Num. of Candidates: 5")

                    # TODO: REMOVE IF USER FINISHED VOTING
                    yield Button("View", variant="primary", classes="view-btn", id="pres-view-btn")

                with Container(classes="position-card"):
                    with Container(classes="position-card__info"):
                        yield Label("[b]Vice President[/]")

                        # TODO: CHANGE ITS LABEL TO CANDIDATE NAME
                        # THAT USER VOTED AFTER VOTING
                        yield Label("Num. of Candidates: 5")

                    # TODO: REMOVE IF USER FINISHED VOTING
                    yield Button("View", variant="primary", classes="view-btn", id="vpres-view-btn")

                with Container(classes="position-card"):
                    with Container(classes="position-card__info"):
                        yield Label("[b]Secretary[/]")

                        # TODO: CHANGE ITS LABEL TO CANDIDATE NAME
                        # THAT USER VOTED AFTER VOTING
                        yield Label("Num. of Candidates: 5")

                    # TODO: REMOVE IF USER FINISHED VOTING
                    yield Button("View", variant="primary", classes="view-btn", id="sec-view-btn")

                # TODO: SHOW THIS FOR NON-ADMIN ACCOUNTS
                # yield Label(" ", classes="space")

                # TODO: SHOW THIS FOR ADMIN ACCOUNTS
                with Container(classes="search-box"):
                    yield Button("Check Voter's ID", id="btn-search-box")
                    yield Input(classes="search-box-input")

                yield Button("Logout", variant="error", id="btn-logout")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-logout":
            self.app.pop_screen()
        if event.button.id == "btn-search-box":
            self.app.push_screen(SearchResultScreen())

        # TODO: REFACTOR
        if event.button.id == "pres-view-btn":
            self.app.push_screen(CandidateListScreen("President"))
        if event.button.id == "vpres-view-btn":
            self.app.push_screen(CandidateListScreen("Vice President"))
        if event.button.id == "sec-view-btn":
            self.app.push_screen(CandidateListScreen("Secretary"))
