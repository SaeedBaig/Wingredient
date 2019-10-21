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


    "title": "Best Chocolate Chip Cookies",
    "ingredients": [
      "1 cup butter, softened ADVERTISEMENT",
      "1 cup white sugar ADVERTISEMENT",
      "1 cup packed brown sugar ADVERTISEMENT",
      "2 eggs ADVERTISEMENT",
      "2 teaspoons vanilla extract ADVERTISEMENT",
      "3 cups all-purpose flour ADVERTISEMENT",
      "1 teaspoon baking soda ADVERTISEMENT",
      "2 teaspoons hot water ADVERTISEMENT",
      "1/2 teaspoon salt ADVERTISEMENT",
      "2 cups semisweet chocolate chips ADVERTISEMENT",
      "1 cup chopped walnuts ADVERTISEMENT",
      "ADVERTISEMENT"
    ],
    "instructions": "Preheat oven to 350 degrees F (175 degrees C).\nCream together the butter, white sugar, and brown sugar until smooth. Beat in the eggs one at a time, then stir in the vanilla. Dissolve baking soda in hot water. Add to batter along with salt. Stir in flour, chocolate chips, and nuts. Drop by large spoonfuls onto ungreased pans.\nBake for about 10 minutes in the preheated oven, or until edges are nicely browned.\n",
    "picture_link": "0SO5kdWOV94j6EfAVwMMYRM3yNN8eRi"
INSERT INTO Recipe VALUES ('1', 'Chicken Soup', '30', 'Easy', '{"Prep chicken", "Boil water", "Cook chicken", "Serve"}', 'Eat hot', 'Creamy delicious chicken soup');
-- recipe 2

-- Recipe VALUES (<id>, <name>, <time>, <difficulty>, <method>, <notes>, <description>, <imageRef>);
-- Account VALUES (<id>, <username>, <password>, <details>);
-- Ingredient VALUES (<id>, <name>, <isMeat>, <dietary>);
-- RecipeToIngredient VALUES (<recipe>, <ingredient>, <quantity>, <optional>, <measurement>);
INSERT INTO Recipe VALUES ('2', 'Chocolate Chip Cookies, 20');

INSERT INTO Ingredient VALUES ('1', 'Chicken', 'true', 'None');
INSERT INTO Ingredient VALUES ('2', 'Onion', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('3', 'Carrot', 'false', 'Vegan');
INSERT INTO Ingredient VALUES ('4', 'Water', 'false', 'Vegan');

INSERT INTO RecipeToIngredient VALUES ('1', '1', '500', 'false', 'Weight');
INSERT INTO RecipeToIngredient VALUES ('1', '2', '2', 'true', 'Count');
INSERT INTO RecipeToIngredient VALUES ('1', '3', '1', 'true', 'Count');
INSERT INTO RecipeToIngredient VALUES ('1', '4', '500', 'false', 'Volume');
