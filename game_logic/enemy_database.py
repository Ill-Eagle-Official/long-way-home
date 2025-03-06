"""
Enemy database for the JRPG battle system.
Contains enemy templates and functions for generating and scaling enemies.
"""

# Base stats for each enemy type
ENEMY_DATABASE = {
    "Goblin": {
        "base_stats": {
            "hp": 400,
            "mp": 40,
            "strength": 15,
            "defense": 10,
            "magic": 8,
            "magic_defense": 8,
            "agility": 10,
            "luck": 10
        },
        "stat_multiplier": 0.8,  # Weaker enemy
        "special_move": "Frenzy",
        "description": "A weak but agile creature that often attacks in groups.",
        "exp_value": 50,  # Base experience points for defeating this enemy
        "abilities": ["Attack", "Frenzy"],
        "drops": ["Potion", "Small Gem"]  # Potential item drops (for future implementation)
    },
    "Wolf": {
        "base_stats": {
            "hp": 450,
            "mp": 30,
            "strength": 18,
            "defense": 12,
            "magic": 5,
            "magic_defense": 8,
            "agility": 15,
            "luck": 12
        },
        "stat_multiplier": 1.0,  # Balanced enemy
        "special_move": "Howl",
        "description": "A fierce predator with high strength and agility.",
        "exp_value": 65,
        "abilities": ["Attack", "Howl"],
        "drops": ["Beast Fang", "Wolf Pelt"]
    },
    "Ogre": {
        "base_stats": {
            "hp": 600,
            "mp": 20,
            "strength": 22,
            "defense": 15,
            "magic": 3,
            "magic_defense": 5,
            "agility": 8,
            "luck": 8
        },
        "stat_multiplier": 1.2,  # Stronger enemy
        "special_move": "Smash",
        "description": "A powerful brute with high HP and strength.",
        "exp_value": 80,
        "abilities": ["Attack", "Smash"],
        "drops": ["Large Gem", "Ogre Bone"]
    },
    "Sahagin": {
        "base_stats": {
            "hp": 425,
            "mp": 45,
            "strength": 16,
            "defense": 12,
            "magic": 12,
            "magic_defense": 10,
            "agility": 12,
            "luck": 10
        },
        "stat_multiplier": 0.9,
        "special_move": "Water Splash",
        "description": "An aquatic creature skilled in both physical and magical attacks.",
        "exp_value": 60,
        "abilities": ["Attack", "Water Splash"],
        "drops": ["Fish Scale", "Water Gem"]
    },
    "Dark Elemental": {
        "base_stats": {
            "hp": 350,
            "mp": 80,
            "strength": 8,
            "defense": 8,
            "magic": 20,
            "magic_defense": 18,
            "agility": 10,
            "luck": 12
        },
        "stat_multiplier": 1.1,
        "special_move": "Dark Burst",
        "description": "A magical entity with powerful dark spells.",
        "exp_value": 75,
        "abilities": ["Attack", "Dark Burst"],
        "drops": ["Dark Matter", "Spirit Shard"]
    }
}

def get_scaled_enemy_stats(enemy_name, player_level):
    """
    Get enemy stats scaled based on player level.
    
    Args:
        enemy_name (str): Name of the enemy to generate
        player_level (int): Current level of the player
        
    Returns:
        dict: Scaled stats for the enemy
        
    Raises:
        KeyError: If enemy_name is not found in the database
    """
    if enemy_name not in ENEMY_DATABASE:
        raise KeyError(f"Enemy '{enemy_name}' not found in database")
        
    enemy_data = ENEMY_DATABASE[enemy_name]
    base_stats = enemy_data["base_stats"]
    stat_mult = enemy_data["stat_multiplier"]
    
    # Scale stats based on player level and enemy's base multiplier
    level_scaling = 1 + (player_level - 1) * 0.1
    
    scaled_stats = {}
    for stat, value in base_stats.items():
        scaled_stats[stat] = int(value * stat_mult * level_scaling)
    
    return {
        "name": enemy_name,
        "stats": scaled_stats,
        "special_move": enemy_data["special_move"],
        "exp_value": int(enemy_data["exp_value"] * level_scaling),
        "abilities": enemy_data["abilities"].copy(),
        "drops": enemy_data["drops"].copy()
    }

def get_random_enemy(player_level, exclude=None):
    """
    Get a random enemy from the database with scaled stats.
    
    Args:
        player_level (int): Current level of the player
        exclude (list, optional): List of enemy names to exclude from selection
        
    Returns:
        dict: Enemy data with scaled stats
    """
    import random
    
    available_enemies = list(ENEMY_DATABASE.keys())
    if exclude:
        available_enemies = [e for e in available_enemies if e not in exclude]
    
    enemy_name = random.choice(available_enemies)
    return get_scaled_enemy_stats(enemy_name, player_level)

def get_enemy_description(enemy_name):
    """
    Get the description of an enemy.
    
    Args:
        enemy_name (str): Name of the enemy
        
    Returns:
        str: Description of the enemy
        
    Raises:
        KeyError: If enemy_name is not found in the database
    """
    if enemy_name not in ENEMY_DATABASE:
        raise KeyError(f"Enemy '{enemy_name}' not found in database")
    
    return ENEMY_DATABASE[enemy_name]["description"] 