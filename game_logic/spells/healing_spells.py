"""
Healing-base spell implementation.
"""

import random
from .base import Spell, SpellType, SpellEffect

class HealingSpell(Spell):
    """Base class for healing spells"""

    def __init__(
        self,
        name: str,
        mp_cost: int,
        base_healing: int,
        description: str
    ):
        super().__init__(
            name=name,
            mp_cost=mp_cost,
            spell_type=SpellType.WHITE_MAGIC,
            base_power=base_healing,
            description=description,
            targeting="ally")
        
    def calculate_effect(self, caster) -> SpellEffect:
        """Calculate healing amount based on caster's magic stat"""
        raw_healing = self.base_healing + ([caster.magic**2 / 6] + self.base_healing) + 4
        final_healing = int(raw_healing * (0.8 + (0.4 * random.random())))

        return SpellEffect(healing=final_healing)
    
class Cure(HealingSpell):
    """Basic healing spell"""
    def __init__(self):
        super().__init__(
            name="Cure",
            mp_cost=4,
            base_healing=24,
            description="Minor heal for one ally."
        )

class Cura(HealingSpell):
    """Mid-level healing spell"""
    def __init__(self):
        super().__init__(
            name="Cura",
            mp_cost=10,
            base_healing=40,
            description="Heal one ally with moderate healing."
        )
        
class Curaga(HealingSpell):
    """Heal all allies"""
    def __init__(self):
        super().__init__(
            name="Curaga",
            mp_cost=20,
            base_healing=80,
            description="Heal all allies with high healing."
        )
        
        
