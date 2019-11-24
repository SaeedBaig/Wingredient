-- method is an array of text outlining the steps of the recipe
-- imageRef holds a file path to an image
DROP TYPE IF EXISTS MeasurementTypes CASCADE;
CREATE TYPE MeasurementTypes as ENUM('g', 'ml', 'Count');

DROP TYPE IF EXISTS Recipe_MeasurementTypes CASCADE;
CREATE TYPE Recipe_MeasurementTypes as ENUM('Tablespoon', 'Teaspoon', 'Cup');

DROP TYPE IF EXISTS Difficulty CASCADE;
CREATE TYPE Difficulty as ENUM('Easy', 'Intermediate', 'Hard');

-- Enum for different dietary traits
--DROP TYPE IF EXISTS DietaryTraits CASCADE;
-- should this be a list not an ENUM  or you can have multiple?
--CREATE TYPE DietaryTraits as ENUM('None', 'Vegan', 'Vegetarian', 'Caeliac');

-- Dietary bits
--0000 = none
--0001 = vegetarian
--0011 = vegan
--0100 = gluten
--1000 = dairy

-- cook time stored in minutes
DROP TABLE IF EXISTS Recipe CASCADE;
CREATE TABLE Recipe (
    id          integer,
    name        varchar(256) not null,
    time        integer,
    difficulty  Difficulty,
    serving     integer,
    notes       text,
    description text,
    cuisine_tags text,
    dietary_tags bit(4),
    imageRef    text default null,
    url         text,
    method      text,
    primary key (id)
);

-- Priority is the importance of the ingredient for cooking
DROP TABLE IF EXISTS Ingredient CASCADE;
CREATE TABLE Ingredient (
    id          integer,
    name        varchar(256),
    measurement_type    MeasurementTypes,
    primary key (id)
);

DROP TABLE IF EXISTS RecipeToIngredient CASCADE;
CREATE TABLE RecipeToIngredient (
    recipe              integer references Recipe(id),
    ingredient          integer references Ingredient(id),
    quantity            numeric,
    r_quantity          numeric,
    r_measurement_type  Recipe_MeasurementTypes,
    description         text,
    notes               text,
    optional            boolean,
    primary key         (recipe, ingredient, quantity)
);

DROP TABLE IF EXISTS Equipment CASCADE;
CREATE TABLE Equipment (
    id          integer,
    name        varchar(256),
    primary key (id)
);

-- relationship between recipe and equipment
DROP TABLE IF EXISTS RecipeToEquipment;
CREATE Table RecipeToEquipment (
    recipe      integer references Recipe(id),
    equipment   integer references Equipment(id)
);

DROP TABLE IF EXISTS Account CASCADE;
CREATE TABLE Account (
    username    varchar(32),
    pwhash      bytea,
    pwsalt      bytea,
    details     text,
    primary key (username)
);

DROP TABLE IF EXISTS ShoppingList;
CREATE TABLE ShoppingList (
    account     varchar(32) references Account(username),
    recipe      integer references Recipe(id),
    ingredient  integer references Ingredient(id),
    quantity    integer,
    primary key (account, recipe, ingredient)
);


-- no measurement type associated in pantry
-- measurement type associated with ingredient
DROP TABLE IF EXISTS Pantry;
CREATE TABLE Pantry (
    account     varchar(32) references Account(username),
    ingredient  integer references Ingredient(id),
    quantity    integer,
    primary key (account, ingredient)
);

DROP TABLE IF EXISTS DietInfo;
CREATE TABLE DietInfo (
    account     varchar(32) references Account(username),
    diet        varchar(32),
    primary key (account, diet)
);

DROP TABLE IF EXISTS Favourites;
CREATE TABLE Favourites (
    account     varchar(32) references Account(username),
    recipe      integer references Recipe(id),
    primary key (account, recipe)
);

DROP TABLE IF EXISTS Recipe_Votes CASCADE;
CREATE TABLE Recipe_Votes (
    account     varchar(32) references Account(username),
    recipe      integer references Recipe(id),
    is_like     boolean,
    primary key (account, recipe)
);

-- modifications made to the database to assist with SQL queries
CREATE OR REPLACE VIEW compulsory_recipetoingredient as
select *
from recipetoingredient
where optional = 'false'
;

DROP VIEW IF EXISTS ingredient_counts;
CREATE VIEW ingredient_counts AS
SELECT
  rtoi.recipe,
  count(rtoi.recipe) AS ingredient_count,
  count(rtoi.recipe) - sum(rtoi.optional::int) AS compulsory_ingredient_count
FROM
  recipetoingredient rtoi
GROUP BY
  rtoi.recipe
;

CREATE OR REPLACE VIEW recipe_rating AS
SELECT
  rv.recipe,
  sum(rv.is_like::integer)::float / count(rv.recipe)::float AS rating
FROM Recipe_Votes rv
GROUP BY rv.recipe
;
