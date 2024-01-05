import json

with open('data/item_combinations.json', 'r') as f:
    item_combinations = json.load(f)

def calculate_score(probabilities, units, compositions, items):
    scores = {}

    # Iterate over each composition
    for composition in compositions['compositions']:
        unit_score = 0
        max_unit_score = 0

        # Iterate over each unit in the composition
        for unit in composition['champions']:
            # Add the unit's probability to the score
            if unit['name'] in units:
                unit_score += 1
            else:
                unit_score += probabilities[unit['name']]


            # Update the maximum possible scores
            max_unit_score += 1  # Each unit contributes 1 to the max unit score

        # Normalize the scores to percentages
        unit_score /= max_unit_score
        items_dict = {item['name']: item for item in items}
        # First, create as many BIS items as possible for all units
        total_item_score, total_bis_items = create_items_for_units(composition['champions'], items_dict, 'BIS')

        # Then, create acceptable items for all units if there's still "space" for them
        total_item_score_acc, _ = create_items_for_units(composition['champions'], items_dict, 'ACC')
        total_item_score += total_item_score_acc

        comp_item_score = total_item_score / (total_bis_items * 2)

        # Store the composition's scores
        scores[composition['name']] = unit_score, comp_item_score

    return scores


def create_item(item, items_dict):
    # Check if we can create the item
    components = item_combinations.get(item)
    if components and all(items_dict.get(component, {}).get('count', 0) >= components.count(component) for component in components):
        # If we can create the item, update the counts
        for component in components:
            items_dict[component]['count'] -= 1
        if item in items_dict:
            items_dict[item]['count'] += 1
        else:
            items_dict[item] = {'name': item, 'count': 1}
        return True
    return False
def create_items_for_units(units, items_dict, item_type):
    total_item_score = 0
    total_bis_items = 0

    for unit in units:
        # Get the unit's BIS items or acceptable items
        items = unit['BIS_items'] if item_type == 'BIS' else unit['acceptable_items']
        # Initialize the item score
        item_score = 0

        # Try to create each item
        for item in items:
            if item_score < 6 or item_type == 'BIS':  # Only try to create items if less than 3 items have been added, or if they are BIS items
                if items_dict.get(item, {}).get('count', 0) > 0 or create_item(item, items_dict):
                    items_dict[item]['count'] -= 1
                    item_score += 2 if item_type == 'BIS' else 1

        total_item_score += item_score
        total_bis_items += len(unit['BIS_items'])

    return total_item_score, total_bis_items

