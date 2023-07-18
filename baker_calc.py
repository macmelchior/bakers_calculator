import pyinputplus as pyip
import shelve


def calculate_amounts(flour_weight, water_perc, starter_perc, salt_perc, starter_type):
    # calculate the amount of water, salt, and starter based on flour amount and return starter amount

    # calculate amounts
    water = round(flour_weight * water_perc / 100)
    starter = round(flour_weight * starter_perc / 100)
    salt = round(flour_weight * salt_perc / 100)

    # deduct liquid starter weight from water weight.
    if starter_type == 'liquid':
        water -= starter

    return water, starter, salt


def calculate_feeding(s_type, s_amount):
    # calculate the amount of old starter, flour, and water needed to prepare starter for the dough
    # s_type - starter type

    # get starter proportions
    starter_proportions = {
        'liquid': (1, 5, 25),
        'regular': (1, 5, 5),
        'stiff': (1, 5, 2.5)
    }
    starter_units, flour_units, water_units = starter_proportions[s_type]

    # get how much one unit weighs
    units = sum([starter_units, flour_units, water_units])
    one_unit = s_amount / units

    # get weights
    starter = round(starter_units * one_unit)
    flour = round(flour_units * one_unit)
    water = round(water_units * one_unit)

    return starter, flour, water


def print_results(flour, water, starter, salt):
    print(f"""
            For the dough, you need:
            {flour} grams of flour,
            {water} grams of water,
            {starter} grams of starter,
            {salt} grams of salt.
""")


def print_feeding_results(old_s, starter_f, starter_w):
    print(f"""
            To feed the starter, you need:
            {old_s} grams of old starter,
            {starter_f} grams of flour,
            {starter_w} grams of water.""")


def save(flour, water, starter, salt, feeding, s_type):
    recipe_name = str(input('Recipe name:\n'))
    content = recipe_name + '\n'
    if feeding == 'yes':
        old_s, starter_f, starter_w = calculate_feeding(s_type, starter)
        content += f"""
    Starter feeding:
    {old_s} grams of old starter,
    {starter_f} grams of flour,
    {starter_w} grams of water.
    """
    content += f"""
    Dough:
    {flour} grams of flour,
    {water} grams of water,
    {starter} grams of starter,
    {salt} grams of salt."""

    with shelve.open('mcb') as mcb_shelf:
        mcb_shelf[recipe_name] = content


def open_recipe():
    recipe_name = str(input('Recipe name:\n'))
    with shelve.open('mcb') as mcb_shelf:
        print(mcb_shelf[recipe_name])


def calculate_recipe():
    flour_weight = int(input('Flour amount in grams: '))
    water_perc = int(input('Water percentage: '))
    starter_perc = int(input('Sourdough starter percentage: '))
    salt_perc = int(input('Salt percentage: '))
    starters = ['liquid', 'regular', 'stiff']
    starter_type = pyip.inputMenu(starters, prompt='Type of starter:\n', numbered=True)
    starter_feeding = pyip.inputYesNo(prompt='Do you need to feed the starter beforehand?\n')

    water_needed, starter_needed, salt_needed = calculate_amounts(flour_weight, water_perc, starter_perc,
                                                                  salt_perc, starter_type)
    if starter_feeding == 'yes':
        old_starter, starter_flour, starter_water = calculate_feeding(starter_type, starter_needed)
        print_feeding_results(old_starter, starter_flour, starter_water)
    print_results(flour_weight, water_needed, starter_needed, salt_needed)

    save_recipe = pyip.inputYesNo('Save the recipe? yes/no:\n')

    if save_recipe:
        save(flour_weight, water_needed, starter_needed, salt_needed, starter_feeding, starter_type)


def main():
    type_of_action = pyip.inputMenu(['Calculate', 'Open recipe'], prompt='What do you want to do?\n', numbered=True)

    if type_of_action == 'Calculate':
        calculate_recipe()

    if type_of_action == 'Open recipe':
        open_recipe()


main()