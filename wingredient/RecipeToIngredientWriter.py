#RecipeToIngredient VALUES (<recipe>, <ingredient>, <quantity>, <optional>, <measurement>);
import csv
with open('recipeToIngredient.csv', mode='w') as recipes:
    recipe_writer = csv.writer(recipes, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    recipe_writer.writerow(['recipe', 'ingredient', 'quantity', 'measurement', 'description', 'notes', 'optional'])
    # Description is before ingredient and notes is after 
    # e.g. 2 medium carrots (chopped)
    # medium is the description 
    # chopped is the note
    recipe_writer.writerow(['1', '1', '2', 'Count', 'medium', '', 'true'])
    recipe_writer.writerow(['1', '2', '2', 'Count', 'cloves', '', 'true'])
    recipe_writer.writerow(['1', '3', '2', 'Count', 'medium', '', 'true'])
    recipe_writer.writerow(['1', '4', '2', 'Count', 'sticks', '', 'true'])
    recipe_writer.writerow(['1', '5', '2', 'Count', '', '', 'true'])
    recipe_writer.writerow(['1', '6', '2', 'Tablespoon', '', '', 'false'])
    recipe_writer.writerow(['1', '7', '1', 'Teaspoon', '', '', 'true'])
    recipe_writer.writerow(['1', '8', '1', 'Teaspoon', '', '', 'true'])
    recipe_writer.writerow(['1', '9', '1', 'Teaspoon', '', '', 'true'])
    recipe_writer.writerow(['1', '10', '400', 'Weight', '', '', 'true'])
    recipe_writer.writerow(['1', '11', '400', 'Weight', '', '', 'true'])
    recipe_writer.writerow(['1', '12', '800', 'Weight', 'chopped', '', 'false'])
    recipe_writer.writerow(['1', '13', '500', 'Weight', '', '', 'false'])
    recipe_writer.writerow(['1', '14', '15', 'Weight', '', '', 'true'])
    recipe_writer.writerow(['1', '15', '2', 'Tablespoon', '', 'true', 'true'])
                                  
#recipe_writer.writerow(['1', ['2 medium onions', '2 cloves garlic', '2 medium carrots', '2 sticks celery', '2 red peppers', 'olive oil', '1 heaped teaspoon chilli powder', '1 heaped teaspoon ground cumin', '1 heaped teaspoon ground cinnamon', '1 x 400 g tin of chickpeas', '1 x 400 g tin of red kidney beans', '2 x 400 g tin of chopped tomatoes', '500 g quality minced beef', '½ a bunch of fresh coriander (15g)', '2 tablespoons balsamic vinegar'] 
