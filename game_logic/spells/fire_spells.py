"""
Fire-based spell implementations.
"""

import random
from .base import Spell, SpellType, SpellEffect, Status, StatusEffect

class FireSpell(Spell):
    """Base class for fire-element spells with burn effect"""
    
    def __init__(
        self,
        name: str,
        mp_cost: int,
        base_power: int,
        burn_chance: float,
        burn_potency: int,
        description: str
    ):
        super().__init__(
            name=name,
            mp_cost=mp_cost,
            spell_type=SpellType.BLACK_MAGIC,
            base_power=base_power,
            description=description,
            targeting="enemy"
        )
        self.burn_chance = burn_chance
        self.burn_potency = burn_potency

    def calculate_effect(self, caster, target) -> SpellEffect:
        """Calculate fire damage and potential burn effect"""
        # Calculate base magic damage
        raw_damage = (self.base_power * caster.magic) / target.magic_defense
        # Add some randomness (±10%)
        final_damage = int(raw_damage * (0.9 + (0.2 * random.random())))
        
        # Create burn status effect
        burn_effect = StatusEffect(
            status=Status.BURN,
            duration=3,  # Lasts 3 turns
            potency=self.burn_potency,
            chance=self.burn_chance
        )
        
        return SpellEffect(
            damage=final_damage,
            status_effects=[burn_effect]
        )

class Fire(FireSpell):
    """Basic fire spell"""
    def __init__(self):
        super().__init__(
            name="Fire",
            mp_cost=4,
            base_power=20,
            burn_chance=0.2,  # 20% chance to burn
            burn_potency=2,   # 2 damage per turn if burned
            description="Deals fire damage with a small chance to burn"
        )

class Fira(FireSpell):
    """Medium-tier fire spell"""
    def __init__(self):
        super().__init__(
            name="Fira",
            mp_cost=12,
            base_power=45,
            burn_chance=0.35,  # 35% chance to burn
            burn_potency=4,    # 4 damage per turn if burned
            description="Deals moderate fire damage with a moderate chance to burn"
        )

class Firaga(FireSpell):
    """High-tier fire spell"""
    def __init__(self):
        super().__init__(
            name="Firaga",
            mp_cost=24,
            base_power=85,
            burn_chance=0.5,   # 50% chance to burn
            burn_potency=8,    # 8 damage per turn if burned
            description="Deals heavy fire damage with a high chance to burn"
        ) 