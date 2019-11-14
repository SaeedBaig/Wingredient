"""Module for the Flask app object."""

from flask import Flask, request, redirect, url_for, session, flash
from mako.template import Template
from mako.lookup import TemplateLookup
from mako.runtime import Context
from os.path import abspath
from . import db
from collections import Counter
from flask_login import LoginManager, current_user, login_user, logout_user
import string


BASE_DIR = "wingredient"
TEMPLATE_DIR = abspath(f"{BASE_DIR}/templates")
STATIC_DIR = abspath(f"{BASE_DIR}/static")
LOOKUP = TemplateLookup(directories=[f"{TEMPLATE_DIR}",])

app = Flask("Wingredient", template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# must import User after initialising login manager
from .user import User, create_account, load_user


#################
### HOME PAGE ###
#################
@app.route("/", methods=["GET", "POST"])
def search():
    template = LOOKUP.get_template("search.html")

    # If the user clicked search, initialise the session-variables of all the
    # input fields.
    if request.method == "POST":
        # All of these are str
        # No user input = empty string
        for input_field in {"terms", "num_servings", "min_rating", "max_difficulty", "max_time"}:
            session[input_field] = request.form[input_field]

        # list of str
        # No user input = empty list
        ingredients = request.form['ingredients'].split(',')
        if ingredients == ['']: # no user input
            ingredients = []
        session["ingredients"] = ingredients

        # All of these are bool
        # Unselected = False
        for checkbox in {"pantry_only", "vegan", "vegetarian", "dairy_free", "gluten_free"}:
            session[checkbox] = checkbox in request.form

        return redirect(url_for("results"))

    # This list of ingredients is hard-coded;
    # it should probably be pulled out of the database
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT name FROM ingredient;"   # query for ingredient ids
            cursor.execute(query)
            results = cursor.fetchall()

    print("user: %s, auth: %r" % (current_user.get_id(), current_user.is_authenticated))

    # Make the username a global object (so we don't have to pass it in manually
    # for every single template.render())
    # (Don't worry it gets updated automatically as )
    Context.username = current_user.get_id() if current_user.is_authenticated else None

    return template.render(
        ingredients=[r[0] for r in results]
    )



###########################
### SEARCH RESULTS PAGE ###
###########################
@app.route("/results",)
def results():
    template = LOOKUP.get_template("search-results.html")

    # All the session-variables initialised in search() are available here.
    # E.g.
    print(session["ingredients"])
    print(session["num_servings"])
    print(session["vegan"])
    # Process the variables in whatever way you need to fetch the correct
    # search results

    results = get_search(session["ingredients"])
    if results == -1:
        return template.render(
            titles=""
        )


    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    return template.render(
        titles=[r[1] for r in results],  #name from recipe
        image_paths=[r[4] for r in results],    # imageRef from recipe
        image_alts=[r[3] for r in results],  # set to description from recipe
        ratings=[80 for r in results],
        cooking_times_in_minutes=[r[2] for r in results],                   #time from recipe
        recipe_ids=[r[0] for r in results],
        default='alphabetical'
    )

@app.route("/results", methods=['POST'])
def results_post():
    template = LOOKUP.get_template("search-results.html")

    results = get_search(session["ingredients"])
    if results == -1:
        return template.render(
            titles=""
        )

    sort_option = request.form['sorting_options']
    print(sort_option)
    if sort_option == "rating":
        pass
    elif sort_option == "cooking-time":
        results = sorted(results, key = lambda a : a[2])   # sort results by cooking time

    return template.render(
        titles=[r[1] for r in results],  #name from recipe
        image_paths=[r[4] for r in results],    # imageRef from recipe
        image_alts=[r[3] for r in results],  # set to description from recipe
        ratings=[80 for r in results],
        cooking_times_in_minutes=[r[2] for r in results],                   #time from recipe
        recipe_ids=[r[0] for r in results],
        default=sort_option
    )


def get_search(ingredients):
    temp_tuple = tuple(ingredients) # temporary tuple cast for compatability with cursor.execute()
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT id FROM ingredient WHERE name IN %s;"   # query for ingredient ids
            if not temp_tuple:  # if there's no input into search
                print("INVALID SEARCH")
                return -1

            cursor.execute(query, (temp_tuple,))
            index_result = cursor.fetchall()
            print(index_result)

            search_indexes = []
            for index in index_result:              # extract ingredient id from query result
                search_indexes.append(index[0])
            print(search_indexes)
            search_indexes = tuple(search_indexes)
            if not search_indexes:  #if there's no returned ingredient ids (shouldn't ever happen)
                print("INVALID SEARCH")
                return -1

            #CHANGE TO SPECIFY EXACT COLUMNS
            query = "SELECT recipe, ingredient FROM recipetoingredient WHERE ingredient IN %s;"  # query for matching recipes for the given ingredients
            cursor.execute(query, (search_indexes,))
            matched_recipes = cursor.fetchall()
            print("matched recipes: ")
            print(matched_recipes)

            matched_recipe_indexes = [listing[0] for listing in matched_recipes]

            tuple_matched_recipe_indexes = tuple(matched_recipe_indexes)
            if not tuple_matched_recipe_indexes:    # no matched recipes
                print("INVALID SEARCH")
                return -1

            query = "SELECT recipe, count FROM ingredient_counts WHERE recipe IN %s;"
            cursor.execute(query, (tuple_matched_recipe_indexes,))
            original_recipes = cursor.fetchall()

            original_recipe_counts = {}
            for listing in original_recipes:
                original_recipe_counts[listing[0]] = listing[1]

            print(original_recipe_counts)
            result_counts = Counter(matched_recipe_indexes)
            print(result_counts)

            valid_recipes = []
            for key in original_recipe_counts.keys():
                if result_counts[key] >= original_recipe_counts[key]:
                    valid_recipes.append(key)

            valid_recipes = tuple(valid_recipes)                                  # Counter object of all the valid
            if not valid_recipes:   # no recipes that match
                print("INVALID SEARCH")
                return -1

            query = "SELECT id, name, time, description, imageRef FROM recipe WHERE id IN %s;"
            cursor.execute(query, (valid_recipes,))
            results = cursor.fetchall()
            results = sorted(results, key = lambda a : str(a[1]).lower())   # sort by alphabetical by name
            print("RESULTS:")
            print(results)
            return results

###########################
### SEARCH RECIPE PAGE ####
###########################
@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    template = LOOKUP.get_template("recipe.html")

    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT name, time, difficulty, method, description, imageRef FROM recipe WHERE id = %s;"   #CHANGE TO SPECIFY EXACT COLUMNS
            cursor.execute(query, (recipe_id,))
            results = cursor.fetchone()

            query = "SELECT ingredient FROM recipetoingredient WHERE recipe = %s;"
            cursor.execute(query, (recipe_id,))
            ingredient_index_tuple = tuple([i[0] for i in cursor.fetchall()])   # tuple of ingredient indexes in recipe
            query = "SELECT name FROM ingredient WHERE id in %s;"
            cursor.execute(query, (ingredient_index_tuple,))
            ingredient_names = tuple([i[0] for i in cursor.fetchall()])
            print(ingredient_names)

            query = "SELECT equipment FROM recipetoequipment WHERE recipe = %s;"
            cursor.execute(query, (recipe_id,))
            equipment_index_tuple = tuple([e[0] for e in cursor.fetchall()])    # tuple of equipment indexes in recipe
            if not equipment_index_tuple:
                equipment_names = ()
            else:
                query = "SELECT name FROM equipment WHERE id in %s;"
                cursor.execute(query, (equipment_index_tuple,))
                equipment_names = tuple([e[0] for e in cursor.fetchall()])


    print(results)

    method = str.split(results[3], "|")
    print(method)

    return template.render(
        title=results[0],
        image_path=results[5],
        image_alt=results[4],
        cooking_time_in_minutes=results[1],
        difficulty=results[2],  # can be 'Easy', 'Medium', or 'Hard'
        ingredients=ingredient_names,
        equipment=equipment_names,
        method=method,
        num_likes=128,
    )


##################
### LOGIN PAGE ###
##################
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = load_user(username)

        if user != None and user.check_password(password):
            login_user(user)
            return redirect(url_for("search"))
        else:
            error = "Incorrect username or password."

    template = LOOKUP.get_template("login.html")
    return template.render(error=error)


###################
### SIGNUP PAGE ###
###################
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # don't go to signup page if the user is already logged in
    if not current_user.is_anonymous and current_user.is_authenticated:
        return redirect(url_for("search"))

    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_duplicate = request.form["password_duplicate"]

        # first check that the username has only allowed characters
        # username allowed characters: a-z, A-Z, 0-9, '-', '_'
        #  capitalisation is preserved for a given user,
        #  but duplicate username check is case insensitive

        allowed_chars = set(
            string.ascii_lowercase + string.ascii_uppercase + string.digits + "-" + "_"
        )

        if not (set(username).issubset(allowed_chars)):
            error = "Usernames may contain only letters, numbers, dashes, and underscores."

        # Check that the username is not already in use
        elif load_user(username) != None:
            error = "Username already in use."

        # Check that the two passwords given match
        elif password != password_duplicate:
            error = "Passwords do not match."

        # No error, add the user to the database and sign in
        if error == None:
            create_account(username, password)
            user = load_user(username)
            login_success = user.check_password(password)
            assert(login_success) # this must succeed
            login_user(user)
            return redirect(url_for("search"))

    template = LOOKUP.get_template("signup.html")
    return template.render(error=error)


###################
### LOGOUT PAGE ###
###################
@app.route("/logout")
def logout():
    current_user.logout()
    logout_user()
    # NOTE: redirect to home page instead?
    return redirect(url_for("search"))
