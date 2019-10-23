-- Recipe VALUES (<id>, <name>, <time>, <difficulty>, <method>, <notes>, <description>, <imageRef>);
-- Account VALUES (<id>, <username>, <password>, <details>);
-- Ingredient VALUES (<id>, <name>, <isMeat>, <dietary>);
-- RecipeToIngredient VALUES (<recipe>, <ingredient>, <quantity>, <optional>, <measurement>);


--recipe 1
INSERT INTO Recipe VALUES ('1', 'Chicken Soup', '30', 'Easy', '{"Prep chicken", "Boil water", "Cook chicken", "Serve"}', 'Eat hot', 'Creamy delicious chicken soup');

INSERT INTO Ingredient VALUES ('1', 'Chicken', 'true', 'None');
INSERT INTO Ingredient VALUES ('2', 'Onion', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('3', 'Carrot', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('4', 'Water', 'false', 'Vegan');

INSERT INTO RecipeToIngredient VALUES ('1', '2', '2', 'true', 'Count');
INSERT INTO RecipeToIngredient VALUES ('1', '1', '500', 'false', 'Weight');
INSERT INTO RecipeToIngredient VALUES ('1', '3', '1', 'true', 'Count');
INSERT INTO RecipeToIngredient VALUES ('1', '4', '500', 'false', 'Volume');


INSERT INTO Recipe VALUES ('1', 'Chicken Soup', '30', 'Easy', '{"Prep chicken", "Boil water", "Cook chicken", "Serve"}', 'Eat hot', 'Creamy delicious chicken soup');
-- recipe 2

