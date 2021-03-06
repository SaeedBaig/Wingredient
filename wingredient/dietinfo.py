# List of allowed diets
allowed_diets = [
    "Vegan",
    "Vegetarian",
    "Dairy-Free",
    "Gluten-Free"
]

allowed_diets_short = {
    "Vegan" : "VGN",
    "Vegetarian" : "VGT",
    "Dairy-Free" : "DF",
    "Gluten-Free" : "GF"
}


def diet_bits_to_names(dietary_tags):
    tags = int(dietary_tags)
    bitmask = 1
    active_diets = []
    for diet in allowed_diets:
        if bitmask & tags:
            active_diets.append(diet)
        bitmask = bitmask << 1
    return active_diets

def diet_bits_to_short_names(dietary_tags):
    return list(map(lambda x: allowed_diets_short[x], diet_bits_to_names(dietary_tags)))
