from . import db

def get_num_likes(recipe_id):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                '''SELECT count(*) FROM recipe_votes WHERE recipe=%s AND is_like IS TRUE;''',
                (recipe_id,)
            )
            return cursor.fetchone()[0]

def get_num_dislikes(recipe_id):
    with db.getconn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                '''SELECT count(*) FROM recipe_votes WHERE recipe=%s AND is_like IS FALSE;''',
                (recipe_id,)
            )
            return cursor.fetchone()[0]

# Returns an integer percentage, or None if there are no likes yet
def get_rating(recipe_id):
    n_likes    = get_num_likes(recipe_id)
    n_dislikes = get_num_dislikes(recipe_id)
    total      = n_likes + n_dislikes
    if total == 0:
        return None
    else:
        return int(100 * float(n_likes) / float(total))

