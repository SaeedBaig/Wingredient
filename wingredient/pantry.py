from . import db

# insert ingredient into db
# ingredients is a list of tuple (ingredient, quantity, measurement_type)
def insert_ingredient(account, ingredient, quantity, m_type):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            # insert ingredient into db
            #INSERT INTO users (id, level) VALUES (1, 0) ON CONFLICT DO UPDATE SET level = users.level + 1;
            query = "INSERT INTO Pantry (account, ingredient, quantity, measurement_type) VALUES (%s, %s, %s, %s) ON CONFLICT (ingredient, measurement_type) DO UPDATE SET quantity = pantry.quantity + EXCLUDED.quantity;"   # query for ingredient ids
            cursor.execute(query, (account, ingredient, quantity, m_type))
            print(str(get_ingredient_name_from_ids([ingredient])) + str(ingredient) + ":" + str(quantity) + "successfully added")
            conn.commit()


# get list of ingredients from db
# user is an id
def get_ingredients(user_id):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT ingredient, quantity, measurement_type FROM pantry WHERE account = %s;"   # query for ingredient ids
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
            return result

def remove_ingredient(user_id, ingredient_id):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            try:
                query = "DELETE FROM pantry WHERE ingredient = %s AND account = %s;"   # query for ingredient ids
                cursor.execute(query, (ingredient_id,user_id,))
            except Exception as e:
                return e
            conn.commit()
            return True

# takes a list of ingredient ids
# returns a list of ingredient names
def get_ingredient_name_from_ids(ids):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            ingredient_names = []
            for id in ids:
                query = "SELECT name FROM ingredient WHERE id = %s;"   # query for ingredient ids
                cursor.execute(query, (id,))
                result = cursor.fetchone()
                ingredient_names.append(result[0])
            print(ingredient_names)
            return ingredient_names

def get_ingredient_info_from_name(name):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT id FROM ingredient WHERE name = %s;"   # query for ingredient ids
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result[0]