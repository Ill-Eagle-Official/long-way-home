"""
Base classes and types for the spell system.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
import random

class SpellType(Enum):
    """Defines the different types of spells available"""
    BLACK_MAGIC = "black_magic"
    WHITE_MAGIC = "white_magic"
    ABILITY = "ability"
    SKILL = "skill"

class Status(Enum):
    """Defines possible status effects"""
    BURN = "burn"      # Deals damage over time
    POISON = "poison"  # Deals percentage-based damage over time
    BLIND = "blind"    # Reduces accuracy
    SLEEP = "sleep"    # Cannot act
    HASTE = "haste"    # Increased speed
    SLOW = "slow"      # Decreased speed

@dataclass
class StatusEffect:
    """Represents a status effect with duration and potency"""
    status: Status
    duration: int  # Number of turns
    potency: int  # Effect strength (e.g., damage per turn for burn)
    chance: float = 1.0  # Probability of applying the status (0.0 to 1.0)

@dataclass
class SpellEffect:
    """Represents the effects a spell can have"""
    damage: int = 0
    healing: int = 0
    stat_changes: dict = None
    status_effects: list[StatusEffect] = None

    def __post_init__(self):
        """Initialize empty collections if None"""
        if self.stat_changes is None:
            self.stat_changes = {}
        if self.status_effects is None:
            self.status_effects = []

class Spell:
    """Base class for all spells, abilities, and skills in the game"""
    
    def __init__(
        self,
        name: str,
        mp_cost: int,
        spell_type: SpellType,
        base_power: int = 0,
        description: str = "",
        targeting: str = "enemy"
    ):
        self.name = name
        self.mp_cost = mp_cost
        self.spell_type = spell_type
        self.base_power = base_power
        self.description = description
        self.targeting = targeting  # 'enemy', 'self', 'ally', 'all_enemies'

    def calculate_effect(self, caster, target) -> SpellEffect:
        """
        Calculate the effect of the spell based on caster and target stats.
        This is the base implementation - specific spells can override this.
        """
        return SpellEffect()

    def can_cast(self, caster) -> tuple[bool, Optional[str]]:
        """Check if the spell can be cast by checking MP and any other conditions"""
        if caster.current_mp < self.mp_cost:
            return False, f"Not enough MP! (Need {self.mp_cost} MP)"
        return True, None

    def apply_effect(self, effect: SpellEffect, target) -> list[str]:
        """Apply the calculated effect to the target and return log messages"""
        messages = []
        
        if effect.damage > 0:
            actual_damage = target.take_damage(effect.damage)
            messages.append(f"{target.name} takes {actual_damage} damage!")
            
        if effect.healing > 0:
            actual_healing = target.heal(effect.healing)
            messages.append(f"{target.name} recovers {actual_healing} HP!")
            
        if effect.stat_changes:
            for stat, change in effect.stat_changes.items():
                setattr(target, stat, getattr(target, stat) + change)
                messages.append(f"{target.name}'s {stat} {'increased' if change > 0 else 'decreased'} by {abs(change)}!")
                
        return messages 