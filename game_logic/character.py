class Character:
    def __init__(self, name, hp, mp, strength, defense, magic, magic_defense, agility, luck):
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

    def take_damage(self, damage):
        actual_damage = max(1, damage)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def is_alive(self):
        return self.current_hp > 0

    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def calculate_damage(self, target):
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
        
        # Ensure minimum damage is 1
        final_damage = max(1, int(damage))
        
        return {'damage': final_damage, 'is_critical': is_critical}

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= 100:
            self.level_up()
            self.experience -= 100

    def level_up(self):
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
            'experience': self.experience
        }

    @classmethod
    def from_dict(cls, data):
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
        return character 