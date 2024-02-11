
class RequestWithUserTagException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SelfTagException(RequestWithUserTagException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Error: You can't tag yourself in this request"

class BotTagException(RequestWithUserTagException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Error: You cant tag Elo bot in this request"

class UserNotInChannelException(RequestWithUserTagException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Error: This user is not in the channel where you made this request"

class InvalidUserTagException(RequestWithUserTagException):
    def __init__(self, user_tag,*args: object) -> None:
        super().__init__(*args)
        if user_tag:
            self.message = f"Error: {user_tag} is not a valid way to tag a user. Make sure you prepend a '@' sign and use slacks auto complete to select a valid user."
        else:
            self.message = "Error: no user provided. Please provide a user name as instructed by the slack tooltip."

