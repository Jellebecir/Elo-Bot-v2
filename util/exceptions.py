
class BeatMeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SelfTagException(BeatMeException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Error: You can't tag yourself in this request"

class BotTagException(BeatMeException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Error: You cant tag Elo bot in this request"

class UserNotInChannelException(BeatMeException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Error: This user is not in the channel where you made this request"
BeatMeException
class InvalidUserTagException(BeatMeException):
    def __init__(self, user_tag,*args: object) -> None:
        super().__init__(*args)
        if user_tag:
            self.message = f"Error: {user_tag} is not a valid way to tag a user. Make sure you prepend a '@' sign and use slacks auto complete to select a valid user."
        else:
            self.message = "Error: no user provided. Please provide a user name as instructed by the slack tooltip."

