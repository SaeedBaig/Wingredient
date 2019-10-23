# Recipe VALUES (<id>,V <name>, <time>, <difficulty>, <method>, <notes>, <dhscription>, <imageRef>);
import csv
with open('recipe.csv', mode='w') as recipe:
    recipe_writer = csv.writer(recipe, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #id,name,image,url,tags,description,notes,time,difficutly,ingredients,method'tags',
    recipe_writer.writerow(['id', 'name', 'time', 'difficulty', 'notes', 'description', 'tags', 'image', 'url', 'method'])
    #recipe_writer.writerow(['1', 'Chilli Con Carne', '75', 'Easy','', '', 'tags', 'image', 'url', 'method'])
    recipe_writer.writerow(['1', 'Good Old Chilli Con Carne', '75', 'Easy', '', "This hearty, all-time classic chilli con carne recipe is hard to beat – delicious!", "Minced beef, Healthy", '/images/recipe_images/1_chilli_con_carne.jpg', 'https://www.jamieoliver.com/recipes/beef-recipes/good-old-chilli-con-carne/', "Peel and finely chop the onions, garlic, carrots and celery – don’t worry about the technique, just chop away until fine. Halve the red peppers, remove the stalks and seeds and roughly chop. Heat 2 tablespoons of oil in a large casserole pan on a medium-high heat, add the chopped veg, chilli powder, cumin, cinnamon and a good pinch of sea salt and black pepper, then cook for 7 minutes, or until softened, stirring regularly. Drain and add the chickpeas and kidney beans, tip in the tomatoes, breaking them up with the back of a spoon, then pour in 1 tin's worth of water. Add the minced beef, breaking any larger chunks. Pick the coriander leaves and put aside, then finely chop and add the stalks to the pan, with the balsamic vinegar. Season with a good pinch of sea salt and black pepper. Bring to the boil, then reduce the heat to low and simmer with a lid slightly ajar for 1 hour, or until slightly thickened and reduced, stirring occasionally.Serve up with fluffy rice or couscous, a hunk of crusty bread, or over a jacket potato, with some yoghurt, guacamole, and wedges of lime on the side for squeezing over. Sprinkle over the reserved coriander, and some fresh chilli, if you like, then tuck in."])
