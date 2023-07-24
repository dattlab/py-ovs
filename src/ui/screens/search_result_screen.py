from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Header, Footer, Label, Button

from src.db.utils import DBUtils
from src.helpers import sort_candidate_result, find_voter


class SearchResultScreen(Screen):

    def __init__(self, target_voter_id: int) -> None:
        super().__init__()
        self.target_voter_id = target_voter_id
        self.db_utils = DBUtils()

        self.voter_id_list = self.db_utils.get_all_voters_id()
        self.num_voters = len(self.voter_id_list)

        sort_candidate_result(self.voter_id_list, 0, self.num_voters - 1, False)

        self.voter_in_db = True \
            if find_voter(self.voter_id_list, self.target_voter_id, 0, self.num_voters - 1) != -1 \
            else False

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label("[b]SEARCH RESULTS[/]", classes="screen-title")

        with Container(classes="container-parent"):
            with Container(id="search-result-details"):
                if not self.voter_in_db:
                    yield Label(f"Voter ID {self.target_voter_id} is not found.")
                    yield Button("Back", id="btn-quit-search-result")
                else:
                    user_data = self.db_utils.user_collection.find_one({"voter_id": self.target_voter_id})
                    with Container(classes="user-result-details"):
                        yield Label(
                            str(self.target_voter_id),
                            classes="user-result-details__item",
                            id="user-result-details__id"
                        )
                        yield Label(f"[b]Name:[/] {user_data['name']}", classes="user-result-details__item")
                        yield Label(f"[b]Username:[/] {user_data['username']}", classes="user-result-details__item")

                    with Container(classes="user-voted-candidates"):
                        yield Label("[b]Vote Status[/]", id="user-voted-candidates__title")

                        yield Label("[b]President[/]", classes="user-voted-candidate__item")
                        if self.db_utils.user_already_voted("President", user_data["username"]):
                            pres_candidate_name = self.db_utils.get_user_vote_for_pos(
                                user_data["username"],
                                "President"
                            )
                        else:
                            pres_candidate_name = "N/A [User is not finished casting vote for this position]"
                        yield Label(pres_candidate_name, classes="user-voted-candidate__item")

                        yield Label("[b]Vice President[/]", classes="user-voted-candidate__item")
                        if self.db_utils.user_already_voted("Vice President", user_data["username"]):
                            vpres_candidate_name = self.db_utils.get_user_vote_for_pos(
                                user_data["username"],
                                "Vice President"
                            )
                        else:
                            vpres_candidate_name = "N/A [User is not finished casting vote for this position]"
                        yield Label(vpres_candidate_name, classes="user-voted-candidate__item")

                        yield Label("[b]Secretary[/]", classes="user-voted-candidate__item")
                        if self.db_utils.user_already_voted("Secretary", user_data["username"]):
                            sect_candidate_name = self.db_utils.get_user_vote_for_pos(
                                user_data["username"],
                                "Secretary"
                            )
                        else:
                            sect_candidate_name = "N/A [User is not finished casting vote for this position]"
                        yield Label(sect_candidate_name, classes="user-voted-candidate__item")

                    yield Button("Back", id="btn-quit-search-result")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-quit-search-result":
            self.app.pop_screen()
