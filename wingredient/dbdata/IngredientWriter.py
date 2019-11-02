import csv
with open('ingredient.csv', mode='w') as recipes:
    recipe_writer = csv.writer(recipes, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    recipe_writer.writerow(['id', 'name'])
    recipe_writer.writerow(['1', 'Onion']) 
    recipe_writer.writerow(['2', 'Garlic']) 
    recipe_writer.writerow(['3', 'Carrot']) 
    recipe_writer.writerow(['4', 'Celerly']) 
    recipe_writer.writerow(['5', 'Capsicum']) 
    recipe_writer.writerow(['6', 'Olive Oil']) 
    recipe_writer.writerow(['7', 'Chilli Powder']) 
    recipe_writer.writerow(['8', 'Ground Cumin']) 
    recipe_writer.writerow(['9', 'Ground Cinnamon']) 
    recipe_writer.writerow(['10', 'Tinned Chickpeas']) 
    recipe_writer.writerow(['11', 'Tinned Red Kidney Beans']) 
    recipe_writer.writerow(['12', 'Tinned Tomatoes']) 
    recipe_writer.writerow(['13', 'Minced Beef']) 
    recipe_writer.writerow(['14', 'Corriader']) 
    recipe_writer.writerow(['15', 'Basamic Vinegar']) 
    recipe_writer.writerow(['16', 'Pumpkin', '  


    



        


