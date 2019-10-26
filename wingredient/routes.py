'''Module for the Flask app object.'''

from flask import Flask, request, redirect, url_for, session
from mako.template import Template
from os.path import abspath
from flask_login import LoginManager

BASE_DIR = 'wingredient'
TEMPLATE_DIR = abspath(f'{BASE_DIR}/templates')
STATIC_DIR = abspath(f'{BASE_DIR}/static')

app = Flask('Wingredient', template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)


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

    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    return template.render(
        titles=['Bowl of Cereal', 'Omellete', 'Stir Fry'],
        image_paths=['static/bowl of cereal.jpg', 'static/omellete.jpg', 'static/stir fry.jpg'],
        image_alts=['bowl of cereal', 'omellete', 'stir fry'],
        ratings=[74, 86, 91],
        cooking_times_in_minutes=[2, 18, 34],
        links_to_recipe=['/recipe', '/recipe', '/recipe'],
    )


###########################
### SEARCH RECIPE PAGE ####
###########################
@app.route('/recipe')
def recipe():
    template = Template(filename=f'{TEMPLATE_DIR}/recipe.html')

    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    return template.render(
        title='Bowl of Cereal',
        image_path='static/bowl of cereal.jpg',
        image_alt='bowl of cereal',
        cooking_time_in_minutes=2.5,
        difficulty='Medium',  # can be 'Easy', 'Medium', or 'Hard'
        ingredients=['Milk', 'Cereal'],
        equipment=['Bowl', 'Cup', 'Microwave'],
        method=[
            'Fill bowl with cereal.',
            'Fill cup with milk.',
            'Warm up cup in microwave for 1 minute.',
            'Pour cup of milk into bowl of cereal.',
        ],
        num_likes=128,
    )

##################
### LOGIN PAGE ###
##################
@app.route('/login')
def login():
    template = Template(filename=f'{TEMPLATE_DIR}/login.html')
    # TODO
    return template.render()

###################
### SIGNUP PAGE ###
###################
@app.route('/signup')
def signup():
    template = Template(filename=f'{TEMPLATE_DIR}/signup.html')
    # TODO
    return template.render()

###################
### LOGOUT PAGE ###
###################
@app.route("/logout")
@login_required
def logout():
    logout_user()
    # NOTE: redirect to home page instead?
    return redirect(url_for('search'))
