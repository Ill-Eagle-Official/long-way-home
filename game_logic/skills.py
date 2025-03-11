"""
Definitions for skills, abilities, and magic in the game.
Includes MP costs, effects, and targeting information.
"""

# MP costs for different actions
SKILL_COSTS = {
    # Basic abilities (no MP cost)
    'Cheer': 0,
    'Provoke': 0,
    'Steal': 0,
    
    # Skills
    'Power Break': 10,
    'Armor Break': 10,
    'Dark Attack': 8,
    'Flee': 4,
    
    # Black Magic
    'Fire': 4,
    'Thunder': 4,
    'Blizzard': 4,

    # White Magic
    'Cure': 4
}

# Spell power for magic spells
SPELL_POWER = {
    'Fire': 20,
    'Thunder': 20,
    'Blizzard': 20
}

# Special move data for enemies
SPECIAL_MOVES = {
    'Frenzy': {
        'power': 1.5,
        'description': 'A powerful attack with increased damage'
    },
    'Howl': {
        'power': 1.5,
        'description': 'A fierce howl that deals heavy damage'
    },
    'Smash': {
        'power': 1.8,
        'description': 'A devastating attack that can break defenses'
    },
    'Water Splash': {
        'power': 1.4,
        'description': 'A water-based attack with moderate damage'
    },
    'Dark Burst': {
        'power': 1.6,
        'description': 'A burst of dark energy that deals magical damage'
    }
}

def get_skill_cost(skill_name):
    """
    Get the MP cost for a skill or spell.
    
    Args:
        skill_name (str): Name of the skill
        
    Returns:
        int: MP cost of the skill (0 if not found)
    """
    return SKILL_COSTS.get(skill_name, 0)

def get_spell_power(spell_name):
    """
    Get the base power for a magic spell.
    
    Args:
        spell_name (str): Name of the spell
        
    Returns:
        int: Base power of the spell (0 if not found)
    """
    return SPELL_POWER.get(spell_name, 0)

def get_special_move_power(move_name):
    """
    Get the power multiplier for a special move.
    
    Args:
        move_name (str): Name of the special move
        
    Returns:
        float: Power multiplier for the move (1.0 if not found)
    """
    move_data = SPECIAL_MOVES.get(move_name, {})
    return move_data.get('power', 1.0) 