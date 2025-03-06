"""
Healing-based spell implementations.
"""

import random
from .base import WhiteMagicSpell, SpellEffect, Status, StatusEffect

class CureSpell(WhiteMagicSpell):
    """Base class for cure-type healing spells with regen effect"""
    
    def __init__(
        self,
        name: str,
        mp_cost: int,
        base_healing: int,
        regen_chance: float = 0.0,
        regen_potency: int = 0,
        description: str = ""
    ):
        super().__init__(
            name=name,
            mp_cost=mp_cost,
            base_healing=base_healing,
            description=description,
            targeting="ally"  # Healing spells target allies by default
        )
        self.regen_chance = regen_chance
        self.regen_potency = regen_potency

    def calculate_effect(self, caster) -> SpellEffect:
        """Calculate healing amount and potential regen effect"""
        # Get the base healing calculation from WhiteMagicSpell
        effect = super().calculate_effect(caster)
        
        # Add regeneration status effect if applicable
        if self.regen_chance > 0:
            regen_effect = StatusEffect(
                status=Status.REGEN,
                duration=3,  # Lasts 3 turns
                potency=self.regen_potency,
                chance=self.regen_chance
            )
            effect.status_effects.append(regen_effect)
        
        return effect

class Cure(CureSpell):
    """Basic healing spell"""
    def __init__(self):
        super().__init__(
            name="Cure",
            mp_cost=4,
            base_healing=30,
            description="Restores a small amount of HP"
        )

class Cura(CureSpell):
    """Medium-tier healing spell"""
    def __init__(self):
        super().__init__(
            name="Cura",
            mp_cost=10,
            base_healing=65,
            regen_chance=0.25,  # 25% chance to apply regen
            regen_potency=5,    # Heals 5 HP per turn if regen applies
            description="Restores moderate HP with a chance to apply regeneration"
        )

class Curaga(CureSpell):
    """High-tier healing spell"""
    def __init__(self):
        super().__init__(
            name="Curaga",
            mp_cost=20,
            base_healing=120,
            regen_chance=0.4,   # 40% chance to apply regen
            regen_potency=10,   # Heals 10 HP per turn if regen applies
            description="Restores significant HP with a high chance to apply regeneration"
        )
        
        
