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
    """Mid-level thunder spell"""
    def __init__(self):
        super().__init__(
            name="Thundara",
            mp_cost=8,
            base_power=45,
            paralyze_chance=0.2,
            description="Thundara spell which hits an enemy, mid paralyze chance"
        )

class Thundaga(ThunderSpell):
    """High-level thunder spell"""
    def __init__(self):
        super().__init__(
            name="Thundaga",
            mp_cost=16,
            base_power=85,
            paralyze_chance=0.3,
            description="Thundaga spell which hits an enemy, high paralyze chance"
        )

class Chainthunder(ThunderSpell):
    """Multi-target thunder spell"""
    def __init__(self):
        super().__init__(
            name="Chain Lightning",
            mp_cost=8,
            base_power=20,
            paralyze_chance=0.1,
            description="Basic thunder spell which hits all enemies, low paralyze chance",
            targeting="all_enemies"
        )

class Chainthundara(ThunderSpell):
    """Multi-target thunder spell"""
    def __init__(self):
        super().__init__(
            name="Chain Thundara",
            mp_cost=16,
            base_power=45,
            paralyze_chance=0.2,
            description="Mid-level thunder spell which hits all enemies, mid paralyze chance",
            targeting="all_enemies"
        )

class Chainthundaga(ThunderSpell):
    """Multi-target thunder spell"""
    def __init__(self):
        super().__init__(
            name="Chain Thundaga",
            mp_cost=32,
            base_power=85,
            paralyze_chance=0.3,
            description="High-level thunder spell which hits all enemies, high paralyze chance",
            targeting="all_enemies"
        )
        
