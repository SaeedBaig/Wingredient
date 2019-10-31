-- modifications made to the database to assist with SQL queries
CREATE OR REPLACE VIEW compulsory_recipetoingredient as
select *
from recipetoingredient
where optional = 'false'
;


CREATE OR REPLACE VIEW ingredient_counts as
select recipe, count(recipe)
from compulsory_recipetoingredient
group by recipe
;