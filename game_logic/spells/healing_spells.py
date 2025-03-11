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
        regen_percent: float = 0.0,  # Percentage of max HP to heal per turn
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
        self.regen_percent = regen_percent

    def calculate_effect(self, caster) -> SpellEffect:
        """Calculate healing amount and potential regen effect"""
        # Get the base healing calculation from WhiteMagicSpell
        effect = super().calculate_effect(caster)
        
        # Add regeneration status effect if applicable
        if self.regen_chance > 0:
            # Store the percentage in the potency field
            # The battle system will use this as a percentage of max_hp
            regen_effect = StatusEffect(
                status=Status.REGEN,
                duration=3,  # Lasts 3 turns
                potency=int(self.regen_percent * 100),  # Store as percentage * 100 for easier reading
                chance=self.regen_chance
            )
            effect.status_effects.append(regen_effect)
        
        return effect
    
# HEALING SPELLS

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
            regen_chance=0.25,     # 25% chance to apply regen
            regen_percent=0.05,    # Heals 5% of max HP per turn
            description="Restores moderate HP with a chance to regenerate 5% HP per turn"
        )

class Curaga(CureSpell):
    """High-tier healing spell"""
    def __init__(self):
        super().__init__(
            name="Curaga",
            mp_cost=20,
            base_healing=120,
            regen_chance=0.4,      # 40% chance to apply regen
            regen_percent=0.10,    # Heals 10% of max HP per turn
            description="Restores significant HP with a chance to regenerate 10% HP per turn"
        )

# REGEN SPELLS
        
class Regen(CureSpell):
    """Applies the regen status effect to the target"""
    def __init__(self):
        super().__init__(
            name="Regen",
            mp_cost=25,
            regen_chance=1.0,
            regen_percent=0.10,
            description="Applies the regen status effect to the target, which heals 10% max HP per turn"
        )

class HighRegen(CureSpell):
    """Applies the high regen status effect to the target"""
    def __init__(self):
        super().__init__(
            name="High Regen",
            mp_cost=35,
            regen_chance=1.0,
            regen_percent=0.20,
            description="Applies the high regen status effect to the target, which heals 20% max HP per turn"
        )

class MassRegen(CureSpell):
    """Applies the regen status effect to all allies"""
    def __init__(self):
        super().__init__(
            name="Mass Regen",
            mp_cost=80,
            regen_chance=1.0,
            regen_percent=0.20,
            description="Applies the high regen status effect to all allies, which heals 20% max HP per turn"
        )

# NULLIFY SPELLS

class NullifySpell(WhiteMagicSpell):
    """Base class for spells that nullify specific damage types"""
    def __init__(
        self,
        name: str,
        mp_cost: int,
        nullify_status: Status,
        description: str
    ):
        super().__init__(
            name=name,
            mp_cost=mp_cost,
            base_healing=0,
            description=description,
            targeting="ally"
        )
        self.nullify_status = nullify_status

    def calculate_effect(self, caster) -> SpellEffect:
        """Apply the nullify status effect"""
        effect = SpellEffect()
        
        # Create nullify status effect that lasts until triggered
        nullify_effect = StatusEffect(
            status=self.nullify_status,
            duration=-1,  # -1 means until triggered
            potency=1,    # Will block 1 instance
            chance=1.0    # Always applies
        )
        
        effect.status_effects.append(nullify_effect)
        return effect

class NulBlaze(NullifySpell):
    """Nullifies one instance of fire damage"""
    def __init__(self):
        super().__init__(
            name="Nul Blaze",
            mp_cost=10,
            nullify_status=Status.NULLIFY_FIRE,
            description="Nullifies one instance of fire damage"
        )

class NulFrost(NullifySpell):
    """Nullifies one instance of ice damage"""
    def __init__(self):
        super().__init__(
            name="Nul Frost",
            mp_cost=10,
            nullify_status=Status.NULLIFY_ICE,
            description="Nullifies one instance of ice damage"
        )

class NulThunder(NullifySpell):
    """Nullifies one instance of thunder damage"""
    def __init__(self):
        super().__init__(
            name="Nul Thunder",
            mp_cost=10,
            nullify_status=Status.NULLIFY_THUNDER,
            description="Nullifies one instance of thunder damage"
        )

class NulWater(NullifySpell):
    """Nullifies one instance of water damage"""
    def __init__(self):
        super().__init__(
            name="Nul Water",
            mp_cost=10,
            nullify_status=Status.NULLIFY_WATER,
            description="Nullifies one instance of water damage"
        )

# STATUS CURE SPELLS

class Esuna(WhiteMagicSpell):
    """Cures all status effects from the target"""
    def __init__(self):
        super().__init__(
            name="Esuna",
            mp_cost=5
            
        )

class Revive(WhiteMagicSpell):
    """Revives the target from death"""
    def __init__(self):
        super().__init__(
            name="Revive",
            mp_cost=18
            
        )

class MassRevive(WhiteMagicSpell):
    """Revives all allies from death"""
    def __init__(self):
        super().__init__(
            name="Mass Revive",
            mp_cost=60
            
        )

class Dispel(WhiteMagicSpell):
    """Removes all status effects from the target"""
    def __init__(self):
        super().__init__(
            name="Dispel",
            mp_cost=12,
            targeting="enemy"
        )

class MassDispel(WhiteMagicSpell):
    """Removes all status effects from all allies"""
    def __init__(self):
        super().__init__(
            name="Mass Dispel",
            mp_cost=35,
            targeting="enemy"
        )

# BUFF/DEBUFF SPELLS

class Haste(WhiteMagicSpell):
    """Increases the speed of the target"""
    def __init__(self):
        super().__init__(
            name="Haste",
            mp_cost=8
        )

class MassHaste(WhiteMagicSpell):
    """Increases the speed of all allies"""
    def __init__(self):
        super().__init__(
            name="Mass Haste",
            mp_cost=30
        )

class Slow(WhiteMagicSpell):
    """Decreases the speed of the target"""
    def __init__(self):
        super().__init__(
            name="Slow",
            mp_cost=8,
            targeting="enemy"
        )

class MassSlow(WhiteMagicSpell):
    """Decreases the speed of all enemies"""
    def __init__(self):
        super().__init__(
            name="Mass Slow",
            mp_cost=30,
            targeting="enemy"
        )

class Shell(WhiteMagicSpell):
    """Halves magic damage applied to the target"""
    def __init__(self):
        super().__init__(
            name="Shell",
            mp_cost=10,
        )

class Protect(WhiteMagicSpell):
    """Halves physical damage applied to the target"""
    def __init__(self):
        super().__init__(
            name="Protect",
            mp_cost=10
        )

class Reflect(WhiteMagicSpell):
    """Reflects magic damage back to the caster"""
    def __init__(self):
        super().__init__(
            name="Reflect",
            mp_cost=14            
        )

class Barrier(WhiteMagicSpell):
    """Blocks physical damage from the target"""
    def __init__(self):
        super().__init__(
            name="Barrier",
            mp_cost=14 
        )

