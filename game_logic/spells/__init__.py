"""
Spells package containing all spell implementations for the game.
"""

from .base import Spell, SpellType, SpellEffect, Status, StatusEffect
from .fire_spells import Fire, Fira, Firaga
# Future imports will go here as we add more spell types:
# from .ice_spells import Ice, Blizzara, Blizzaga
# from .thunder_spells import Thunder, Thundara, Thundaga
# from .healing_spells import Cure, Cura, Curaga

# Export all spell classes for easy access
__all__ = [
    'Spell', 'SpellType', 'SpellEffect', 'Status', 'StatusEffect',
    'Fire', 'Fira', 'Firaga',
] 