-- method is an array of text outlining the steps of the recipe
-- imageRef holds a file path to an image
DROP TYPE IF EXISTS MeasurementTypes CASCADE;
CREATE TYPE MeasurementTypes as ENUM('Weight', 'Volume', 'Count');

DROP TYPE IF EXISTS Difficulty CASCADE;
CREATE TYPE Difficulty as ENUM('Easy', 'Intermediate', 'Hard');

-- Enum for different dietary traits
DROP TYPE IF EXISTS DietaryTraits CASCADE;
CREATE TYPE DietaryTraits as ENUM('None', 'Vegan', 'Vegetarian', 'Caeliac');

-- cook time stored in minutes
DROP TABLE IF EXISTS Recipe CASCADE;
CREATE TABLE Recipe (
    id          integer,
    name        varchar(256) not null,
    time        integer,
    difficulty  Difficulty,
    method      text[],
    notes       text,
    description text,
    imageRef   text default null,
    primary key (id)
);

-- Priority is the importance of the ingredient for cooking
DROP TABLE IF EXISTS Ingredient CASCADE;
CREATE TABLE Ingredient (
    id          integer,
    name        varchar(256),
    isMeat      boolean,
    dietary     DietaryTraits,
    primary key (id)
);

DROP TABLE IF EXISTS RecipeToIngredient;
CREATE TABLE RecipeToIngredient (
    recipe              integer references Recipe(id),
    ingredient          integer references Ingredient(id),
    quantity            integer,
    optional            boolean,
    measurement_type    MeasurementTypes,
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
    id          integer,
    username    varchar(256),
    password    varchar(256),
    details     text,
    primary key (id)
);

DROP TABLE IF EXISTS ShoppingList;
CREATE TABLE ShoppingList (
    account     integer references Account(id),
    ingredient  integer references Ingredient(id),
    quantity    integer,
    primary key (account, ingredient)
);

DROP TABLE IF EXISTS Pantry;
CREATE TABLE Pantry (
    account     integer references Account(id),
    ingredient  integer references Ingredient(id),
    quantity    integer,
    primary key (account, ingredient)
);

DROP TABLE IF EXISTS Favourites;
CREATE TABLE Favourites (
    account     integer references Account(id),
    recipe      integer references Recipe(id),
    primary key (account, recipe)
);

DROP TABLE IF EXISTS Likes;
CREATE TABLE Likes (
    account     integer references Account(id),
    recipe      integer references Recipe(id),
    primary key (account, recipe)
);

DROP TABLE IF EXISTS Dislikes;
CREATE TABLE Dislikes (
    account     integer references Account(id),
    recipe      integer references Recipe(id),
    primary key (account, recipe)
);