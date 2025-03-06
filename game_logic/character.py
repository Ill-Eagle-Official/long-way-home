class Character:
    """
    Represents a character in the game (either player or enemy).
    Handles stats, abilities, and combat calculations using Final Fantasy X-style mechanics.
    """
    
    def __init__(self, name, hp, mp, strength, defense, magic, magic_defense, agility, luck):
        """
        Initialize a character with their base stats.
        
        Args:
            name (str): Character's name
            hp (int): Hit Points - determines how much damage they can take
            mp (int): Magic Points - used for special abilities and spells
            strength (int): Physical attack power
            defense (int): Physical damage resistance
            magic (int): Magical attack power
            magic_defense (int): Magical damage resistance
            agility (int): Affects turn order and critical hit chance
            luck (int): Affects critical hits and special events
        """
        # Basic stats
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.max_mp = mp
        self.current_mp = mp
        self.strength = strength
        self.defense = defense
        self.magic = magic
        self.magic_defense = magic_defense
        self.agility = agility
        self.luck = luck
        self.level = 1
        self.experience = 0
        
        # Initialize skill lists for different ability types
        self.abilities = []  # Special abilities like "Cheer", "Provoke"
        self.skills = []     # Skills like "Dark Attack", "Power Break"
        self.black_magic = [] # Offensive magic
        self.white_magic = [] # Healing and support magic
        
        # Enemy-specific attributes
        self.special_move = None  # Special move for enemies
        self.exp_value = 0       # Experience points awarded when defeated
        self.drops = []          # Potential item drops
        
        # Set initial abilities based on character type
        self._init_abilities()
    
    def _init_abilities(self):
        """
        Initialize character-specific abilities based on their class/role.
        Each character type gets a unique set of abilities.
        """
        if self.name == "Warrior":
            self.abilities = ["Cheer", "Provoke"]
            self.skills = ["Power Break", "Armor Break"]
        elif self.name == "Black Mage":
            self.black_magic = ["Fire", "Thunder", "Blizzard"]
            self.white_magic = ["Cure"]
        elif self.name == "Thief":
            self.abilities = ["Steal"]
            self.skills = ["Dark Attack", "Flee"]
    
    def use_mp(self, cost):
        """
        Attempt to use MP for an ability or spell.
        
        Args:
            cost (int): Amount of MP required
            
        Returns:
            bool: True if MP was successfully used, False if not enough MP
        """
        if self.current_mp >= cost:
            self.current_mp -= cost
            return True
        return False
    
    def calculate_magic_damage(self, target, spell_power):
        """
        Calculate magical damage using FFX's formula.
        
        Args:
            target (Character): The target of the spell
            spell_power (int): Base power of the spell
            
        Returns:
            dict: Contains damage amount and whether it was a critical hit
        """
        import random
        # FFX's magic damage formula:
        # [(Magic * 0.8 + Magic_Power * 0.5) * (Random + 1.0) * Modifier] - Magic_Defense * 0.875
        
        base_damage = (self.magic * 0.8 + spell_power * 0.5)
        random_factor = random.uniform(0, 0.25)
        
        # Critical hits are less common with magic
        crit_chance = min(self.luck / 4, 15) / 100
        is_critical = random.random() < crit_chance
        
        modifier = 1.5 if is_critical else 1.0
        
        damage = (base_damage * (1 + random_factor) * modifier) - (target.magic_defense * 0.875)
        
        return {'damage': max(1, int(damage)), 'is_critical': is_critical}
    
    def get_available_actions(self):
        """
        Get all currently available actions for the character.
        Filters out actions that cannot be used due to MP costs.
        
        Returns:
            dict: Dictionary of available actions by category
        """
        actions = {
            'basic': ['attack', 'defend'],
            'abilities': [ability for ability in self.abilities if self._can_use_ability(ability)],
            'skills': [skill for skill in self.skills if self._can_use_skill(skill)],
            'black_magic': [spell for spell in self.black_magic if self._can_use_spell(spell)],
            'white_magic': [spell for spell in self.white_magic if self._can_use_spell(spell)]
        }
        return actions
    
    def _can_use_ability(self, ability):
        """
        Check if an ability can be used (has enough MP).
        
        Args:
            ability (str): Name of the ability
            
        Returns:
            bool: True if the ability can be used
        """
        costs = {
            'Cheer': 0,
            'Provoke': 0,
            'Steal': 0
        }
        return self.current_mp >= costs.get(ability, 0)
    
    def _can_use_skill(self, skill):
        """
        Check if a skill can be used (has enough MP).
        
        Args:
            skill (str): Name of the skill
            
        Returns:
            bool: True if the skill can be used
        """
        costs = {
            'Power Break': 10,
            'Armor Break': 10,
            'Dark Attack': 8,
            'Flee': 4
        }
        return self.current_mp >= costs.get(skill, 0)
    
    def _can_use_spell(self, spell):
        """
        Check if a spell can be used (has enough MP).
        
        Args:
            spell (str): Name of the spell
            
        Returns:
            bool: True if the spell can be used
        """
        costs = {
            'Fire': 4,
            'Thunder': 4,
            'Blizzard': 4,
            'Cure': 4
        }
        return self.current_mp >= costs.get(spell, 0)

    def take_damage(self, damage):
        """
        Apply damage to the character.
        
        Args:
            damage (int): Amount of damage to take
            
        Returns:
            int: Actual damage taken after calculations
        """
        actual_damage = max(1, damage)
        old_hp = self.current_hp
        self.current_hp = max(0, self.current_hp - actual_damage)
        print(f"{self.name} taking {actual_damage} damage: {old_hp} -> {self.current_hp} HP")
        return actual_damage

    def is_alive(self):
        """Check if the character is still alive."""
        alive = self.current_hp > 0
        print(f"Checking if {self.name} is alive: HP={self.current_hp}, result={alive}")
        return alive

    def heal(self, amount):
        """
        Heal the character for a specified amount.
        
        Args:
            amount (int): Amount of HP to restore
        """
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def calculate_damage(self, target):
        """
        Calculate physical damage using FFX's formula.
        
        Args:
            target (Character): The target of the attack
            
        Returns:
            dict: Contains damage amount and whether it was a critical hit
        """
        import random
        
        # FFX's physical damage formula:
        # [(Strength * 0.8 + Level * 0.5) * (Random + 1) * Modifier] - Defense * 0.875
        # where Random is between 0 and 0.25
        
        base_damage = (self.strength * 0.8 + self.level * 0.5)
        random_factor = random.uniform(0, 0.25)
        
        # Critical hit chance based on luck (max 25%)
        crit_chance = min(self.luck / 2, 25) / 100
        is_critical = random.random() < crit_chance
        
        modifier = 1.5 if is_critical else 1.0
        
        # Add weapon bonus (simplified to level-based bonus)
        weapon_bonus = self.level * 0.1
        
        damage = (base_damage * (1 + random_factor) * modifier + weapon_bonus) - (target.defense * 0.875)
        
        final_damage = max(1, int(damage))
        
        return {'damage': final_damage, 'is_critical': is_critical}

    def gain_experience(self, amount):
        """
        Add experience points and level up if necessary.
        
        Args:
            amount (int): Amount of experience to gain
        """
        self.experience += amount
        while self.experience >= 100:
            self.level_up()
            self.experience -= 100

    def level_up(self):
        """
        Increase character level and improve stats.
        Similar to FFX's sphere grid, but simplified to automatic improvements.
        """
        self.level += 1
        self.max_hp += 40
        self.current_hp = self.max_hp
        self.max_mp += 5
        self.current_mp = self.max_mp
        self.strength += 1
        self.defense += 1
        self.magic += 1
        self.magic_defense += 1
        self.agility += 1
        self.luck += 1

    def to_dict(self):
        """
        Convert character state to a dictionary for storage/transmission.
        
        Returns:
            dict: Character's current state
        """
        return {
            'name': self.name,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
            'max_mp': self.max_mp,
            'current_mp': self.current_mp,
            'strength': self.strength,
            'defense': self.defense,
            'magic': self.magic,
            'magic_defense': self.magic_defense,
            'agility': self.agility,
            'luck': self.luck,
            'level': self.level,
            'experience': self.experience,
            'abilities': self.abilities,
            'skills': self.skills,
            'black_magic': self.black_magic,
            'white_magic': self.white_magic,
            'special_move': self.special_move,
            'exp_value': self.exp_value,
            'drops': self.drops
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a character instance from a dictionary.
        
        Args:
            data (dict): Character state data
            
        Returns:
            Character: New character instance with the specified state
        """
        character = cls(
            data['name'],
            data['max_hp'],
            data['max_mp'],
            data['strength'],
            data['defense'],
            data['magic'],
            data['magic_defense'],
            data['agility'],
            data['luck']
        )
        character.current_hp = data['current_hp']
        character.current_mp = data['current_mp']
        character.level = data['level']
        character.experience = data['experience']
        character.abilities = data['abilities']
        character.skills = data['skills']
        character.black_magic = data['black_magic']
        character.white_magic = data['white_magic']
        character.special_move = data.get('special_move')
        character.exp_value = data.get('exp_value', 0)
        character.drops = data.get('drops', [])
        return character 