"""
Ice-based spell implementations.
"""

from .base import BlackMagicSpell, SpellEffect, Status, StatusEffect, DamageType

class IceSpell(BlackMagicSpell):
    """Base class for ice-element spells with freeze effect"""
    
    def __init__(
        self,
        name: str,
        mp_cost: int,
        base_power: int,
        freeze_chance: float,
        freeze_duration: int,
        description: str
    ):
        super().__init__(
            name=name,
            mp_cost=mp_cost,
            base_power=base_power,
            description=description,
            targeting="enemy",
            damage_type=DamageType.ICE
        )
        self.freeze_chance = freeze_chance
        self.freeze_duration = freeze_duration

    def calculate_effect(self, caster, target) -> SpellEffect:
        """Calculate ice damage and potential freeze effect"""
        # Get the base damage calculation from BlackMagicSpell
        effect = super().calculate_effect(caster, target)
        
        # Add freeze status effect
        freeze_effect = StatusEffect(
            status=Status.FREEZE, 
            duration=self.freeze_duration,
            chance=self.freeze_chance
        )
        effect.status_effects.append(freeze_effect)
        return effect

# Different tiers of ice spells

class Blizzard(IceSpell):
    """Basic ice spell"""
    def __init__(self):
        super().__init__(
            name="Frost",
            mp_cost=4,
            base_power=20,
            freeze_chance=0.1,
            freeze_duration=2,
            description="Frost spell which hits all enemies"
        )

class Blizzara(IceSpell):
    """Medium-tier ice spell"""
    def __init__(self):
        super().__init__(
            name="Blizzara",
            mp_cost=12,
            base_power=45,
            freeze_chance=0.25,
            freeze_duration=2,
            description="Blizzara spell which hits all enemies"
        )

class Blizzaga(IceSpell):
    """High-tier ice spell"""
    def __init__(self):
        super().__init__(
            name="Blizzaga",
            mp_cost=24,
            base_power=85,
            freeze_chance=0.4,
            freeze_duration=2,
            description="Blizzaga spell which hits all enemies"
        )

class Icywind(IceSpell):
    """Icywind spell"""
    def __init__(self):
        super().__init__(
            name="Icywind", 
            mp_cost=8,
            base_power=20,
            freeze_chance=0.1,
            freeze_duration=2,
            description="Multi-target ice spell",
            targeting="all_enemies"
        )

class Frostywind(IceSpell):
    """Frostywind spell"""
    def __init__(self):
        super().__init__(
            name="Frostywind",
            mp_cost=24,
            base_power=45,
            freeze_chance=0.25,
            freeze_duration=2,
            description="Mid-powered multi-target ice spell",
            targeting="all_enemies"
        )

class Frigidwind(IceSpell):
    """Frigidwind spell"""
    def __init__(self):
        super().__init__(
            name="Frigidwind",
            mp_cost=48,
            base_power=85,
            freeze_chance=0.4,
            freeze_duration=2,
            description="High-powered multi-target ice spell",
            targeting="all_enemies"
        )
        