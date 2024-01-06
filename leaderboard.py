from texttable import Texttable
from util.slack_util import SlackUtility

class Leaderboard:
    def __init__(self, state, channel_id) -> None:
        self.table = Texttable()
        self.table_header = ["Rank", "Name", "Wins", "Losses", "Rating", "Shift"]
        self.slack_util = SlackUtility()
        self.players = [player[1] for player in state.get_snapshot().items()]
        self.channel_id = channel_id

    def execute(self):
        self.create_leaderboard_table()
        result = "```" + self.table.draw().replace("=", "") + "```"
        self.slack_util.client.chat_postMessage(
            channel=self.channel_id,
            text=result
        )

    def create_leaderboard_table(self):
        self.set_table_styling()
        self.set_table_content()

    def set_table_styling(self):
        self.table.set_cols_align(["l" for i in range(6)])
        self.table.set_cols_valign(["m" for i in range(6)])
        self.table.set_deco(Texttable.HEADER)
        self.table.set_header_align(["l" for i in range(6)])

    def set_table_content(self):
        self.table.header(self.table_header)
        for player in self.players:
            player_name = self.slack_util.get_user_name_by_id(player.id)
            player_rank = self.get_player_rank_display(player.rank)
            row = [player_rank, player_name, player.wins, player.losses, player.rating, player.change]
            self.table.add_row(row)

    def get_player_rank_display(self, player_rank):
        if player_rank - 1 < 3:
            return ['🥇', '🥈', '🥉'][player_rank - 1]
        else:
            return player_rank
