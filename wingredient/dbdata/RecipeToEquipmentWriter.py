import csv
with open('wingredient/dbdata/recipeToEquipment.csv', mode='w') as recipeToEquipment:
    #print('recipeToEquipment.csv generated')
    equipment_writer = csv.writer(recipeToEquipment, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    equipment_writer.writerow(['recipe', 'equipment'])
    #Chilli con carne
    equipment_writer.writerow(['1', '1'])
    # Pumpkin and Ginger Soup
    equipment_writer.writerow(['2', '2'])
    # Lazy garlic chicken with butter noodles
    equipment_writer.writerow(['3', '3'])
    # Vegan pad see ew
    equipment_writer.writerow(['4', '4'])
    equipment_writer.writerow(['4', '5'])
    equipment_writer.writerow(['4', '6'])
    # Basic beef and vegetable stir-fry
    equipment_writer.writerow(['5', '4'])
    # Vegetarian Thai curry tray bake
    equipment_writer.writerow(['6', '7'])
    # Quick Turkish lamb pizzas
    equipment_writer.writerow(['7', '8'])
    equipment_writer.writerow(['7', '9'])
    # Asian-style mushroom burger 
    equipment_writer.writerow(['8', '10'])
    # Gluten-free Italian meatballs and spaghetti
    equipment_writer.writerow(['9', '2'])
    #  Lemon chicken with smoky corn salad
    equipment_writer.writerow(['10', '10'])
    # Middle Eastern lamb koftas with aromatic lentil rice
    equipment_writer.writerow(['11', '2'])
    equipment_writer.writerow(['11', '3'])
    # Salmon and soba noodle bowl
    equipment_writer.writerow(['12', '2'])
    equipment_writer.writerow(['12', '3'])
    # Crispy Korean fried tofu with snow peas
    equipment_writer.writerow(['13', '11'])
    equipment_writer.writerow(['13', '4'])
    # 17-minute turmeric chilli fried egg bowl
    equipment_writer.writerow(['14', '3'])
    # Mexican-style omelette wrap 
    equipment_writer.writerow(['15', '3'])
    # Vegan pasta salad with green goddess dressing
    equipment_writer.writerow(['16', '2'])
    equipment_writer.writerow(['16', '9'])
    equipment_writer.writerow(['16', '12'])
    # Speedy shepherd's pie
    equipment_writer.writerow(['17', '13'])
    equipment_writer.writerow(['17', '14'])
    # Japanese-style shredded chicken salad
    equipment_writer.writerow(['18', '15'])
    # Karaage chicken (Fried chicken)
    equipment_writer.writerow(['19', '16'])
    equipment_writer.writerow(['19', '2'])
    # Simple crepe recipe
    equipment_writer.writerow(['20', '8'])


    




