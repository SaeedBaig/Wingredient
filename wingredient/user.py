from .routes import login_manager


class User:
    def __init__(self, username):
        self.username = username
        self.authenticated = True

    # user_id is just the username
    def get_id(self):
        return self.username

    @property
    def is_authenticated(self):
        return self.authenticated

    # All users are active
    @property
    def is_active(self):
        return True

    # Any logged in user is not anonymous
    @property
    def is_anonymous(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    # TODO make this actually check user rather than just create
    # new authenticated user instances
    insecure_user = User(user_id)
    insecure_user.authenticated = True
    return insecure_user
