import random
from .character import Character

class Battle:
    def __init__(self, player):
        self.player = player
        self.enemy = self._generate_enemy()
        self.turn = 0
        self.battle_log = []

    def _generate_enemy(self):
        enemy_types = [
            {
                'name': 'Dingo',
                'hp': 250,
                'mp': 20,
                'strength': 10,
                'defense': 5,
                'magic': 3,
                'magic_defense': 5,
                'agility': 8,
                'luck': 10
            },
            {
                'name': 'Killer Bee',
                'hp': 180,
                'mp': 0,
                'strength': 12,
                'defense': 2,
                'magic': 0,
                'magic_defense': 2,
                'agility': 15,
                'luck': 12
            },
            {
                'name': 'Water Flan',
                'hp': 350,
                'mp': 40,
                'strength': 4,
                'defense': 15,
                'magic': 15,
                'magic_defense': 15,
                'agility': 5,
                'luck': 8
            },
            {
                'name': 'Condor',
                'hp': 220,
                'mp': 10,
                'strength': 8,
                'defense': 4,
                'magic': 2,
                'magic_defense': 4,
                'agility': 20,
                'luck': 15
            }
        ]
        
        enemy_type = random.choice(enemy_types)
        # Scale enemy based on player level (FFX-style scaling)
        level_scaling = max(1, self.player.level - 1) * 0.15
        
        return Character(
            enemy_type['name'],
            int(enemy_type['hp'] * (1 + level_scaling)),
            int(enemy_type['mp'] * (1 + level_scaling)),
            int(enemy_type['strength'] * (1 + level_scaling)),
            int(enemy_type['defense'] * (1 + level_scaling)),
            int(enemy_type['magic'] * (1 + level_scaling)),
            int(enemy_type['magic_defense'] * (1 + level_scaling)),
            int(enemy_type['agility'] * (1 + level_scaling)),
            int(enemy_type['luck'] * (1 + level_scaling))
        )

    def start_battle(self):
        self.turn = 0
        self.battle_log = []
        return self._get_battle_state()

    def process_turn(self, action):
        if action not in ['attack', 'defend', 'heal']:
            return {'error': 'Invalid action'}

        # Player's turn
        damage_dealt = 0
        if action == 'attack':
            attack_result = self.player.calculate_damage(self.enemy)
            damage_dealt = attack_result['damage']
            self.enemy.take_damage(damage_dealt)
            
            if attack_result['is_critical']:
                self.battle_log.append(f"CRITICAL HIT! {self.player.name} strikes {self.enemy.name} for {damage_dealt} damage!")
            else:
                self.battle_log.append(f"{self.player.name} attacks {self.enemy.name} for {damage_dealt} damage!")
        elif action == 'defend':
            self.player.defense += 5  # Temporary defense boost
            self.battle_log.append(f"{self.player.name} takes a defensive stance!")
        elif action == 'heal':
            heal_amount = 20
            self.player.heal(heal_amount)
            self.battle_log.append(f"{self.player.name} heals for {heal_amount} HP!")

        # Check if enemy is defeated
        if not self.enemy.is_alive():
            exp_gain = random.randint(20, 30)
            self.player.gain_experience(exp_gain)
            self.battle_log.append(f"{self.enemy.name} is defeated! {self.player.name} gains {exp_gain} experience!")
            return self._get_battle_state(battle_over=True, victory=True)

        # Enemy's turn
        enemy_attack = self.enemy.calculate_damage(self.player)
        enemy_damage = enemy_attack['damage']
        self.player.take_damage(enemy_damage)
        
        if enemy_attack['is_critical']:
            self.battle_log.append(f"CRITICAL HIT! {self.enemy.name} strikes {self.player.name} for {enemy_damage} damage!")
        else:
            self.battle_log.append(f"{self.enemy.name} attacks {self.player.name} for {enemy_damage} damage!")

        # Reset temporary defense boost
        if action == 'defend':
            self.player.defense -= 5

        # Check if player is defeated
        if not self.player.is_alive():
            self.battle_log.append(f"{self.player.name} has been defeated!")
            return self._get_battle_state(battle_over=True, victory=False)

        self.turn += 1
        return self._get_battle_state()

    def _get_battle_state(self, battle_over=False, victory=None):
        state = {
            'turn': self.turn,
            'player': self.player.to_dict(),
            'enemy': self.enemy.to_dict(),
            'battle_log': self.battle_log,
            'battle_over': battle_over
        }
        if battle_over:
            state['victory'] = victory
        return state 