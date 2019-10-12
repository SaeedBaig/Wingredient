-- method is an array of text outlining the steps of the recipe
-- imageRef holds a file path to an image
-- 
CREATE TABLE Recipe (
    id          integer,
    name        varchar(256) not null,
    time        time(HH:MM),
    difficulty  Difficulty,
    method      text[],
    notes       text,
    description text,
    imageRef   text default null,
    primary key (id)
);

CREATE TYPE Difficulty as ENUM('Easy', 'Intermediate', 'Hard');

-- Priority is the importance of the ingredient for cooking
CREATE TABLE Ingredient (
    id          integer,
    name        varchar(256),
    isMeat      boolean,
    dietary     DietaryTraits,
    priority    integer,
    primary key (id)
);

-- Enum for different dietary traits
CREATE TYPE DietaryTraits as ENUM('Vegan', 'Vegetarian', 'Caeliac');

CREATE TABLE RecipeToIngredient (
    recipe              integer references Recipe(id),
    ingredient          integer references Ingredient(id),
    quantity            integer,
    optional            boolean,
    measurement_type    MeasurementTypes,
    primary key         (recipe, ingredient, quantity)
);

CREATE TYPE MeasurementTypes as ENUM('Weight', 'Capacity', 'Count')

CREATE TABLE Equipment (
    id          integer,
    name        varchar(256),
    primary key (id)
);

-- relationship between recipe and equipment
CREATE Table RecipeToEquipment (
    recipe      integer references Recipe(id),
    equipment   integer references Equipment(id),
);

CREATE TABLE Account (
    id          integer,
    username    varchar(256),
    password    varchar(256),
    details     text,
    primary key (id)
);

CREATE TABLE ShoppingList (
    user        integer references Account(id),
    ingredient  integer references Ingredient(id),
    quantity    integer,
    primary key (user, ingredient)
);

CREATE TABLE Pantry (
    user        integer references Account(id),
    ingredient  integer references Ingredient(id),
    quantity    integer,
    primary key (user, ingredient)
);

CREATE TABLE Favourites (
    user        integer references Account(id),
    recipe      integer references Recipe(id),
    primary key (user, recipe)
);

CREATE TABLE Likes (
    user        integer references Account(id),
    recipe      integer references Recipe(id),
    primary key (user, recipe)
);

CREATE TABLE Dislikes (
    user        integer references Account(id),
    recipe      integer references Recipe(id),
    primary key (user, recipe)
);


