'''Module for the Flask app object.'''

from flask import Flask, request, redirect, url_for, session
from mako.template import Template
from os.path import abspath

BASE_DIR = 'wingredient'
TEMPLATE_DIR = abspath(f'{BASE_DIR}/templates')
STATIC_DIR = abspath(f'{BASE_DIR}/static')

app = Flask('Wingredient', template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


#################
### HOME PAGE ###
#################
@app.route('/', methods=['GET', 'POST'])
def search():
    template = Template(filename=f'{TEMPLATE_DIR}/search.html')

    # If the user clicked search, initialise the session-variables of all the
    # input fields.
    if request.method == 'POST':
        # All of these are str
        # No user input = empty string
        for input_field in {'terms', 'num_servings', 'min_rating', 'max_difficulty', 'max_time'}:
            session[input_field] = request.form[input_field]

        # list of str
        # No user input = empty list
        session['ingredients'] = request.form.getlist('ingredients')

        # All of these are bool
        # Unselected = False
        for checkbox in {'pantry_only', 'vegan', 'vegetarian', 'dairy_free', 'gluten_free'}:
            session[checkbox] = (checkbox in request.form)

        return redirect(url_for('results'))

    # This list of ingredients is hard-coded;
    # it should probably be pulled out of the database
    return template.render(ingredients=['Milk', 'Flour', 'Sugar', 'Vanilla', 'Eggs'])


###########################
### SEARCH RESULTS PAGE ###
###########################
@app.route('/results')
def results():
    template = Template(filename=f'{TEMPLATE_DIR}/search-results.html')

    # All the session-variables initialised in search() are available here.
    # E.g.
    print(session['ingredients'])
    print(session['num_servings'])
    print(session['vegan'])
    # Process the variables in whatever way you need to fetch the correct
    # search results
    temp_tuple = tuple(session['ingredients']) # temporary tuple cast for compatability with cursor.execute()
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT id FROM ingredient WHERE name IN %s;"   # query for ingredient ids
            cursor.execute(query, (temp_tuple,))
            index_result = cursor.fetchall()
            print(index_result)
            search_indexes = []
            for index in index_result:              # extract ingredient id from query result
                search_indexes.append(index[0])
            print(search_indexes)
            search_indexes = tuple(search_indexes)

            query = "SELECT * FROM recipetoingredient WHERE ingredient IN %s;"  # query for matching recipes for the given ingredients
            cursor.execute(query, (search_indexes,))
            matched_recipes = cursor.fetchall()
            print(matched_recipes)

            matched_recipe_indexes = []
            for listing in matched_recipes:                 # create collection for counter
                matched_recipe_indexes.append(listing[0])

            tuple_matched_recipe_indexes = tuple(matched_recipe_indexes)

            query = "SELECT * from ingredient_counts WHERE recipe IN %s;"
            cursor.execute(query, (tuple_matched_recipe_indexes,))
            original_recipes = cursor.fetchall()

            original_recipe_counts = {}
            for listing in original_recipes:
                original_recipe_counts[listing[0]] = listing[1]

            print(original_recipe_counts)
            result_counts = Counter(matched_recipe_indexes)
            valid_recipes = []
            for key in original_recipe_counts.keys():
                if result_counts[key] == original_recipe_counts[key]:
                    valid_recipes.append(key)

            valid_recipes = tuple(valid_recipes)                                  # Counter object of all the valid

            query = "SELECT * from recipe WHERE id IN %s;"
            cursor.execute(query, (valid_recipes,))
            results = cursor.fetchall()

    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    return template.render(
        titles=['Bowl of Cereal', 'Omellete', 'Stir Fry'],
        image_paths=['static/bowl of cereal.jpg', 'static/omellete.jpg', 'static/stir fry.jpg'],
        image_alts=['bowl of cereal', 'omellete', 'stir fry'],
        ratings=[74, 86, 91],
        cooking_times_in_minutes=[r[2] for r in results],                   #time from recipe
        recipe_ids=[r[0] for r in results],
    )


###########################
### SEARCH RECIPE PAGE ####
###########################
@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    template = Template(filename=f"{TEMPLATE_DIR}/recipe.html")
    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * from recipe WHERE id = %s;"
            cursor.execute(query, (recipe_id,))
            results = cursor.fetchone()

    print(results)
    return template.render(
        title=results[1],
        image_path=results[7],
        image_alt=results[6],
        cooking_time_in_minutes=results[2],
        difficulty=results[3],  # can be 'Easy', 'Medium', or 'Hard'
        ingredients=["Milk", "Cereal"],
        equipment=["Bowl", "Cup", "Microwave"],
        method=results[4],
        num_likes=128,
    )
