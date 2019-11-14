
# !/bin/bash
# no arguments = prompted for username 
# or
# enter postgresql username as first argument 

if [ -z "$1"]
then
    read -p "Please enter your postgresql username: " username
    THE_USER=$username
else 
    THE_USER=$1
fi

python RecipeWriter.py  
python IngredientWriter.py   
python RecipeToIngredientWriter.py 
#drop and create db
#
psql -d test --user=${THE_USER} -c "\i wingredient-schema.sql" 
psql -d test --user=${THE_USER} -c "\copy recipe FROM 'recipe.csv' DELIMITER ',' CSV HEADER"
psql -d test --user=${THE_USER} -c "\copy ingredient FROM 'ingredient.csv' DELIMITER ',' CSV HEADER"
psql -d test --user=${THE_USER} -c "\copy recipeToIngredient FROM 'recipeToIngredient.csv' DELIMITER ',' CSV HEADER"



