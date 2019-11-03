import csv
with open('recipeToIngredient.csv', mode='w') as recipes:
    recipe_writer = csv.writer(recipes, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    recipe_writer.writerow(['recipe', 'ingredient', 'quantity', 'measurement', 'description', 'notes', 'optional'])
    #Chilli con carne
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
                         
    # Pumpkin and Ginger Soup
    recipe_writer.writerow(['2', '16', '1000', 'Weight', '', '', 'false'])
    recipe_writer.writerow(['2', '17', '2', 'Count', '', '', 'true'])
    recipe_writer.writerow(['2', '18', '75', 'Weight', '', '', 'false'])
    recipe_writer.writerow(['2', '19', '0.33', 'Teaspoon', 'fresh', '', 'true'])
    recipe_writer.writerow(['2', '20', '0.33', 'Teaspoon', 'fresh', '', 'true'])
    recipe_writer.writerow(['2', '6', '2 ', 'Tablespoon', 'extra virgin', '', 'false'])
    recipe_writer.writerow(['2', '21', '1000', 'Volume', 'organic', '', 'false'])
    recipe_writer.writerow(['2', '22', '125', 'Volume', '', 'plus extra to serve', 'false'])
    recipe_writer.writerow(['2', '7', '0.5', 'Tablespoon', '', '', 'true'])
    recipe_writer.writerow(['2', '23', '1', 'Count', '', '', 'true'])
   
    # Lazy garlic chicken with butter noodles
    recipe_writer.writerow(['3', '24', '200', 'Weight', 'dried', '', 'false'])
    recipe_writer.writerow(['3', '6', '2', 'Teaspoon', '', '', 'false'])
    recipe_writer.writerow(['3', '25', '600', 'Weight', '', 'trimmed', 'false'])
    recipe_writer.writerow(['3', '26', '80', 'Weight', '', 'chopped', 'false'])
    recipe_writer.writerow(['3', '2', '4', 'Count', 'cloves', 'finely chopped', 'true'])
    recipe_writer.writerow(['3', '27', '250', 'Weight', 'packet', '', 'false'])
    recipe_writer.writerow(['3', '28', '0.25', 'Teaspoon', 'pinch of dried', 'plus extra to serve', 'true'])
    recipe_writer.writerow(['3', '29', '0.33', 'Cup', 'finely chopped fresh continental', 'leaves', 'true'])
    recipe_writer.writerow(['3', '30', '50', 'Weight', 'finely shredded', 'to serve', ''])
    
    # recipe_writer.writerow(['3', '', '', '', '', '', ''])
    # recipe_writer.writerow(['3', '', '', '', '', '', ''])




