class Character:
    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.level = 1
        self.experience = 0

    def take_damage(self, damage):
        actual_damage = max(1, damage)  # Remove defense calculation here as it's now in calculate_damage
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def is_alive(self):
        return self.current_hp > 0

    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def calculate_damage(self, target):
        import random
        
        # Base damage formula similar to Final Fantasy:
        # Damage = (Attack * 2 - Defense) * (Level / 32 + 2) * Variance
        
        # Calculate base damage
        base_damage = (self.attack * 2 - target.defense)
        level_modifier = (self.level / 32 + 2)
        base_damage = base_damage * level_modifier
        
        # Add variance (between 0.85 and 1.15)
        variance = random.uniform(0.85, 1.15)
        damage = base_damage * variance
        
        # Critical hit chance (based on speed, max 25%)
        crit_chance = min(self.speed / 2, 25) / 100
        is_critical = random.random() < crit_chance
        
        if is_critical:
            damage *= 1.5  # 50% more damage on critical hits
            
        # Add a small random factor (-5 to +5)
        damage += random.randint(-5, 5)
        
        # Ensure minimum damage is 1
        final_damage = max(1, int(damage))
        
        # Return both the damage and whether it was a critical hit
        return {'damage': final_damage, 'is_critical': is_critical}

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= 100:
            self.level_up()
            self.experience -= 100

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.current_hp = self.max_hp
        self.attack += 2
        self.defense += 1
        self.speed += 1

    def to_dict(self):
        return {
            'name': self.name,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
            'attack': self.attack,
            'defense': self.defense,
            'speed': self.speed,
            'level': self.level,
            'experience': self.experience
        }

    @classmethod
    def from_dict(cls, data):
        character = cls(
            data['name'],
            data['max_hp'],
            data['attack'],
            data['defense'],
            data['speed']
        )
        character.current_hp = data['current_hp']
        character.level = data['level']
        character.experience = data['experience']
        return character 