-- Recipe VALUES (<id>, <name>, <time>, <difficulty>, <method>, <notes>, <description>, <imageRef>);
INSERT INTO Recipe VALUES ('1', 'Chicken Soup', '30', 'Medium', '{"Prep chicken", "Boil water", "Cook chicken", "Serve"}', 'Eat hot', 'Creamy delicious chicken soup', 'static/chicken_soup.jpg');
INSERT INTO Recipe VALUES ('2', 'Avocado Toast', '10', 'Easy', '{"Toast bread", "SCrape out avocado", "Spread avocado on toast", "Serve"}', 'Add pepper as a garnish', 'Healthy breakfast avocado toast', 'static/avocado_toast.jpg');
INSERT INTO Recipe VALUES ('3', 'Ham Sandwich', '15', 'Easy', '{"Prepare lettuce, tomato", "Stack lettuce, tomato, ham onto bread", "Serve"}', 'None', 'Healthy, simple ham sandwich', 'static/ham_sandwich.jpeg');
INSERT INTO Recipe VALUES ('4', 'Bowl of Cereal', '5', 'Easy', '{"Pour cereal into bowl", "Pour milk on top of cereal up to above cereal level", "Serve"}', 'Eat immediately', 'Basic bowl of cereal', 'static/bowl of cereal.jpg');

-- Ingredient (<id>, <name>, <isMeat>, <dietary>);
INSERT INTO Ingredient VALUES ('1', 'Chicken', 'true', 'None');
INSERT INTO Ingredient VALUES ('2', 'Onion', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('3', 'Carrot', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('4', 'Water', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('5', 'Milk', 'true', 'Vegetarian');
INSERT INTO Ingredient VALUES ('6', 'Eggs', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('7', 'Bread', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('8', 'Cereal', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('9', 'Butter', 'true', 'Vegetarian');
INSERT INTO Ingredient VALUES ('10', 'Flour', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('11', 'Sugar', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('12', 'Avocado', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('13', 'Ham', 'true', 'None');
INSERT INTO Ingredient VALUES ('14', 'Lettuce', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('15', 'Tomato', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('16', 'Beef Mince', 'false', 'None');

-- RecipeToIngredient (<recipe>, <ingredient>, <quantity>, <optional>, <measurement>);
INSERT INTO RecipeToIngredient VALUES ('1', '1', '500', 'false', 'Weight'); -- chicken for chicken soup
INSERT INTO RecipeToIngredient VALUES ('1', '2', '2', 'true', 'Count'); -- onion for chicken soup
INSERT INTO RecipeToIngredient VALUES ('1', '3', '1', 'true', 'Count'); -- carrot for chicken soup
INSERT INTO RecipeToIngredient VALUES ('1', '4', '500', 'false', 'Volume'); -- water for chicken soup
INSERT INTO RecipeToIngredient VALUES ('2', '7', '2', 'false', 'Count'); --bread for avo toast
INSERT INTO RecipeToIngredient VALUES ('2', '12', '1', 'false', 'Count'); -- avo for avo toast
INSERT INTO RecipeToIngredient VALUES ('3', '7', '2', 'false', 'Count'); --bread for ham sandwich
INSERT INTO RecipeToIngredient VALUES ('3', '14', '1', 'true', 'Count'); --lettuce for ham sandwich
INSERT INTO RecipeToIngredient VALUES ('3', '15', '1', 'true', 'Count'); -- tomato for ham sandwich
INSERT INTO RecipeToIngredient VALUES ('3', '13', '2', 'false', 'Count'); -- ham for ham sandwich
INSERT INTO RecipeToIngredient VALUES ('4', '8', '100', 'false', 'Weight'); -- cereal for bowl of cereal
INSERT INTO RecipeToIngredient VALUES ('4', '5', '200', 'false', 'Volume'); -- milk for bowl of cereal

-- Equipment(<id>, <name>)
INSERT INTO Equipment VALUES ('1', 'Frying Pan');
INSERT INTO Equipment VALUES ('2', 'Pot');
INSERT INTO Equipment VALUES ('3', 'Bowl');
INSERT INTO Equipment VALUES ('4', 'Plate');
INSERT INTO Equipment VALUES ('5', 'Knife');

-- RecipeToEquipment(<recipe>, <equipment>)
INSERT INTO RecipeToEquipment VALUES ('1', '2'); -- pot for chicken soup
INSERT INTO RecipeToEquipment VALUES ('1', '3'); -- bowl for chicken soup
INSERT INTO RecipeToEquipment VALUES ('2', '4'); -- plate for avo toast
INSERT INTO RecipeToEquipment VALUES ('2', '5'); -- knife for avo toast
INSERT INTO RecipeToEquipment VALUES ('3', '4'); -- plate for ham sandwich
INSERT INTO RecipeToEquipment VALUES ('3', '5'); -- knife for ham sandwich
INSERT INTO RecipeToEquipment VALUES ('4', '3'); -- bowl for cereal

-- Account VALUES (<username>, <pwhash>, <pwsalt>, <details>);
-- NOTE DON'T INSERT ACCOUNTS HERE, USE THE SIGNUP PAGE INSTEAD




