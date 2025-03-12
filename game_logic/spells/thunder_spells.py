"""Lightning-based spell implementations."""

from .base import BlackMagicSpell, SpellEffect, Status, StatusEffect, DamageType
from random import randrange

class ThunderSpell(BlackMagicSpell):
    """Base class for lightning-element spells with paralyze effect"""
    
    def __init__(
        self,
        name: str,
        mp_cost: int,
        base_power: int,
        paralyze_chance: float,
        description: str
    ):
        super().__init__(
            name=name,
            mp_cost=mp_cost,
            base_power=base_power,
            description=description,
            targeting="enemy",
            damage_type=DamageType.THUNDER
        )
        self.paralyze_chance = paralyze_chance
        self.paralyze_duration = randrange(1, 3)  # Generate random duration here

    def calculate_effect(self, caster, target) -> SpellEffect:
        """Calculate lightning damage and potential paralyze effect"""
        effect = super().calculate_effect(caster, target)
        
        paralyze_effect = StatusEffect(
            status=Status.PARALYZE,
            duration=self.paralyze_duration,
            chance=self.paralyze_chance
        )
        effect.status_effects.append(paralyze_effect)
        return effect

class Thunder(ThunderSpell):
    """Basic thunder spell"""
    def __init__(self):
        super().__init__(
            name="Thunder",
            mp_cost=4,
            base_power=20,
            paralyze_chance=0.1,
            description="Thunder spell which hits an enemy, low paralyze chance"
        )

class Thundara(ThunderSpell):
    """"""