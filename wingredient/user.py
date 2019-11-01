import os
from hashlib import scrypt
from .routes import login_manager
from . import db

encoding = "ascii"
scrypt_n = 2
scrypt_r = 8
scrypt_p = 1
salt_len = 64

# Using the database:
# with db.pool.getconn() as conn:
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

user_table = {}

class User:
    def __init__(self, username):
        self.username = username
        self.authenticated = False

    def set_password(self, password):
        pw_salt = generate_salt()
        pw_hash = compute_hash(password, pw_salt)

        with db.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                        '''UPDATE Account SET pwhash=%s, pwsalt=%s WHERE username=%s;''', 
                        (pw_hash, pw_salt, self.username)
                )
                conn.commit()

    def authenticate(self, password):
        (req_hash, salt) = self.get_password_hash_and_salt()
        login_hash = compute_hash(password, salt)

        # setting the password regenerates salt and hash
        self.set_password(password)

        # Don't deauthenticate if incorrect
        if login_hash == req_hash:
            self.authenticated = True
        return login_hash == req_hash


    def get_password_hash_and_salt(self):
        with db.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT * FROM Account WHERE username=%s;''', (self.username,))
                user_entry = cursor.fetchone()
                assert(cursor.fetchone() == None) # there should always be exactly one
                return (bytes(user_entry[1]), bytes(user_entry[2]))

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

    with db.pool.getconn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                    '''INSERT INTO Account VALUES (%s, %s, %s, %s);''', 
                    (username, pw_hash, pw_salt, "")
            )
            conn.commit()


@login_manager.user_loader
def load_user(user_id):
    if user_id in user_table:
        # print("user_table hit %s" % (user_id))
        return user_table[user_id]
    else:
        # print("user_table miss %s" % (user_id))
        with db.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT * FROM Account WHERE username=%s;''', (user_id,))
                user_entry = cursor.fetchone()
                if user_entry != None:
                    user = User(user_id)
                    user_table.update({user_id:user}) 
                    return user
                else:
                    return None
