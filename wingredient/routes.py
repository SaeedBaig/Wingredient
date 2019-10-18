"""Module for the Flask app object."""
from flask import Flask
from mako.template import Template
from os.path import abspath

BASE_DIR = 'wingredient'
TEMPLATE_DIR = abspath(f'{BASE_DIR}/templates')
STATIC_DIR = abspath(f'{BASE_DIR}/static')

app = Flask(
"Wingredient",
template_folder=TEMPLATE_DIR,
static_folder=STATIC_DIR)


#################
### HOME PAGE ###
#################
@app.route("/")
def search():
    template = Template(filename=f'{TEMPLATE_DIR}/search.html')

    # This list of ingredients is hard-coded;
    # it should probably be pulled out of the database
    return template.render(
    ingredients=['Milk', 'Flour', 'Sugar', 'Vanilla', 'Eggs']
    )


###########################
### SEARCH RESULTS PAGE ###
###########################
@app.route("/results")
def search_results():
    template = Template(filename=f'{TEMPLATE_DIR}/search-results.html')

    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    return template.render(
    titles=['Bowl of Cereal', 'Omellete', 'Stir Fry'],
    image_paths=['static/bowl of cereal.jpg', 'static/omellete.jpg',
    'static/stir fry.jpg'],
    image_alts=['bowl of cereal', 'omellete', 'stir fry'],
    ratings=[74, 86, 91],
    cooking_times_in_minutes=[2, 18, 34],
    links_to_recipe = ['#', '#', '#']
    )


###########################
### SEARCH RECIPE PAGE ####
###########################
@app.route("/recipe")
def recipe():
    template = Template(filename=f'{TEMPLATE_DIR}/recipe.html')

    # All these paramaters are hard-coded;
    # they should probably be pulled out of the database
    return template.render(
    title='Bowl of Cereal',
    image_path='static/bowl of cereal.jpg',
    image_alt='bowl of cereal',
    cooking_time_in_minutes=2.5,
    difficulty='Medium',    # can be 'Easy', 'Medium', or 'Hard'
    ingredients=['Milk', 'Cereal'],
    equipment=['Bowl', 'Cup', 'Microwave'],
    method = [
    'Fill bowl with cereal.',
    'Fill cup with milk.',
    'Warm up cup in microwave for 1 minute.',
    'Pour cup of milk into bowl of cereal.'],
    num_likes=128
    )
