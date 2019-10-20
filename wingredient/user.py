class User:
    def __init__(self):
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True

    def get_id(self):
        # placeholder username
        return 'guest'
