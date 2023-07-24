from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Label, Header, Footer, Button, Input

from src.ui.screens.search_result_screen import SearchResultScreen
from src.ui.components.position_card import PositionCard

from src.db.utils import DBUtils
from src.helpers import sort_candidate_result


class PositionListScreen(Screen):

    def __init__(self, loggedin_username: str, is_user_admin: bool) -> None:
        super().__init__()
        self.loggedin_username = loggedin_username
        self.is_user_admin = is_user_admin

        self.db_utils = DBUtils()

        self.input_voter_id = Input(classes="search-box-input")

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label("[b]ONGOING ELECTION[/]", classes="screen-title")

        with Container(classes="container-parent"):
            with Container(id="position-list"):

                pres_card = PositionCard(
                    "President",
                    self.loggedin_username,
                    self.db_utils.user_already_voted("President", self.loggedin_username)
                )
                pres_card.classes = "position-card"
                yield pres_card

                vpres_card = PositionCard(
                    "Vice President",
                    self.loggedin_username,
                    self.db_utils.user_already_voted("Vice President", self.loggedin_username)
                )
                vpres_card.classes = "position-card"
                yield vpres_card

                sect_card = PositionCard(
                    "Secretary",
                    self.loggedin_username,
                    self.db_utils.user_already_voted("Secretary", self.loggedin_username)
                )
                sect_card.classes = "position-card"
                yield sect_card

                if self.is_user_admin:
                    with Container(classes="search-box"):
                        yield Button("Check Voter's ID", id="btn-search-box")
                        yield self.input_voter_id
                else:
                    yield Label(" ", classes="space")

                yield Button("Logout", variant="error", id="btn-logout")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-logout":
            self.app.pop_screen()
        if event.button.id == "btn-search-box":
            self.app.push_screen(SearchResultScreen(int(self.input_voter_id.value)))

        if event.button.id == "president-view-btn":
            self.app.switch_screen(CandidateListScreen("President", self.loggedin_username, self.is_user_admin))
        if event.button.id == "vice-president-view-btn":
            self.app.switch_screen(CandidateListScreen("Vice President", self.loggedin_username, self.is_user_admin))
        if event.button.id == "secretary-view-btn":
            self.app.switch_screen(CandidateListScreen("Secretary", self.loggedin_username, self.is_user_admin))


class CandidateListScreen(Screen):

    def __init__(self, pos_name: str, username: str, user_is_admin: bool) -> None:
        super().__init__()
        self.pos_name = pos_name
        self.username = username
        self.user_is_admin = user_is_admin

        self.db_utils = DBUtils()
        self.pos_collection = self.db_utils.position_collection.find_one({"position_name": pos_name})
        self.candidate_list = [
            (c["candidate_name"], c["vote_count"])
            for c in self.pos_collection["candidates"]
        ]

        if self.user_is_admin:
            sort_candidate_result(self.candidate_list, 0, len(self.candidate_list) - 1)

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label(f"[b]CANDIDATES FOR\n{self.pos_name.upper()}[/]", classes="screen-title")

        with Container(classes="container-parent"):
            with Container(id="candidate-list"):
                for candidate in self.candidate_list:
                    yield PositionVotingItem(
                        self.pos_name, candidate[0],
                        candidate[1],
                        self.username,
                        self.user_is_admin,
                        classes="candidate-list__item"
                    )

                yield Button("Back", id="btn-back")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.switch_screen(PositionListScreen(self.username, self.user_is_admin))


class PositionVotingItem(Container):

    def __init__(
            self,
            position_name: str,
            candidate_name: str,
            vote_count: int,
            username: str,
            user_is_admin: bool,
            classes: str
    ) -> None:
        super().__init__()

        self.btn_id = "-".join(position_name.lower().split(" ")) \
            if position_name == "Vice President" \
            else position_name
        self.position_name = position_name
        self.candidate_name = candidate_name
        self.vote_count = str(vote_count)
        self.username = username
        self.user_is_admin = user_is_admin

        self.db_utils = DBUtils()

        self.classes = classes

    def compose(self) -> ComposeResult:
        if self.user_is_admin:
            yield Label(self.vote_count, classes="candidate-list__vote-count")
        else:
            yield Button("Vote", id=f"{self.btn_id}-vote-btn", variant="primary")
        yield Label(self.candidate_name, classes="candidate-list__name")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == f"{self.btn_id}-vote-btn":
            self.db_utils.update_vote_history(self.username, self.position_name, self.candidate_name)
            self.app.switch_screen(PositionListScreen(self.username, self.user_is_admin))
