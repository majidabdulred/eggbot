from discord_slash.utils.manage_commands import create_option, create_choice

options_token = [
    create_option(
        name="tokenid",
        description="ID of the Token",
        option_type=4,
        required=True)]

percent = {'Alien': 0.91, 'Amethyst': 10, 'Angry': 9, 'Anvil': 7, 'Autumn': 10, 'Bald Chicken': 13, 'Beauty': 9,
           'Black': 10, 'Black Hole': 0.51, 'Bloodshot': 9, 'Blue': 15, 'Blue Egg': 3, 'Blue Rooster': 7, 'Bulging': 9,
           'CK-47': 7, 'Candy': 2, 'Cherry Dusk': 0.54, 'Chicken': 24, 'Chickenapult': 8, 'Classic': 0.83,
           'Cockeyed': 9,
           'Cold Snap': 2, 'Coober': 8, 'Crosseyed': 9, 'Determined': 9, 'Devolution': 2, 'Dig': 4, 'Dorking': 45,
           'Eggshell': 13, 'English Mustard': 13, 'Exhausted': 9, 'Eyepatch': 0.85, 'Fan Group': 4, 'Flesh': 9,
           'Flight?': 7, 'Gold': 31, 'Green': 15, 'Growth': 8, 'Helicopter': 4, 'Hen': 50, 'Istanblue': 5, 'Jetpack': 4,
           "Joker's Jade": 10, 'Lakenvelder': 33, 'Lava': 10, 'Lilac': 10, 'Lizard': 0.88, 'Machete': 7,
           'Manic Mint': 10, 'Merah Red': 2, 'Moving Walkway': 2, 'Ocean': 9, 'Orange': "", 'Orange Will': 4,
           'Pink': 10,
           'Purple': 2, 'Purple Wine': 5, 'Red': 15, 'Ring': 0.77, 'Robot': '', 'Rollerblades': 8, 'Rooster': 50,
           'Rose': 2, 'Royal Procession': 0.55, 'Royal Violet': 2, 'Sad': 9, 'Sapphire': 5, 'Screamin Green': 10,
           'Serama': 6, 'Shocked': 9, 'Shocking Pink': 2, 'Sleepy': 9, 'Spicy': 100, 'Spring': 9, 'Stone': 10,
           'Striped Bald Chicken': '', 'Striped Eggshell': '', 'Striped English Mustard': '', 'Striped Istalblue': '',
           "Striped Joker's Jade": '', 'Striped Manic Mint': '', 'Striped Royal Violet': '',
           'Striped Screamin Green': '', 'Striped Shocking Pink': '', 'Striped Wild moss': '', 'Studs': '',
           'Sultan': 16,
           'Summer': 10, 'Teal': 0.27, 'Teleport': 7, 'Vampire': 0.86, 'White': "", 'Wild Moss': 3, 'Winter': 10,
           'Yellow': 31}

trait_list = {'gender': ['Hen', 'Rooster'],
              'heritage': ['Sultan', 'Dorking', 'Lakenvelder', 'Serama'],
              'talent': ['Anvil', 'Fan Group', 'Rollerblades', 'Coober', 'Cold Snap', 'Helicopter', 'Growth', 'CK-47',
                         'Jetpack', 'Blue Rooster', 'Blue Egg', 'Teleport', 'Chickenapult', 'Moving Walkway', 'Machete',
                         'Devolution', 'Dig', 'Flight?', 'Black Hole', 'Royal Procession'],
              'body': ["Joker's Jade", 'Screamin Green', 'Istanblue', 'Manic Mint', 'Eggshell', 'Purple Wine',
                       'English Mustard', 'Wild Moss', 'Bald Chicken', 'Royal Violet', 'Rose', 'Shocking Pink',
                       'Sapphire', 'Orange Will', 'Classic', 'Robot', 'Merah Red', 'Cherry Dusk', 'Black'],
              'stripes': ["Striped Joker's Jade", 'Striped Bald Chicken', 'Striped Manic Mint',
                          'Striped English Mustard', 'Striped Purple Wine', 'Striped Istalblue', 'Striped Royal Violet',
                          'Striped Screamin Green', 'Striped Wild moss', 'Striped Shocking Pink', 'Striped Eggshell',
                          'Striped Sapphire', 'Striped Orange Will', 'Striped Rose', 'Striped Merah Red',
                          'Striped Cherry Dusk'],
              'eye': ['Bulging', 'Bloodshot', 'Shocked', 'Beauty', 'Sleepy', 'Exhausted', 'Determined',
                      'Cockeyed',
                      'Crosseyed', 'Angry', 'Sad', 'Alien', 'Eyepatch', 'Lizard', 'Robot'],
              'beak': ['Vampire', 'Ring'],
              'bg': ['Stone', 'Autumn', 'Summer', 'Winter', 'Flesh', 'Lava', 'Lilac', 'Spring', 'Ocean',
                     'Amethyst'],
              'perfection': ["90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100"]}

options_find = [
    create_option(
        name=category,
        description="Choose one of the options",
        option_type=3,
        required=False,
        choices=[
            create_choice(name=trait, value=trait) for trait in trait_list[category]])
    for category in trait_list.keys()]

