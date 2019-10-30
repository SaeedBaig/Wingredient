import csv
with open('recipeToIngredient.csv', mode='w') as recipes:
    recipe_writer = csv.writer(recipes, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    recipe_writer.writerow(['recipe', 'ingredient', 'quantity', 'measurement', 'description', 'notes', 'optional'])
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
    recipe_writer.writerow(['1', '15', '2', 'Tablespoon', '', '', 'true'])
                                  