from .routes import login_manager

class User:
    def __init__(self):
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True

    def get_id(self):
        # placeholder username
        return 'guest'
        

@login_manaer.user_loader
def load_user(user_id):
    # TODO Create user object from unicode user_id
    return None
