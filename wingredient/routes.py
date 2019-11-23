"""Module for the Flask app object."""
import uuid

import psycopg2.extras
from flask import Flask, request, redirect, url_for, session, flash
from mako.template import Template
from mako.lookup import TemplateLookup
from mako.runtime import Context
from os.path import abspath

import os

from werkzeug.datastructures import ImmutableMultiDict
from . import db
from .pantry import *
from .recipe_form import *
from collections import Counter
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import string

from .dietinfo import allowed_diets
from .rating import get_num_likes, get_num_dislikes, get_rating
from fractions import Fraction


BASE_DIR = "wingredient"
TEMPLATE_DIR = abspath(f"{BASE_DIR}/templates")
STATIC_DIR = abspath(f"{BASE_DIR}/static")
LOOKUP = TemplateLookup(directories=[f"{TEMPLATE_DIR}",])

app = Flask("Wingredient", template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# must import User after initialising login manager
from .user import User, create_account, load_user, pw_min_len

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
        fields_to_copy = (
            "terms", "fuzzyness", "num_servings", "min_rating", "max_difficulty", "max_time"
        )
        for input_field in fields_to_copy:
            if request.form[input_field]:
                url_args[input_field] = request.form[input_field]

        # list of str
        # No user input = empty list
        ingredients = request.form['ingredients'].split(',')
        if ingredients != ['']: # no user input
            url_args["ingredients"] = ingredients

        if request.form.get("pantry_only"):
            url_args["pantry_only"] = True

        if request.form.get("favs_only"):
            url_args["favs_only"] = True

        dietary_tags = 0
        for i, checkbox in enumerate(allowed_diets):
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

    current_diets = current_user.get_diets() if current_user.is_authenticated else []

    return template.render(
        ingredients=[r[0] for r in results],
        allowed_diets = allowed_diets,
        current_diets = current_diets
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
        titles=[r[1] for r in _results],  #name from recipe
        image_paths=[r[4] for r in _results],    # imageRef from recipe
        image_alts=[r[3] for r in _results],  # set to description from recipe
        ratings=[r[8] if r[8] is None else int(r[8] * 100) for r in _results],
        cooking_times_in_minutes=[r[2] for r in _results],                   #time from recipe
        recipe_ids=[r[0] for r in _results],
        difficulties=[r[6] for r in _results],
        dietary_tags=[r[7] for r in _results],
        missing_ingredients=[r[9] for r in _results],
        matched_ingredients=[r[10] for r in _results],
        default="relevance"
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
        _results.sort(key=lambda a: a[8] or 0, reverse=True)
    elif sort_option == "cooking-time":
        _results.sort(key=lambda a: a[2])
    elif sort_option == "alphabetical":
        _results.sort(key=lambda a: a[1].lower())
    elif sort_option == "relevance":
        _results.sort(key=lambda a: a[11], reverse=True)

    return template.render(
        titles=[r[1] for r in _results],  #name from recipe
        image_paths=[r[4] for r in _results],    # imageRef from recipe
        image_alts=[r[3] for r in _results],  # set to description from recipe
        ratings=[r[8] if r[8] is None else int(r[8] * 100) for r in _results],
        cooking_times_in_minutes=[r[2] for r in _results],                   #time from recipe
        recipe_ids=[r[0] for r in _results],
        difficulties=[r[6] for r in _results],
        dietary_tags=[r[7] for r in _results],
        missing_ingredients=[r[9] for r in _results],
        matched_ingredients=[r[10] for r in _results],
        default=sort_option
    )


def get_search():
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            where_clauses = []
            extra_joins = []
            having_clauses = []
            query_args = {}
            relevance_score_expr = "0"

            # Create the expressions and arguments to match the search filters

            # Filter favourites
            if request.args.get("favs_only"):
                extra_joins.append(
                    "JOIN Favourites f ON f.account = %(cur_user_id)s AND f.recipe = r.id"
                )
                query_args["cur_user_id"] = current_user.get_id()

            ingredients = request.args.getlist("ingredients")
            use_pantry = request.args.get("pantry_only")
            cur_ingredients_tname = None
            if ingredients or use_pantry:
                cur_ingredients_tname = "current_ingredients_" + str(
                    uuid.uuid4()
                ).replace("-", "_")
                cursor.execute(
                    f"""
                    CREATE TEMPORARY TABLE {cur_ingredients_tname} (
                        name text PRIMARY KEY,
                        quantity integer
                    )
                    """
                )
                if ingredients:
                    psycopg2.extras.execute_values(
                        cursor,
                        f"INSERT INTO {cur_ingredients_tname} (name) VALUES %s",
                        [(ingredient,) for ingredient in ingredients]
                    )
                if use_pantry:
                    cursor.execute(
                        f"""
                        INSERT INTO {cur_ingredients_tname}
                          SELECT i.name, p.quantity
                          FROM pantry p
                          JOIN ingredient i on p.ingredient = i.id
                        ON CONFLICT DO NOTHING
                        """
                    )
                conn.commit()
                extra_joins.extend((
                    f"JOIN recipetoingredient rtoi ON rtoi.recipe = r.id",
                    f"JOIN ingredient i ON i.id = rtoi.ingredient",
                    f"""
                    LEFT OUTER JOIN {cur_ingredients_tname} ci ON
                      ci.name = i.name
                      AND (ci.quantity IS NULL OR ci.quantity >= rtoi.quantity)
                      AND NOT rtoi.optional
                    """,
                    f"""
                    LEFT OUTER JOIN {cur_ingredients_tname} ci_optional ON
                      ci_optional.name = i.name
                      AND (ci_optional.quantity IS NULL OR ci_optional.quantity >= rtoi.quantity)
                    """,
                ))
                query_args["ingredients"] = tuple(ingredients)
                missing_ingredient_count_expr = (
                    "ic.compulsory_ingredient_count - sum((ci.name IS NOT NULL)::int)"
                )
                matched_ingredient_count_expr = "sum((ci_optional.name IS NOT NULL)::int)"
                relevance_score_expr += f" + {matched_ingredient_count_expr}"
            else:
                missing_ingredient_count_expr = "ic.compulsory_ingredient_count"
                matched_ingredient_count_expr = "0"

            dietary_tags = request.args.get("dietary_tags", default=0, type=int)
            if dietary_tags:
                where_clauses.append(
                    "r.dietary_tags & %(dietary_tags)s::bit(4) = %(dietary_tags)s::bit(4)"
                )
                query_args["dietary_tags"] = dietary_tags

            max_time = request.args.get("max_time", default=0, type=int)
            if max_time:
                where_clauses.append("r.time <= %(max_time)s")
                query_args["max_time"] = max_time

            num_servings = request.args.get("num_servings", default=0, type=int)
            if num_servings:
                where_clauses.append("r.serving >= %(num_servings)s")
                query_args["num_servings"] = num_servings

            min_rating = request.args.get("min_rating", default=0, type=int)
            if min_rating:
                where_clauses.append("(rr.rating ISNULL OR rr.rating >= %(min_rating)s)")
                query_args["min_rating"] = min_rating / 100

            search_terms = request.args.get("terms", default="", type=str)
            if search_terms:
                search_term_pattern = "(" + "|".join(search_terms.lower().split(" ")) + ")"
                matched_search_terms_expr = "term_matches.count"
                extra_joins.append(
                    """
                    NATURAL JOIN LATERAL (
                      SELECT count(matches) AS count
                      FROM regexp_matches(
                        concat(r.name, r.description, r.method), %(search_term_pattern)s, 'ig'
                      ) matches
                    ) term_matches
                    """
                )
                query_args["search_term_pattern"] = search_term_pattern
                where_clauses.append(
                    "term_matches.count > 0"
                )
                relevance_score_expr += f" + {matched_search_terms_expr}"
            else:
                matched_search_terms_expr = "1"

            fuzzyness = request.args.get("fuzzyness", default=None, type=int)
            if fuzzyness is not None:
                having_clauses.append(f"{missing_ingredient_count_expr} <= %(fuzzyness)s")
                query_args["fuzzyness"] = fuzzyness

            # Format the expressions into a single "WHERE <expr>" string
            extra_joinclause = " ".join(extra_joins)
            if where_clauses:
                where_clause = "WHERE " + " AND ".join(where_clauses)
            else:
                where_clause = ""
            if having_clauses:
                having_clause = "HAVING " + " AND ".join(having_clauses)
            else:
                having_clause = ""

            query = f"""
                SELECT
                  r.id,
                  r.name,
                  r.time,
                  r.description,
                  r.imageref,
                  r.serving,
                  r.difficulty,
                  r.dietary_tags,
                  rr.rating,
                  {missing_ingredient_count_expr} AS missing_compulsory_ingredient_count,
                  {matched_ingredient_count_expr} AS matched_ingredient_count,
                  {matched_search_terms_expr} AS matched_search_terms_count,
                  {relevance_score_expr} AS relevance_score
                FROM recipe r
                JOIN ingredient_counts ic ON r.id = ic.recipe
                LEFT OUTER JOIN recipe_rating rr ON r.id = rr.recipe
                {extra_joinclause}
                {where_clause}
                GROUP BY
                  r.id,
                  ic.compulsory_ingredient_count,
                  rr.rating,
                  matched_search_terms_count
                {having_clause}
                ORDER BY
                  relevance_score DESC,
                  rr.rating DESC NULLS LAST,
                  r.name ASC
            """
            print(query)
            cursor.execute(query, query_args)
            ret = cursor.fetchall()

            if cur_ingredients_tname is not None:
                # Drop the temporary table
                cursor.execute(f"DROP TABLE {cur_ingredients_tname} CASCADE")

            return ret

###########################
### SEARCH RECIPE PAGE ####
###########################

def format_quantity(quantity):
    # Convert quantity into fraction 0.25 = 1/4
    quantity = str(Fraction(quantity))
    return quantity

def format_measurement(measurement):
    if measurement == 'Count': measurement = ''
    return measurement

def format_optional(optional):
    optional_check = ""
    if optional:
        optional_check = " (optional)"
    return optional_check

@app.route("/recipe/<int:recipe_id>", methods=["GET"])
def recipe(recipe_id):
    template = LOOKUP.get_template("recipe.html")
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT name, time, difficulty, method, description, imageRef FROM recipe WHERE id = %s;"   #CHANGE TO SPECIFY EXACT COLUMNS
            cursor.execute(query, (recipe_id,))
            results = cursor.fetchone()

            #query = "SELECT ingredient FROM recipetoingredient WHERE recipe = %s;"
            #cursor.execute(query, (recipe_id,))
            #ingredient_index_tuple = tuple([i[0] for i in cursor.fetchall()])   # tuple of ingredient indexes in recipe


# SELECT i.name, rti.quantity, rti.r_quantity, (CASE WHEN (rti.r_quantity IS NULL) THEN rti.quantity ELSE rti.r_quantity END) as modified_quantity FROM recipetoingredient rti, ingredient i where i.id = rti.ingredient AND rti.recipe = 1;
            query = "SELECT (COALESCE(rti.r_quantity, rti.quantity)) as quantity, (COALESCE(rti.r_measurement_type::text, i.measurement_type::text)) as measurement_type, i.name, rti.optional FROM recipetoingredient rti, ingredient i where i.id = rti.ingredient AND rti.recipe = %s;"
            #query = "SELECT rti.quantity, i.measurement_type, rti.r_quantity, rti.r_measurement_type, i.name FROM ingredient i, recipetoingredient rti WHERE i.id = rti.ingredient AND rti.recipe = %s;"
            cursor.execute(query, (recipe_id,))
            #ir = for row in cursor.fetchall()
            ires = cursor.fetchall()
            ires = ([(format_quantity(i[0]), format_measurement(i[1]), i[2], format_optional(i[3])) for i in ires])
            ingredient_results = list(map(" ".join,ires))

            query = "SELECT i.name FROM Pantry p, Ingredient i WHERE p.ingredient = i.id AND p.account = %s;"
            cursor.execute(query, (current_user.get_id(),))
            pantry_res = cursor.fetchall()
            pantry_results = [r[0] for r in pantry_res]
           # ingredient_results = list(map(" ".join, ([(str(i[0]), i[1], i[2]) for i in ires])))
            #for x in ingredient_results:
            #    print(x[0], x[1])

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

    is_favourite = current_user.is_fav(recipe_id) if current_user.is_authenticated else False
    is_like      = current_user.is_like(recipe_id) if current_user.is_authenticated else False
    is_dislike   = current_user.is_dislike(recipe_id) if current_user.is_authenticated else False

    return template.render(
        title=results[0],
        image_path=results[5],
        image_alt=results[4],
        cooking_time_in_minutes=results[1],
        difficulty=results[2],  # can be 'Easy', 'Medium', or 'Hard'
        ingredients=ingredient_results,
        equipment=equipment_names,
        method=method,
        num_likes=get_num_likes(recipe_id),
        num_dislikes=get_num_dislikes(recipe_id),
        rating=get_rating(recipe_id),
        is_favourite=is_favourite,
        is_like=is_like,
        is_dislike=is_dislike,
        recipe_id=recipe_id,
        pantry=pantry_results
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

        # The checks that the username has only allowed characters, that the
        # password is at least pw_min_len characters long, and that the 2
        # passwords match is all done on the front end.

        #  capitalisation is preserved for a given user,
        #  but duplicate username check is case insensitive

        # Check that the username is not already in use
        if load_user(username) != None:
            error = "Username already in use."

        # No error, add the user to the database and sign in
        if error == None:
            create_account(username, password)
            user = load_user(username)
            login_success = user.check_password(password)
            assert(login_success) # this must succeed
            login_user(user)
            return redirect(url_for("search"))

    template = LOOKUP.get_template("signup.html")
    return template.render(error=error, pw_min_len=pw_min_len)


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
### Shopping List ###
###################
#@app.route("/shoppinglist")
#def shoppinglist():
#    with db.getconn() as conn:
#        with conn.cursor() as cursor:
#            #query = "SELECT name, time, difficulty, method, description, imageRef FROM recipe WHERE id = 20;"
#
#            ##CHANGE TO SPECIFY EXACT COLUMNS
#            #cursor.execute(query)
#            #results = cursor.fetchone()
#
#    template = LOOKUP.get_template("shopping-list.html")
#    return template.render()
#
#
#@app.route("/addtoshoppinglist")
#def shoppinglist():
#    with db.getconn() as conn:
#        with conn.cursor() as cursor:
#            #query = "SELECT name, time, difficulty, method, description, imageRef FROM recipe WHERE id = 20;"
#
#            ##CHANGE TO SPECIFY EXACT COLUMNS
#            #cursor.execute(query)
#            #results = cursor.fetchone()
#
#    # NOTE: redirect to home page instead?
#    return redirect(url_for("search"))
def format_m_type(val):
    return "(" + val + ")"

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
            ingredient = request.form['ingredient_input']
            ingredient = ingredient.split(' ')[0]
            ingredient_index = get_ingredient_info_from_name(ingredient)
            quantity = request.form['quantity']
            if quantity == '':
                quantity = 1
            insert_ingredient(current_user.get_id(), ingredient_index, quantity)
        else:
            remove_id = request.form["pantry-delete"]
            print(remove_id)
            remove_ingredient(current_user.get_id(), remove_id)

    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT name, measurement_type FROM ingredient ORDER BY name;"   # query for ingredient ids
            cursor.execute(query)
            all_ingredients_results = cursor.fetchall()

    ires = ([(i[0], format_m_type(i[1])) for i in all_ingredients_results])


    ingredient_results = list(map(" ".join,ires))
    results = get_ingredients(current_user.get_id())



    ingredient_ids = [r[0] for r in results]
    quantities = [r[1] for r in results]
    print(ingredient_ids)
    if (ingredient_ids):
        ingredient_info = get_ingredient_info_from_ids(ingredient_ids)
    else:
        ingredient_info = []

    return template.render(
        error="none",
        all_ingredients = ingredient_results,
        ingredients=[r[0] for r in ingredient_info],
        ingredient_ids = ingredient_ids,
        quantities=quantities,
        pantry_types=[r[1] for r in ingredient_info],
        username=current_user.get_id() if current_user.is_authenticated else None
    )


#########################
### USER PROFILE PAGE ###
#########################
@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    template = LOOKUP.get_template("profile.html")

    password_msg = None
    dietary_msg = None

    allowed_forms = ["dietary_form", "password_form"]
    open_forms    = []

    if request.method == "POST":
        whichform = request.form["whichform"]
        if whichform == "dietary_form":
            diets = set(request.form.keys()).intersection(set(allowed_diets))
            current_user.set_diets(diets)
            dietary_msg = "Diets set successfully."

        elif whichform == "password_form":
            password_error         = None
            current_password       = request.form["current_password"]
            new_password           = request.form["new_password"]
            new_password_duplicate = request.form["new_password_duplicate"]

            if not current_user.check_password(current_password):
                password_error = "Current password incorrect."

            # Check that the password is long enough
            elif len(new_password) < pw_min_len:
                password_error = "Password must be at least %d characters long." % (pw_min_len)

            if new_password != new_password_duplicate:
                password_error = "New passwords do not match."



            if password_error == None:
                current_user.set_password(new_password)
                password_msg = "Password changed successfully."
            else:
                password_msg = password_error
        else:
            pass

        # Remember which collapsible forms are open
        for form_name in allowed_forms:
            if request.form.get(form_name) != None:
                open_forms.append(form_name)

    current_diets = current_user.get_diets()

    return template.render(
        open_forms    = open_forms,
        allowed_diets = allowed_diets,
        current_diets = current_diets,
        password_msg  = password_msg,
        dietary_msg   = dietary_msg
   )

@app.route("/recipe-form", methods=["GET", "POST"])
def recipe_form():
    template = LOOKUP.get_template("recipe-form.html")
    if request.method == "POST":

        count = request.form['count']
        method = []
        for i in range(1, int(count)+1):
            if ('field' + str(i)) in request.form:
                method.append(request.form['field' + str(i)])
        recipe_method = "|".join(method)

        session['recipe_name'] = request.form['recipe_name']
        session['recipe_time'] = request.form['cooking_time']
        session['recipe_difficulty'] = request.form['difficulty']
        session['recipe_serving'] = request.form['serving_size']
        session['recipe_notes'] = request.form['cooking_notes']
        session['recipe_description'] = request.form['description']
        session['recipe_equipment'] = request.form['equipment']
        session['recipe_method'] = recipe_method
        ingredient_count = request.form['count-ingredient']
        recipe_ingredients = []
        ingredient_quantities = []
        ingredient_checks = []
        session['cuisine_tags'] = request.form['cuisine_tags']
        print(session['cuisine_tags'])

        for i in range(1, int(ingredient_count)+1):
            if ('ingredient' + str(i)) in request.form:
                recipe_ingredients.append(request.form['ingredient' + str(i)])
            if ('ingredient-quantity' + str(i)) in request.form:
                ingredient_quantities.append(request.form['ingredient-quantity' + str(i)])
            if ('ingredient_check' + str(i)) in request.form:   # optionality checkbox is ticked
                ingredient_checks.append(True)
            else:
                ingredient_checks.append(False)
        session['recipe_ingredients'] = recipe_ingredients
        session['ingredient_quantities'] = ingredient_quantities
        session['ingredient_checks'] = ingredient_checks
        print(ingredient_quantities)
        print(ingredient_checks)
        dietary_tags = 0b0000
        vegan_check = "vegan_check" in request.form
        vegetarian_check = "vegetarian_check" in request.form
        gluten_check = "gluten_check" in request.form
        dairy_check = "dairy_check" in request.form
        if vegan_check:
            dietary_tags = dietary_tags | 0b0011
        if vegetarian_check:
            dietary_tags = dietary_tags | 0b0001
        if gluten_check:
            dietary_tags = dietary_tags | 0b0100
        if dairy_check:
            dietary_tags = dietary_tags | 0b1000

        session['dietary_tags'] = dietary_tags


        return redirect(url_for('recipe_confirm'))


    with db.getconn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT name, measurement_type FROM ingredient ORDER BY name;"   # query for ingredient ids
            cursor.execute(query)
            all_ingredients_results = cursor.fetchall()
    equipment = get_all_equipment()
    #print(equipment)
    return template.render(
        error="none",
        all_ingredients=[r[0] for r in all_ingredients_results],
        m_types=[r[1] for r in all_ingredients_results],
        equipment=get_all_equipment(),
        username=current_user.get_id() if current_user.is_authenticated else None
    )

@app.route("/confirm-recipe", methods=["POST", "GET"])
def recipe_confirm():
    template = LOOKUP.get_template("recipe-confirm.html")
    recipe_name = session.get("recipe_name", None)
    recipe_time=session.get("recipe_time", None)
    recipe_difficulty=session.get("recipe_difficulty", None)
    recipe_serving=session.get("recipe_serving", None)
    recipe_notes=session.get("recipe_notes", None)
    recipe_description=session.get("recipe_description", None)
    recipe_equipment=session.get("recipe_equipment", None)
    recipe_ingredients=session.get("recipe_ingredients", None)
    ingredient_quantities=session.get("ingredient_quantities", None)
    recipe_method=session.get("recipe_method", None)
    dietary_tags = session.get("dietary_tags", None)
    ingredient_checks = session.get("ingredient_checks", None)
    cuisine_tags = session.get("cuisine_tags", None)
    recipe_equipment = recipe_equipment.split(',')
    vegetarian_check = 0b0001 & dietary_tags
    vegan_check = 0b0011 & dietary_tags
    gluten_check = 0b0100 & dietary_tags
    dairy_check = 0b1000 & dietary_tags
    display_method = recipe_method.split('|')
    if request.method == "POST":
        # take file input
        if 'recipe_image' in request.files:
            image = request.files['recipe_image']
            if image.filename != '':
                print(image.filename)
                filepath = 'wingredient/static/images/recipe_images'
                image.save(os.path.join(filepath, image.filename))
        print("file uploaded")
        path = "static/images/recipe_images/"
        recipe_imageRef = path + image.filename
        print(recipe_imageRef)
        #submit recipe into database
        recipe_id = upload_recipe(current_user.get_id(), recipe_name, recipe_time, recipe_difficulty, recipe_serving, recipe_notes, recipe_description, cuisine_tags, dietary_tags, recipe_imageRef, recipe_method, recipe_ingredients, ingredient_quantities, ingredient_checks, recipe_equipment)
        return redirect('recipe/' + str(recipe_id))


    print(session.get("recipe_ingredients", None))

    print(session.get("recipe_name", None))

    return template.render(
        recipe_name=recipe_name,
        recipe_time=recipe_time,
        recipe_difficulty=recipe_difficulty,
        recipe_serving=recipe_serving,
        recipe_notes=recipe_notes,
        recipe_description=recipe_description,
        recipe_equipment=recipe_equipment,
        recipe_ingredients=recipe_ingredients,
        ingredient_quantities=ingredient_quantities,
        recipe_method=display_method,
        vegetarian=vegetarian_check,
        vegan=vegan_check,
        gluten_free=gluten_check,
        dairy_free=dairy_check,
        cuisine_tags = cuisine_tags
    #   error="none",
    #   username=current_user.get_id() if current_user.is_authenticated else None
    )


@app.route('/recipe/<int:recipe_id>/like', methods=['POST', 'DELETE'])
@app.route('/recipe/<int:recipe_id>/dislike', methods=['POST', 'DELETE'])
def recipe_vote(recipe_id):
    if not current_user.is_authenticated:
        return 'You must log in first', 403

    if request.method == "POST":
        # Add like or dislike
        if request.path.endswith('/like'):
            current_user.add_like(recipe_id)
        elif request.path.endswith('/dislike'):
            current_user.add_dislike(recipe_id)
        else:
            # Should never happen
            return 'Invalid path', 400
    elif request.method == "DELETE":
        # Remove like or dislike
        current_user.del_vote(recipe_id)
    return ''


@app.route('/recipe/<int:recipe_id>/favourite', methods=['POST', 'DELETE'])
def recipe_favourite(recipe_id):
    if not current_user.is_authenticated:
        return 'You must log in first', 403

    if request.method == "POST":
        current_user.add_fav(recipe_id)
    elif request.method == "DELETE":
        current_user.del_fav(recipe_id)
    return ''
