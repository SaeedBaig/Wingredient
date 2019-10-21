# Recipe VALUES (<id>,V <name>, <time>, <difficulty>, <method>, <notes>, <description>, <imageRef>);
#RECIPE HEADER

# Plan is to be able to easily generate recipes into a csv that we can import into a database. This will help to have data in a csv especially if we end up modifying the database early on a lot.

#employee_writer.writerow(['John Smith', 'Accounting', 'November'])
#   employee_writer.writerow(['Erica Meyers', 'IT', 'March'])
# RecipeToIngredient VALUES (<recipe>, <ingredient>, <quantity>, <optional>, <measurement>);
#Ingredient VALUES (<id>, <name>, <isMeat>, <dietary>);

#ID, Name,Time,Difficulty,Method,
import csv
with open('recipes.csv', mode='w') as recipes:
    recipe_writer = csv.writer(recipes, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    recipe_writer.writerow(['id', 'name', 'time', 'difficutly', 'method', 'url'])
    recipe_writer.writerow(['1', 'Roasted Vegetable Soup', '30', 'Easy', "In a large saucepan, heat 3 cups of chicken stock. In 2 batches, coarsely puree the roasted vegetables and the chicken stock in the bowl of a food processor fitted with the steel blade. Pour the soup back into the pot and season, to taste. Thin with more chicken stock and reheat. The soup should be thick but not like a vegetable puree, so add more chicken stock and/or water until it's the consistency you like.\\nPlace the chickens, onions, carrots, celery, parsnips, parsley, thyme, dill, garlic, and seasonings in a 16 to 20-quart stockpot. Add 7 quarts of water and bring to a boil. Simmer uncovered for 4 hours. Strain the entire contents of the pot through a colander and discard the solids. Chill the stock overnight. The next day, remove the surface fat. Use immediately or pack in containers and freeze for up to 3 months.\\nPreheat the oven to 425 degrees F.\\nCut the carrots, parsnips, sweet potato, and butternut squash in 1- to 1 1/4-inch cubes. All the vegetables will shrink while baking, so don't cut them too small.\\nPlace all the cut vegetables in a single layer on 2 sheet pans. Drizzle them with olive oil, salt, and pepper. Toss well. Bake for 25 to 35 minutes, until all the vegetables are tender, turning once with a metal spatula.\\nSprinkle with parsley, season to taste, and serve hot."])
    recipe_writer.writerow(['2', 'Roasted Vegetable Soup', '30', 'Easy', "In a large saucepan, heat 3 cups of chicken stock. In 2 batches, coarsely puree the roasted vegetables and the chicken stock in the bowl of a food processor fitted with the steel blade. Pour the soup back into the pot and season, to taste. Thin with more chicken stock and reheat. The soup should be thick but not like a vegetable puree, so add more chicken stock and/or water until it's the consistency you like.\\nPlace the chickens, onions, carrots, celery, parsnips, parsley, thyme, dill, garlic, and seasonings in a 16 to 20-quart stockpot. Add 7 quarts of water and bring to a boil. Simmer uncovered for 4 hours. Strain the entire contents of the pot through a colander and discard the solids. Chill the stock overnight. The next day, remove the surface fat. Use immediately or pack in containers and freeze for up to 3 months.\\nPreheat the oven to 425 degrees F.\\nCut the carrots, parsnips, sweet potato, and butternut squash in 1- to 1 1/4-inch cubes. All the vegetables will shrink while baking, so don't cut them too small.\\nPlace all the cut vegetables in a single layer on 2 sheet pans. Drizzle them with olive oil, salt, and pepper. Toss well. Bake for 25 to 35 minutes, until all the vegetables are tender, turning once with a metal spatula.\\nSprinkle with parsley, season to taste, and serve hot."])



