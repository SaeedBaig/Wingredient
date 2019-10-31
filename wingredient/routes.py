"""Module for the Flask app object."""

from flask import Flask, request, redirect, url_for, session
from mako.template import Template
from os.path import abspath
from . import db
from collections import Counter
from flask_login import LoginManager, current_user, login_user, logout_user
import string

BASE_DIR = "wingredient"
TEMPLATE_DIR = abspath(f"{BASE_DIR}/templates")
STATIC_DIR = abspath(f"{BASE_DIR}/static")

app = Flask("Wingredient", template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# must import User after initialising login manager
from .user import User

#################
### HOME PAGE ###
#################
@app.route("/", methods=["GET", "POST"])
def search():
    template = Template(filename=f"{TEMPLATE_DIR}/search.html")

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

    return template.render(
        username=current_user.get_id() if current_user.is_authenticated else None,
        ingredients=[r[0] for r in results]
    )



###########################
### SEARCH RESULTS PAGE ###
###########################
@app.route("/results")
def results():
    template = Template(filename=f"{TEMPLATE_DIR}/search-results.html")

    # All the session-variables initialised in search() are available here.
    # E.g.
    print(session["ingredients"])
    print(session["num_servings"])
    print(session["vegan"])
    # Process the variables in whatever way you need to fetch the correct
    # search results
    temp_tuple = tuple(session['ingredients']) # temporary tuple cast for compatability with cursor.execute()
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT id FROM ingredient WHERE name IN %s;"   # query for ingredient ids
            cursor.execute(query, (temp_tuple,))
            index_result = cursor.fetchall()
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
        titles=[r[1] for r in results],  #name from recipe
        image_paths=[r[7] for r in results],    # imageRef from recipe
        image_alts=[r[6] for r in results],  # set to description from recipe
        ratings=[74, 86, 91],
        cooking_times_in_minutes=[r[2] for r in results],                   #time from recipe
        links_to_recipe=['/recipe', '/recipe', '/recipe'],
    )

###########################
### SEARCH RECIPE PAGE ####
###########################
@app.route("/recipe")
def recipe():
    template = Template(filename=f"{TEMPLATE_DIR}/recipe.html")

    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    return template.render(
        title="Bowl of Cereal",
        image_path="static/bowl of cereal.jpg",
        image_alt="bowl of cereal",
        cooking_time_in_minutes=2.5,
        difficulty="Medium",  # can be 'Easy', 'Medium', or 'Hard'
        ingredients=["Milk", "Cereal"],
        equipment=["Bowl", "Cup", "Microwave"],
        method=[
            "Fill bowl with cereal.",
            "Fill cup with milk.",
            "Warm up cup in microwave for 1 minute.",
            "Pour cup of milk into bowl of cereal.",
        ],
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

        # TODO implement actual login check
        # PASSWORD FOR ALL ACCOUNTS
        if password == "guest":
            # flash("Logged in successfully.")
            login_user(User(username))
            return redirect(url_for("search"))
        else:
            error = "Incorrect username or password."

    template = Template(filename=f"{TEMPLATE_DIR}/login.html")
    # TODO
    return template.render(error=error)


###################
### SIGNUP PAGE ###
###################
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_duplicate = request.form["password_duplicate"]

        # first check that the username has only allowed characters
        # username allowed characters: a-z, A-Z, 0-9, '-', '_'
        #  capitalisation is preserved for a given user,
        #  but duplicate username check is case insensitive

        # TODO move this out side function
        allowed_chars = set(
            string.ascii_lowercase + string.ascii_uppercase + string.digits + "-" + "_"
        )

        if not (set(username).issubset(allowed_chars)):
            error = "Usernames may contain only letters, numbers, dashes, and underscores."

        # TODO Check that the username is not already in use
        elif False:
            error = "Username already in use."

        # Check that the two passwords given match
        elif password != password_duplicate:
            error = "Passwords do not match."

        # #TODO No error, add the user to the database and sign in
        if error == None:
            pass

    template = Template(filename=f"{TEMPLATE_DIR}/signup.html")
    # TODO
    return template.render(error=error)


###################
### LOGOUT PAGE ###
###################
@app.route("/logout")
def logout():
    logout_user()
    # NOTE: redirect to home page instead?
    return redirect(url_for("search"))
