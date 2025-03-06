"""
Character templates and base stats for different character classes.
"""

CHARACTER_TEMPLATES = {
    'warrior': {
        'name': 'Warrior',
        'hp': 840,
        'mp': 56,
        'strength': 20,
        'defense': 15,
        'magic': 5,
        'magic_defense': 10,
        'agility': 12,
        'luck': 15,
        'description': 'A strong physical fighter with high HP and strength.',
        'abilities': ["Cheer", "Provoke"],
        'skills': ["Power Break", "Armor Break"],
        'black_magic': [],
        'white_magic': []
    },
    'mage': {
        'name': 'Black Mage',
        'hp': 572,
        'mp': 84,
        'strength': 8,
        'defense': 8,
        'magic': 22,
        'magic_defense': 18,
        'agility': 10,
        'luck': 17,
        'description': 'A powerful spellcaster with high magic and MP.',
        'abilities': [],
        'skills': [],
        'black_magic': ["Fire", "Thunder", "Blizzard"],
        'white_magic': ["Cure"]
    },
    'rogue': {
        'name': 'Thief',
        'hp': 690,
        'mp': 70,
        'strength': 15,
        'defense': 10,
        'magic': 10,
        'magic_defense': 12,
        'agility': 25,
        'luck': 20,
        'description': 'An agile fighter with high speed and luck.',
        'abilities': ["Steal"],
        'skills': ["Dark Attack", "Flee"],
        'black_magic': [],
        'white_magic': []
    }
}

def get_character_template(character_type):
    """
    Get the template for a specific character class.
    
    Args:
        character_type (str): The type of character to get template for
        
    Returns:
        dict: Character template with base stats and abilities
        
    Raises:
        KeyError: If character_type is not found
    """
    if character_type not in CHARACTER_TEMPLATES:
        raise KeyError(f"Character type '{character_type}' not found")
    return CHARACTER_TEMPLATES[character_type].copy() 