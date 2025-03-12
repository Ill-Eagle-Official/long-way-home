"""
Fire-based spell implementations.
"""

from .base import BlackMagicSpell, SpellEffect, Status, StatusEffect, DamageType

class FireSpell(BlackMagicSpell):
    """Base class for fire-element spells with burn effect"""
    
    def __init__(
        self,
        name: str,
        mp_cost: int,
        base_power: int,
        burn_chance: float,
        description: str
    ):
        super().__init__(
            name=name,
            mp_cost=mp_cost,
            base_power=base_power,
            description=description,
            targeting="enemy",
            damage_type=DamageType.FIRE
        )
        self.burn_chance = burn_chance
        self.burn_potency = 0.05 # 5% of max HP per turn if burned
        self.burn_duration = 999

    def calculate_effect(self, caster, target) -> SpellEffect:
        """Calculate fire damage and potential burn effect"""
        # Get the base damage calculation from BlackMagicSpell
        effect = super().calculate_effect(caster, target)
        
        # Add burn status effect
        burn_effect = StatusEffect(
            status=Status.BURN,
            duration=3,  # Lasts 3 turns
            potency=self.burn_potency,
            chance=self.burn_chance,
            duration=self.burn_duration
        )
        
        effect.status_effects.append(burn_effect)
        return effect

# Different tiers of fire spells
class Fire(FireSpell):
    """Basic fire spell"""
    def __init__(self):
        super().__init__(
            name="Fire",
            mp_cost=4,
            base_power=20,
            burn_chance=0.2,  # 20% chance to burn
            description="Deals fire damage with a small chance to burn",
        )

class Fira(FireSpell):
    """Medium-tier fire spell"""
    def __init__(self):
        super().__init__(
            name="Fira",
            mp_cost=12,
            base_power=45,
            burn_chance=0.35,  # 35% chance to burn
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
            description="Deals heavy fire damage with a high chance to burn"
        ) 

class Fireball(FireSpell):
    """Fire spell which hits all enemies"""
    def __init__(self):
        super().__init__(
            name="Fireball",
            mp_cost=8,
            base_power=20,
            burn_chance=0.2,
            description="Fireball spell which hits all enemies",
            targeting="all_enemies"
        )
        
class Firaball(FireSpell):
    """Fire spell which hits all allies"""
    def __init__(self):
        super().__init__(
            name="Firaball",
            mp_cost=24,
            base_power=45,
            burn_chance=0.35,
            description="Firaball spell which hits all enemies",
            targeting="all_enemies"
        )

class Firagaball(FireSpell):
    """Powerful fire spell which hits all enemies"""
    def __init__(self):
        super().__init__(
            name="Firagaball",
            mp_cost=48,
            base_power=85,
            burn_chance=0.5,
            description="Firagaball spell which hits all enemies",
            targeting="all_enemies"
        )
        
        
        