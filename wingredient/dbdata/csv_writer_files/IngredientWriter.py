import csv
with open('ingredient.csv', mode='w') as recipes:
    #print('ingredient.csv generated')
    recipe_writer = csv.writer(recipes, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    recipe_writer.writerow(['id', 'name', 'measurement'])
    recipe_writer.writerow(['1', 'Brown Onion', 'Count']) 
    recipe_writer.writerow(['2', 'Garlic Cloves', 'Count']) 
    recipe_writer.writerow(['3', 'Carrot', 'Count']) 
    recipe_writer.writerow(['4', 'Celery', 'Count']) 
    recipe_writer.writerow(['5', 'Red Capsicum', 'Count']) 
    recipe_writer.writerow(['6', 'Olive Oil', 'Count']) 
    recipe_writer.writerow(['7', 'Chilli Powder', 'Count']) 
    recipe_writer.writerow(['8', 'Ground Cumin', 'Count']) 
    recipe_writer.writerow(['9', 'Ground Cinnamon', 'Count']) 
    recipe_writer.writerow(['10', 'Tinned Chickpeas', 'Weight']) 
    recipe_writer.writerow(['11', 'Tinned Red Kidney Beans', 'Weight']) 
    recipe_writer.writerow(['12', 'Tinned Tomatoes', 'Weight']) 
    recipe_writer.writerow(['13', 'Beef Mince', 'Weight']) 
    recipe_writer.writerow(['14', 'Coriander', 'Count']) 
    recipe_writer.writerow(['15', 'Balsamic Vinegar', 'Count']) 
    recipe_writer.writerow(['16', 'Kent Pumpkin', 'Weight'])
    recipe_writer.writerow(['17', 'Shallots', 'Count'])
    recipe_writer.writerow(['18', 'Ginger', 'Count'])
    recipe_writer.writerow(['19', 'Chives', 'Count'])
    recipe_writer.writerow(['20', 'Mint Leaves', 'Count'])
    recipe_writer.writerow(['21', 'Vegetable Stock', 'Volume'])
    recipe_writer.writerow(['22', 'Coconut Milk', 'Volume'])
    recipe_writer.writerow(['23', 'Lime', 'Count'])
    recipe_writer.writerow(['24', 'Spaghetti', 'Weight'])
    recipe_writer.writerow(['25', 'Chicken Thigh Fillets', 'Weight'])
    recipe_writer.writerow(['26', 'Butter', 'Weight'])
    recipe_writer.writerow(['27', 'Zucchini Noodles', 'Weight'])
    recipe_writer.writerow(['28', 'Chilli Flakes', 'Count'])
    recipe_writer.writerow(['29', 'Parsley Leaves', 'Count'])
    recipe_writer.writerow(['30', 'Parmesan', 'Weight'])
    recipe_writer.writerow(['31', 'Tofu', 'Weight'])
    recipe_writer.writerow(['32', 'Rice Noodle', 'Weight'])
    recipe_writer.writerow(['33', 'Cornflour', 'Weight'])
    recipe_writer.writerow(['34', 'Peanut Oil', 'Count'])
    recipe_writer.writerow(['35', 'Chinese Broccoli', 'Count'])
    recipe_writer.writerow(['36', 'Soy Sauce', 'Count'])
    recipe_writer.writerow(['37', 'Brown Sugar', 'Count'])
    recipe_writer.writerow(['38', 'Egg', 'Count'])
    recipe_writer.writerow(['39', 'Steak', 'Weight'])
    recipe_writer.writerow(['40', 'Baby Corn', 'Count'])
    recipe_writer.writerow(['41', 'Broccolini', 'Count'])
    recipe_writer.writerow(['42', 'Oyster Sauce', 'Count'])
    recipe_writer.writerow(['43', 'Rice', 'Count'])
    recipe_writer.writerow(['44', 'Curry Paste', 'Count'])
    recipe_writer.writerow(['45', 'Baby Carrot', 'Count'])
    recipe_writer.writerow(['46', 'Lamb Mince', 'Weight'])
    recipe_writer.writerow(['47', 'Mixed Spice', 'Count'])
    recipe_writer.writerow(['48', 'Turkish Bread', 'Count'])
    recipe_writer.writerow(['49', 'Pizza Cheese', 'Weight']) 
    recipe_writer.writerow(['50', 'Cherry Tomatoes', 'Weight']) 
    recipe_writer.writerow(['51', 'Lemon', 'Count']) 
    recipe_writer.writerow(['52', 'Mixed Salad Leaves', 'Count']) 
    recipe_writer.writerow(['53', 'Mushrooms', 'Weight']) 
    recipe_writer.writerow(['54', 'Sesame Seeds', 'Weight']) 
    recipe_writer.writerow(['55', 'Lemon Juice', 'Volume']) 
    recipe_writer.writerow(['56', 'Miso Paste', 'Count']) 
    recipe_writer.writerow(['57', 'Bread Rolls', 'Count']) 
    recipe_writer.writerow(['58', 'Red Cabbage', 'Count']) 
    recipe_writer.writerow(['59', 'Sprouts', 'Weight']) 
    recipe_writer.writerow(['60', 'Basil', 'Count']) 
    recipe_writer.writerow(['61', 'Tomato Paste', 'Weight']) 
    recipe_writer.writerow(['62', 'Tomato Passata', 'Volume']) 
    recipe_writer.writerow(['63', 'Whole Chicken', 'Weight']) 
    recipe_writer.writerow(['64', 'Oregano', 'Count']) 
    recipe_writer.writerow(['65', 'Paprika', 'Count']) 
    recipe_writer.writerow(['66', 'Corn', 'Count']) 
    recipe_writer.writerow(['67', 'Spring Onion', 'Count']) 
    recipe_writer.writerow(['68', 'Baby Gem Lettuce', 'Count']) 
    recipe_writer.writerow(['69', 'Avocado', 'Count']) 
    recipe_writer.writerow(['70', 'Buttermilk', 'Volume'])
    recipe_writer.writerow(['71', 'Greek-style Yoghurt', 'Weight'])
    recipe_writer.writerow(['72', 'Breadcrumbs', 'Weight'])
    recipe_writer.writerow(['73', 'Lentils', 'Weight'])
    recipe_writer.writerow(['74', 'Chicken Stock', 'Volume'])
    recipe_writer.writerow(['75', 'Tomatoes', 'Count'])
    recipe_writer.writerow(['76', 'Ground Coriander', 'Count'])
    recipe_writer.writerow(['77', 'Cayenne Pepper', 'Count'])
    recipe_writer.writerow(['78', 'Salt', 'Count'])    
    recipe_writer.writerow(['79', 'Pepper', 'Count'])
    recipe_writer.writerow(['80', 'Soba Noodles', 'Weight'])
    recipe_writer.writerow(['81', 'Teriyaki Marinade', 'Volume'])   
    recipe_writer.writerow(['82', 'Lime Juice', 'Volume'])   
    recipe_writer.writerow(['83', 'Sesame Oil', 'Count'])   
    recipe_writer.writerow(['84', 'Salmon', 'Count'])   
    recipe_writer.writerow(['85', 'Radishes', 'Count'])   
    recipe_writer.writerow(['86', 'Baby Cucumbers', 'Count'])   
    recipe_writer.writerow(['87', 'Tomato Sauce', 'Volume'])   
    recipe_writer.writerow(['88', 'Rice Wine Vinegar', 'Count'])   
    recipe_writer.writerow(['89', 'Honey', 'Count'])
    recipe_writer.writerow(['90', 'Gochujang paste', 'Count'])
    recipe_writer.writerow(['91', 'Garlic Chives', 'Count'])        
    recipe_writer.writerow(['92', 'Rice Flour', 'Weight'])
    recipe_writer.writerow(['93', 'Vegetable oil', 'Count'])
    recipe_writer.writerow(['94', 'Snow Peas', 'Weight'])
    recipe_writer.writerow(['95', 'Kale', 'Weight'])
    recipe_writer.writerow(['96', 'Spinach Mix', 'Weight'])
    recipe_writer.writerow(['97', 'Ground Turmeric', 'Count'])
    recipe_writer.writerow(['98', 'Red Onion', 'Count'])
    recipe_writer.writerow(['99', 'Dill', 'Count'])
    recipe_writer.writerow(['100', 'Tabasco Sauce', 'Count'])
    recipe_writer.writerow(['101', 'Red Wine Vinegar', 'Count'])
    recipe_writer.writerow(['102', 'Baby Spinach', 'Weight'])
    recipe_writer.writerow(['103', 'Zucchini', 'Count'])
    recipe_writer.writerow(['104', 'Roma Tomatoes', 'Weight'])
    recipe_writer.writerow(['105', 'Pasta', 'Weight'])
    recipe_writer.writerow(['106', 'Pine Nuts', 'Weight'])
    recipe_writer.writerow(['107', 'Baby Rocket Leaves', 'Count'])
    recipe_writer.writerow(['108', 'Mixed Vegetables', 'Weight'])
    recipe_writer.writerow(['109', 'Beef Stock', 'Volume'])
    recipe_writer.writerow(['110', 'Sweet Potato', 'Weight']) 
    recipe_writer.writerow(['111', 'Goat Cheese', 'Weight'])
    recipe_writer.writerow(['112', 'Chicken Breast', 'Weight'])
    recipe_writer.writerow(['113', 'Chinese Cabbage', 'Count'])
    recipe_writer.writerow(['114', 'Apple', 'Count'])
    recipe_writer.writerow(['115', 'Nori', 'Count'])
    recipe_writer.writerow(['116', 'Mirin', 'Volume'])
    recipe_writer.writerow(['117', 'Sushi Seasoning', 'Count'])
    recipe_writer.writerow(['118', 'Plain Flour', 'Weight'])
    recipe_writer.writerow(['119', 'Milk', 'Volume'])
    recipe_writer.writerow(['120', 'Self-raising Flour', 'Weight']) 
    recipe_writer.writerow(['121', 'Butternut Pumpkin', 'Weight'])
    recipe_writer.writerow(['122', 'Water', 'Volume'])
    recipe_writer.writerow(['123', 'Pork Mince', 'Weight'])
#    recipe_writer.writerow(['125', ''])
#    recipe_writer.writerow(['126', ''])
#    recipe_writer.writerow(['127', ''])
#    recipe_writer.writerow(['128', ''])
#    recipe_writer.writerow(['129', ''])
#    recipe_writer.writerow(['130', '']) 
#    recipe_writer.writerow(['131', ''])
#    recipe_writer.writerow(['132', ''])
#    recipe_writer.writerow(['133', ''])
#    recipe_writer.writerow(['134', ''])
#    recipe_writer.writerow(['135', ''])
#    recipe_writer.writerow(['136', ''])
#    recipe_writer.writerow(['137', ''])
#    recipe_writer.writerow(['138', ''])
#    recipe_writer.writerow(['139', ''])
#    recipe_writer.writerow(['140', '']) 
#    recipe_writer.writerow(['141', ''])
#    recipe_writer.writerow(['142', ''])
#    recipe_writer.writerow(['143', ''])
#    recipe_writer.writerow(['144', ''])
#    recipe_writer.writerow(['145', ''])
#    recipe_writer.writerow(['146', ''])
#    recipe_writer.writerow(['147', ''])
#    recipe_writer.writerow(['148', ''])
#    recipe_writer.writerow(['149', ''])
#    recipe_writer.writerow(['150', '']) 
#    recipe_writer.writerow(['151', '']) 
#    recipe_writer.writerow(['152', '']) 
#    recipe_writer.writerow(['153', '']) 
#    recipe_writer.writerow(['154', '']) 
#    recipe_writer.writerow(['155', '']) 
#    recipe_writer.writerow(['156', '']) 
#    recipe_writer.writerow(['157', '']) 
#    recipe_writer.writerow(['158', '']) 
#    recipe_writer.writerow(['159', '']) 
#    recipe_writer.writerow(['160', '']) 
#    recipe_writer.writerow(['161', '']) 
#    recipe_writer.writerow(['162', '']) 
#    recipe_writer.writerow(['163', '']) 
#    recipe_writer.writerow(['164', '']) 
#    recipe_writer.writerow(['165', '']) 
#    recipe_writer.writerow(['166', '']) 
#    recipe_writer.writerow(['167', '']) 
#    recipe_writer.writerow(['168', '']) 
#    recipe_writer.writerow(['169', '']) 
#    recipe_writer.writerow(['170', ''])
#    recipe_writer.writerow(['171', ''])
#    recipe_writer.writerow(['172', ''])
#    recipe_writer.writerow(['173', ''])
#    recipe_writer.writerow(['174', ''])
#    recipe_writer.writerow(['175', ''])
#    recipe_writer.writerow(['176', ''])
#    recipe_writer.writerow(['177', ''])
#    recipe_writer.writerow(['178', ''])    
#    recipe_writer.writerow(['179', ''])
#    recipe_writer.writerow(['180', ''])
#    recipe_writer.writerow(['181', ''])   
#    recipe_writer.writerow(['182', ''])   
#    recipe_writer.writerow(['183', ''])   
#    recipe_writer.writerow(['184', ''])   
#    recipe_writer.writerow(['185', ''])   
#    recipe_writer.writerow(['186', ''])   
#    recipe_writer.writerow(['187', ''])   
#    recipe_writer.writerow(['188', ''])   
#    recipe_writer.writerow(['189', ''])
#    recipe_writer.writerow(['190', ''])
#    recipe_writer.writerow(['191', ''])        
#    recipe_writer.writerow(['192', ''])
#    recipe_writer.writerow(['193', ''])
#    recipe_writer.writerow(['194', ''])
#    recipe_writer.writerow(['195', ''])
#    recipe_writer.writerow(['196', ''])
#    recipe_writer.writerow(['197', ''])
#    recipe_writer.writerow(['198', ''])
#    recipe_writer.writerow(['199', ''])

#   recipe_writer.writerow(['100', ''])
#   recipe_writer.writerow(['101', ''])
#   recipe_writer.writerow(['102', ''])
#   recipe_writer.writerow(['103', ''])
#   recipe_writer.writerow(['104', ''])
#   recipe_writer.writerow(['105', ''])
#   recipe_writer.writerow(['106', ''])
#   recipe_writer.writerow(['107', ''])
#   recipe_writer.writerow(['108', ''])
#   recipe_writer.writerow(['109', ''])
#   recipe_writer.writerow(['110', '']) 
#   recipe_writer.writerow(['111', ''])
#   recipe_writer.writerow(['112', ''])
#   recipe_writer.writerow(['113', ''])
#   recipe_writer.writerow(['114', ''])
#   recipe_writer.writerow(['115', ''])
#   recipe_writer.writerow(['116', ''])
#   recipe_writer.writerow(['117', ''])
#   recipe_writer.writerow(['118', ''])
#   recipe_writer.writerow(['119', ''])
#   recipe_writer.writerow(['120', '']) 
#   recipe_writer.writerow(['121', ''])
#   recipe_writer.writerow(['122', ''])
#   recipe_writer.writerow(['123', ''])
#   recipe_writer.writerow(['124', ''])
#   recipe_writer.writerow(['125', ''])
#   recipe_writer.writerow(['126', ''])
#   recipe_writer.writerow(['127', ''])
#   recipe_writer.writerow(['128', ''])
#   recipe_writer.writerow(['129', ''])
#   recipe_writer.writerow(['130', '']) 
#   recipe_writer.writerow(['131', ''])
#   recipe_writer.writerow(['132', ''])
#   recipe_writer.writerow(['133', ''])
#   recipe_writer.writerow(['134', ''])
#   recipe_writer.writerow(['135', ''])
#   recipe_writer.writerow(['136', ''])
#   recipe_writer.writerow(['137', ''])
#   recipe_writer.writerow(['138', ''])
#   recipe_writer.writerow(['139', ''])
#   recipe_writer.writerow(['140', '']) 
#   recipe_writer.writerow(['141', ''])
#   recipe_writer.writerow(['142', ''])
#   recipe_writer.writerow(['143', ''])
#   recipe_writer.writerow(['144', ''])
#   recipe_writer.writerow(['145', ''])
#   recipe_writer.writerow(['146', ''])
#   recipe_writer.writerow(['147', ''])
#   recipe_writer.writerow(['148', ''])
#   recipe_writer.writerow(['149', ''])
#   recipe_writer.writerow(['150', '']) 
#   recipe_writer.writerow(['151', '']) 
#   recipe_writer.writerow(['152', '']) 
#   recipe_writer.writerow(['153', '']) 
#   recipe_writer.writerow(['154', '']) 
#   recipe_writer.writerow(['155', '']) 
#   recipe_writer.writerow(['156', '']) 
#   recipe_writer.writerow(['157', '']) 
#   recipe_writer.writerow(['158', '']) 
#   recipe_writer.writerow(['159', '']) 
#   recipe_writer.writerow(['160', '']) 
#   recipe_writer.writerow(['161', '']) 
#   recipe_writer.writerow(['162', '']) 
#   recipe_writer.writerow(['163', '']) 
#   recipe_writer.writerow(['164', '']) 
#   recipe_writer.writerow(['165', '']) 
#   recipe_writer.writerow(['166', '']) 
#   recipe_writer.writerow(['167', '']) 
#   recipe_writer.writerow(['168', '']) 
#   recipe_writer.writerow(['169', '']) 
#   recipe_writer.writerow(['170', ''])
#   recipe_writer.writerow(['171', ''])
#   recipe_writer.writerow(['172', ''])
#   recipe_writer.writerow(['173', ''])
#   recipe_writer.writerow(['174', ''])
#   recipe_writer.writerow(['175', ''])
#   recipe_writer.writerow(['176', ''])
#   recipe_writer.writerow(['177', ''])
#   recipe_writer.writerow(['178', ''])    
#   recipe_writer.writerow(['179', ''])
#   recipe_writer.writerow(['180', ''])
#   recipe_writer.writerow(['181', ''])   
#   recipe_writer.writerow(['182', ''])   
#   recipe_writer.writerow(['183', ''])   
#   recipe_writer.writerow(['184', ''])   
#   recipe_writer.writerow(['185', ''])   
#   recipe_writer.writerow(['186', ''])   
#   recipe_writer.writerow(['187', ''])   
#   recipe_writer.writerow(['188', ''])   
#   recipe_writer.writerow(['189', ''])
#   recipe_writer.writerow(['190', ''])
#   recipe_writer.writerow(['191', ''])        
#   recipe_writer.writerow(['192', ''])
#   recipe_writer.writerow(['193', ''])
#   recipe_writer.writerow(['194', ''])
#   recipe_writer.writerow(['195', ''])
#   recipe_writer.writerow(['196', ''])
#   recipe_writer.writerow(['197', ''])
#   recipe_writer.writerow(['198', ''])
#   recipe_writer.writerow(['199', ''])
