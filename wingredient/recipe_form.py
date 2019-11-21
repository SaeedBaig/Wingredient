from werkzeug import secure_filename
from . import db

def upload_recipe(username, name, cooking_time, difficulty, serving_size, cooking_notes, description, cuisine_tags, dietary_tags, imageRef, method, ingredients, ingredient_quantities, equipment):
    ingredient_ids = get_ingredient_ids_from_names(ingredients)
    equipment_ids = get_equipment_ids_from_names(equipment)
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            recipe_id = gen_id()
            query = "INSERT INTO Recipe (id, name, time, difficulty, serving, notes, description, cuisine_tags, dietary_tags, imageRef, method) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::bit(4), %s, %s)" 
            cursor.execute(query, (recipe_id, name, cooking_time, difficulty, serving_size, cooking_notes, description, cuisine_tags, dietary_tags, imageRef, method))
            conn.commit()
    upload_ingredients(recipe_id, ingredient_ids, ingredient_quantities)
    upload_equipment(recipe_id, equipment_ids)
    get_recipe()


def gen_id():
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT id FROM Recipe ORDER BY id DESC LIMIT 1;"
            cursor.execute(query)
            result = cursor.fetchone()
            return (int(result[0]) + 1)

def get_ingredient_ids_from_names(ingredients):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT id FROM Ingredient WHERE name in %s;"
            cursor.execute(query, (tuple(ingredients),))
            result = cursor.fetchall()
    return [r[0] for r in result]

def get_equipment_ids_from_names(equipment):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT id FROM Equipment WHERE name in %s;"
            cursor.execute(query, (tuple(equipment),))
            result = cursor.fetchall()
    return [r[0] for r in result]

def upload_ingredients(recipe_id, ingredients, quantities):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            for i in range(len(ingredients)):
                query = "INSERT INTO RecipeToIngredient (recipe, ingredient, quantity) VALUES (%s, %s, %s)" 
                cursor.execute(query, (recipe_id, ingredients[i], quantities[i]))
            conn.commit()

def upload_equipment(recipe_id, equipment):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            for e in equipment:
                query = "INSERT INTO RecipeToEquipment (recipe, equipment) VALUES (%s, %s)" 
                cursor.execute(query, (recipe_id, e))
            conn.commit()


def get_recipe():
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Recipe;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)

def get_all_equipment():
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT name FROM Equipment;"
            cursor.execute(query)
            result = cursor.fetchall()
            return [r[0] for r in result]
         