import csv
with open('ingredient.csv', mode='w') as recipes:
    recipe_writer = csv.writer(recipes, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Ingredient VALUES (<id>, <name>, <dietary>)
    recipe_writer.writerow(['id', 'name', 'dietary'])
    recipe_writer.writerow(['1', 'Onion', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['2', 'Garlic', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['3', 'Carrot', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['4', 'Celerly', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['5', 'Capsicum', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['6', 'Olive Oil', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['7', 'Chilli Powder', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['8', 'Ground Cumin', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['9', 'Ground Cinnamon', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['10', 'Tinned Chickpeas', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['11', 'Tinned Kidney Beans', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['12', 'Tinned Tomatoes', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['13', 'Minced Beef', 'Meat']) 
    recipe_writer.writerow(['14', 'Corriader', 'Vegan, Vegetarian']) 
    recipe_writer.writerow(['15', 'Basamic Vinegar', 'Vegan, Vegetarian']) 


    #dium onions', '2 cloves garlic', '2 medium carrots', '2 sticks celery', '2 red peppers', 'olive oil', '1 heaped teaspoon chilli powder', '1 heaped teaspoon ground cumin', '1 heaped teaspoon ground cinnamon', '1 x 400 g tin of chickpeas', '1 x 400 g tin of red kidney beans', '2 x 400 g tin of chopped tomatoes', '500 g quality minced beef', '½ a bunch of fresh coriander (15g)', '2 tablespoons balsamic vinegar'] 

        

#recipe_writer.writerow(['1', ['2 medium onions', '2 cloves garlic', '2 medium carrots', '2 sticks celery', '2 red peppers', 'olive oil', '1 heaped teaspoon chilli powder', '1 heaped teaspoon ground cumin', '1 heaped teaspoon ground cinnamon', '1 x 400 g tin of chickpeas', '1 x 400 g tin of red kidney beans', '2 x 400 g tin of chopped tomatoes', '500 g quality minced beef', '½ a bunch of fresh coriander (15g)', '2 tablespoons balsamic vinegar'] 

