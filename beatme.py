from util.slack_util import SlackUtility

class BeatMe:
    def __init__(self, state, request_ids) -> None:
        self.state = state
        self.slack_util = SlackUtility()
        self.winner_id = request_ids['winner']
        self.winner_name = self.slack_util.get_user_name_by_id(self.winner_id)
        self.loser_id = request_ids['loser']
        self.loser_name = self.slack_util.get_user_name_by_id(self.loser_id)
        self.channel_id = request_ids['channel']

    def execute(self):

        # Get old player data for reference
        old_ranked_state = self.state.get_snapshot()
        
        # # Update state by locally updating the state
        self.state.mock_record_match(self.winner_id, self.loser_id)

        # Calculate changes in score relative to the old
        state_changes = self.state.get_snapshot_diffs(old_ranked_state)
        self.send_match_notifications(state_changes)
    
    def send_match_notifications(self, state_changes):
        self.send_match_anouncement_message(state_changes)
        self.notify_non_participants_of_rank_change(state_changes)

    def send_match_anouncement_message(self, state_changes):
        self.slack_util.client.chat_postMessage(
            channel=self.channel_id,
            blocks=self.get_match_announcement_message(state_changes)
        )


    def get_match_announcement_message(self, state_changes):
        winner_change = state_changes[self.winner_id]
        loser_change = state_changes[self.loser_id]
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"New match: {self.winner_name} vs {self.loser_name} 🏓",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{winner_change['rating']} points were gained and lost during this match",
                    "emoji": True
                },
		    },
            {
                "type": "divider"
            }
        ]
        blocks += self.get_winner_announcement_block(winner_change)
        blocks.append(self.get_loser_announcement_block(loser_change))
        return blocks

    def get_winner_announcement_block(self, stat_changes):
        player = self.state.get_player(self.winner_id)
        title = f"{self.winner_name} won the match 🏆\n"
        elo_section = f"  Elo: {player.rating}\n"
        if stat_changes['rank']:
            rank_section = f"  New rank: {str(player.rank) + ('👑' if player.rank == 1 else '')} ⬆️ {stat_changes['rank']}\n"
        else:
            rank_section = f"  Current rank: {player.rank}\n"
        
        if player.rank == 1 and stat_changes['rank'] > 0:
            self.slack_util.client.chat_postMessage(
                channel=self.channel_id,
                text=f"<!channel> we have a new #1 👑. Congratulations <@{self.winner_id}>!"
                )
            
        return [
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": title,
                                "style": {
                                    "bold": True
                                }
                            },
                            {
                                "type": "text",
                                "text": elo_section + rank_section 
                            }
                        ]
                    }
                ]
            },
            {
                "type": "divider"
            },
        ]

    def get_loser_announcement_block(self, stat_changes):
        player = self.state.get_player(self.loser_id)
        title = f"{self.loser_name} lost the match 😢\n"
        elo_section = f"  Elo: {player.rating}\n"
        if stat_changes['rank']:
            rank_section = f"  New rank: {player.rank} ⬇️ {abs(stat_changes['rank'])}"
        else:
            rank_section = f"  Current rank: {player.rank}"
        
        return {
			"type": "rich_text",
			"elements": [
				{
					"type": "rich_text_section",
					"elements": [
						{
							"type": "text",
							"text": title,
							"style": {
								"bold": True
							}
						},
						{
							"type": "text",
							"text": elo_section + rank_section
						}
					]
				}
			]
		}
    
    def notify_non_participants_of_rank_change(self, state_changes):
        print(state_changes)
        for changes in state_changes.items():
            player_id = changes[0]
            change = changes[1]
            if not change['rating']:
                rank_change = change['rank']
                message = f"Due to the most recent match, your rank has {'decreased' if rank_change < 0 else 'increased'}.\n" \
                f"Your new rank is {self.state.get_player(player_id).rank}."
                self.slack_util.client.chat_postEphemeral(
                    user=player_id,
                    channel=self.channel_id,
                    text=message
                )