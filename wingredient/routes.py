"""Module for the Flask app object."""

from flask import Flask, request, redirect, url_for, session, flash
from mako.template import Template
from mako.lookup import TemplateLookup
from mako.runtime import Context
from os.path import abspath
from werkzeug.datastructures import ImmutableMultiDict 
from . import db
from .pantry import *
from collections import Counter
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
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
        url_args = {}
        for input_field in ("terms", "num_servings", "min_rating", "max_difficulty", "max_time"):
            if request.form[input_field]:
                url_args[input_field] = request.form[input_field]

        # list of str
        # No user input = empty list
        ingredients = request.form['ingredients'].split(',')
        if ingredients != ['']: # no user input
            url_args["ingredients"] = ingredients

        if request.form.get("pantry_only"):
            url_args["pantry_only"] = True

        dietary_tags = 0
        for i, checkbox in enumerate(("vegetarian", "vegan", "gluten_free", "dairy_free")):
            if request.form.get(checkbox):
                dietary_tags |= 1 << i

        if dietary_tags:
            url_args["dietary_tags"] = dietary_tags

        return redirect(url_for(
            "results",
            **url_args,
        ))

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
    print(request.args.getlist("ingredients"))
    print(request.args.get("num_servings"))
    # Process the variables in whatever way you need to fetch the correct
    # search results

    _results = get_search()
    if _results == -1:
        return template.render(
            titles=""
        )


    return template.render(
        titles=[r[1] for r in _results],  # name from recipe
        image_paths=[r[4] for r in _results],    # imageRef from recipe
        image_alts=[r[3] for r in _results],  # set to description from recipe
        ratings=[80 for r in _results],
        cooking_times_in_minutes=[r[2] for r in _results],                   #time from recipe
        recipe_ids=[r[0] for r in _results],
        default='alphabetical'
    )

@app.route("/results", methods=['POST'])
def results_post():
    template = LOOKUP.get_template("search-results.html")

    _results = get_search()
    if _results == -1:
        return template.render(
            titles=""
        )

    sort_option = request.form['sorting_options']
    print(sort_option)
    if sort_option == "rating":
        pass
    elif sort_option == "cooking-time":
        _results = sorted(_results, key = lambda a : a[2])   # sort results by cooking time

    return template.render(
        titles=[r[1] for r in _results],  #name from recipe
        image_paths=[r[4] for r in _results],    # imageRef from recipe
        image_alts=[r[3] for r in _results],  # set to description from recipe
        ratings=[80 for r in _results],
        cooking_times_in_minutes=[r[2] for r in _results],                   #time from recipe
        recipe_ids=[r[0] for r in _results],
        default=sort_option
    )


def get_search():
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            whereclauses = []
            query_args = {}

            ingredients = request.args.getlist("ingredients")
            if ingredients:
                whereclauses.append("i.name IN %(ingredients)s")
                query_args["ingredients"] = tuple(ingredients)
                missing_ingredient_count_expr = (
                    "ic.compulsory_ingredient_count - count(rtoi.recipe)"
                )
            else:
                missing_ingredient_count_expr = "ic.compulsory_ingredient_count"

            dietary_tags = request.args.get("dietary_tags", default=0, type=int)
            if dietary_tags:
                whereclauses.append(
                    "r.dietary_tags & %(dietary_tags)s::bit(4) = %(dietary_tags)s::bit(4)"
                )
                query_args["dietary_tags"] = dietary_tags

            max_time = request.args.get("max_time", default=0, type=int)
            if max_time:
                whereclauses.append("r.time <= %(max_time)s")
                query_args["max_time"] = max_time

            num_servings = request.args.get("num_servings", default=0, type=int)
            if num_servings:
                whereclauses.append("r.serving >= %(num_servings)s")
                query_args["num_servings"] = num_servings

            if whereclauses:
                whereclause = "WHERE " + " AND ".join(whereclauses)
            else:
                whereclause = ""
            query = f"""
                SELECT
                  r.id,
                  r.name,
                  r.time,
                  r.description,
                  r.imageref,
                  r.serving,
                  ic.compulsory_ingredient_count,
                  (
                    {missing_ingredient_count_expr}
                  ) AS missing_ingredient_count
                FROM recipetoingredient rtoi
                JOIN ingredient i ON rtoi.ingredient = i.id
                JOIN ingredient_counts ic on rtoi.recipe = ic.recipe
                JOIN recipe r ON rtoi.recipe = r.id
                {whereclause}
                GROUP BY
                  r.id,
                  ic.compulsory_ingredient_count
                ORDER BY
                  missing_ingredient_count,
                  r.name
            """
            cursor.execute(query, query_args)
            return cursor.fetchall()

###########################
### SEARCH RECIPE PAGE ####
###########################
@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    template = LOOKUP.get_template("recipe.html")

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
    if current_user.is_authenticated and not current_user.is_anonymous:
        current_user.logout()
        logout_user()
    return redirect(url_for("search"))

###################
### PANTRY PAGE ###
###################
@app.route("/pantry", methods=["GET", "POST"])
@login_required
def pantry():
    # template = Template(filename=f"{TEMPLATE_DIR}/pantry.html")
    template = LOOKUP.get_template("pantry.html")
    if request.method == "POST":
        if 'pantry-add' in request.form:
            ingredient = request.form['ingredients']
            ingredient_index = get_ingredient_info_from_name(ingredient)
            quantity = request.form['quantity']
            if quantity == '':
                quantity = 1
            insert_ingredient(current_user.get_id(), ingredient_index, quantity)
        else:
            print("fuk")
            remove_id = request.form["pantry-delete"]
            print(remove_id)
            remove_ingredient(current_user.get_id(), remove_id)

    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT name, measurement_type FROM ingredient ORDER BY name;"   # query for ingredient ids
            cursor.execute(query)
            all_ingredients_results = cursor.fetchall()

    results = get_ingredients(current_user.get_id())



    ingredient_ids = [r[0] for r in results]
    quantities = [r[1] for r in results]
    print(ingredient_ids)
    if (ingredient_ids):
        ingredient_info = get_ingredient_info_from_ids(ingredient_ids)

    print(ingredient_info)
    return template.render(
        error="none",
        all_ingredients = [r[0] for r in all_ingredients_results],
        ingredients=[r[0] for r in ingredient_info],
        ingredient_ids = ingredient_ids,
        quantities=quantities,
        pantry_types=[r[1] for r in ingredient_info],
        m_types=[r[1] for r in all_ingredients_results],
        username=current_user.get_id() if current_user.is_authenticated else None
    )


#########################
### USER PROFILE PAGE ###
#########################
@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    template = LOOKUP.get_template("profile.html")

    if request.method == "POST":
        pass

    return template.render()
