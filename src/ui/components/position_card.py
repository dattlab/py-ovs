from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Button

from src.db.utils import DBUtils


class PositionCard(Container):

    def __init__(self, position_name: str, username: str, user_already_voted: bool) -> None:
        super().__init__()
        self.position_name = position_name
        self.btn_id = "-".join(position_name.lower().split(" ")) \
            if position_name == "Vice President" \
            else position_name.lower()

        self.db_utils = DBUtils()

        self.pos_data = self.db_utils.position_collection.find_one({ "position_name": position_name })
        self.num_candidates = len(self.pos_data["candidates"])

        self.username = username
        self.user_already_voted = user_already_voted

    def compose(self) -> ComposeResult:
        with Container(classes="position-card__info"):
            yield Label(f"[b]{self.position_name}[/]")

            if self.user_already_voted:
                yield Label(
                    f"Candidate Voted: {self.db_utils.get_user_vote_for_pos(self.username, self.position_name)}"
                )
            else:
                yield Label(f"Num. of Candidates: {self.num_candidates}")

        if not self.user_already_voted:
            yield Button("View", variant="primary", classes="view-btn", id=f"{self.btn_id}-view-btn")
