import os
from hashlib   import scrypt
from .routes   import login_manager
from .dietinfo import allowed_diets
from . import db

encoding = "ascii"
scrypt_n = 2
scrypt_r = 8
scrypt_p = 1
salt_len = 64

# Using the database:
# with db.getconn() as conn:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT rows FROM table")
#         cursor.fetchall()

# password is a string and salt is a bytes object
def compute_hash(password, salt):
    return scrypt(
            bytes(password, encoding),
            salt=salt,
            n=scrypt_n,
            r=scrypt_r,
            p=scrypt_p
    )

def generate_salt():
    return os.urandom(salt_len)

class User:
    def __init__(self, username):
        self.username = username
        self.authenticated = True

    def set_password(self, password):
        pw_salt = generate_salt()
        pw_hash = compute_hash(password, pw_salt)

        with db.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                        '''UPDATE Account SET pwhash=%s, pwsalt=%s WHERE username=%s;''',
                        (pw_hash, pw_salt, self.username)
                )
                conn.commit()

    def check_password(self, password):
        (req_hash, salt) = self.get_password_hash_and_salt()
        login_hash = compute_hash(password, salt)

        # setting the password regenerates salt and hash
        self.set_password(password)

        return login_hash == req_hash


    def get_password_hash_and_salt(self):
        with db.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT * FROM Account WHERE username=%s;''', (self.username,))
                user_entry = cursor.fetchone()
                assert(cursor.fetchone() == None) # there should always be exactly one
                return (bytes(user_entry[1]), bytes(user_entry[2]))

    def get_diets(self):
        with db.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''SELECT * FROM DietInfo WHERE account=%s;''',
                    (self.username,)
                )
                dietinfo_list = cursor.fetchall()
                return list(map(lambda t: t[1], dietinfo_list))

    def set_diets(self, diets):
        assert(set(diets).issubset(set(allowed_diets)))
        with db.getconn() as conn:
            with conn.cursor() as cursor:
                # Clear all the user's diet info from the table
                cursor.execute(
                    '''DELETE FROM DietInfo WHERE account=%s;''',
                    (self.username,)
                )
                # Add all the requested diets
                for diet in diets:
                    cursor.execute(
                        '''INSERT INTO DietInfo VALUES (%s, %s);''',
                        (self.username, diet)
                    )
                conn.commit()

    def add_fav(self, recipe_id):
        if not self.is_fav(recipe_id):
            with db.getconn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        '''INSERT INTO Favourites VALUES (%s, %s);''',
                        (self.username, recipe_id)
                    )
                    conn.commit()

    def del_fav(self, recipe_id):
        with db.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''DELETE FROM Favourites WHERE account=%s AND recipe=%s;''',
                    (self.username, recipe_id)
                )
                conn.commit()

    def is_fav(self, recipe_id):
        with db.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''SELECT * FROM Favourites WHERE account=%s AND recipe=%s;''',
                    (self.username, recipe_id)
                )
                return cursor.fetchone() != None

    def add_like(self, recipe_id):
        if not self.is_like(recipe_id):
            with db.getconn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        '''INSERT INTO Recipe_Votes VALUES (%s, %s, %s);''',
                        (self.username, recipe_id, True)
                    )
                    conn.commit()

    def del_vote(self, recipe_id):
        with db.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''DELETE FROM Recipe_Votes WHERE account=%s AND recipe=%s;''',
                    (self.username, recipe_id)
                )
                conn.commit()

    def is_like(self, recipe_id):
        with db.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''SELECT is_like FROM Recipe_Votes WHERE account=%s AND recipe=%s;''',
                    (self.username, recipe_id)
                )
                record = cursor.fetchone()
                return record and record[0]

    def add_dislike(self, recipe_id):
        if not self.is_dislike(recipe_id):
            with db.getconn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        '''INSERT INTO Recipe_Votes VALUES (%s, %s, %s);''',
                        (self.username, recipe_id, False)
                    )
                    conn.commit()

    def is_dislike(self, recipe_id):
        with db.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''SELECT is_like FROM Recipe_Votes WHERE account=%s AND recipe=%s;''',
                    (self.username, recipe_id)
                )
                record = cursor.fetchone()
                return record and not record[0]

    def logout(self):
        self.authenticated = False

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


def create_account(username, password):
    pw_salt = generate_salt()
    pw_hash = compute_hash(password, pw_salt)

    with db.getconn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                    '''INSERT INTO Account VALUES (%s, %s, %s, %s);''',
                    (username, pw_hash, pw_salt, "")
            )
            conn.commit()


@login_manager.user_loader
def load_user(user_id):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT * FROM Account WHERE username=%s;''', (user_id,))
            user_entry = cursor.fetchone()
            if user_entry != None:
                user = User(user_id)
                return user
            else:
                return None
