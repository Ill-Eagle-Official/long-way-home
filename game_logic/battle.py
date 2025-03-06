import random
from .character import Character
from .enemy_database import get_random_enemy

class Battle:
    """
    Manages the battle system between player and enemy characters.
    Implements a turn-based combat system inspired by Final Fantasy X,
    including action processing, damage calculation, and battle state management.
    """

    def __init__(self, player):
        """
        Initialize a new battle instance.
        
        Args:
            player (Character): The player character instance
        """
        self.player = player
        self.enemy = self._generate_enemy()
        self.turn = 1
        self.battle_log = []
        self.battle_over = False
        self.victory = False

    def _generate_enemy(self):
        """
        Generate a random enemy with scaled stats based on player level.
        Uses the enemy database to create appropriate enemies.
        
        Returns:
            Character: A new enemy character instance
        """
        enemy_data = get_random_enemy(self.player.level)
        stats = enemy_data["stats"]
        
        enemy = Character(
            enemy_data["name"],
            stats["hp"],
            stats["mp"],
            stats["strength"],
            stats["defense"],
            stats["magic"],
            stats["magic_defense"],
            stats["agility"],
            stats["luck"]
        )
        
        # Store additional enemy-specific data
        enemy.special_move = enemy_data["special_move"]
        enemy.exp_value = enemy_data["exp_value"]
        enemy.abilities = enemy_data["abilities"]
        enemy.drops = enemy_data["drops"]
        
        return enemy

    def start_battle(self):
        """
        Initialize the battle state and return initial battle information.
        
        Returns:
            dict: Initial battle state including enemy info and turn count
        """
        self.battle_log.append(f"A {self.enemy.name} appears!")
        return self._get_battle_state()

    def process_turn(self, action):
        """
        Process a single turn of combat, including player and enemy actions.
        
        Args:
            action (dict): Player's chosen action and target
            
        Returns:
            dict: Updated battle state after the turn is complete
        """
        # Process player's action
        self._process_player_action(action)
        
        # If enemy is still alive, process their turn
        if self.enemy.is_alive() and not self.battle_over:
            self._process_enemy_turn()
        
        self.turn += 1
        
        # Check battle end conditions
        self._check_battle_end()
        
        return self._get_battle_state()

    def _process_player_action(self, action):
        """
        Handle the player's chosen action for their turn.
        
        Args:
            action (dict): Contains action type and name
        """
        action_type = action.get('type', 'basic')
        action_name = action.get('name', 'attack')
        
        # Process different types of actions
        if action_type == 'basic':
            if action_name == 'attack':
                self._handle_attack(self.player, self.enemy)
            elif action_name == 'defend':
                self._handle_defend(self.player)
                
        elif action_type == 'abilities':
            self._handle_ability(action_name)
            
        elif action_type == 'skills':
            self._handle_skill(action_name)
            
        elif action_type in ['black_magic', 'white_magic']:
            self._handle_magic(action_name, action_type)

    def _process_enemy_turn(self):
        """
        Handle the enemy's turn using simple AI logic.
        Enemy will generally attack, but may use special abilities
        when below certain HP thresholds.
        """
        # Enemy AI: More likely to use special moves when HP is low
        hp_percent = (self.enemy.current_hp / self.enemy.max_hp) * 100
        
        if hp_percent < 30 and random.random() < 0.4:
            # Use special move when low on HP
            special_move = self.enemy.special_move
            damage_mult = 1.5
            result = self.enemy.calculate_damage(self.player)
            damage = int(result['damage'] * damage_mult)
            self.player.take_damage(damage)
            self.battle_log.append(f"{self.enemy.name} uses {special_move} for {damage} damage!")
            return
        
        # Default to basic attack
        self._handle_attack(self.enemy, self.player)

    def _handle_attack(self, attacker, target):
        """
        Process a basic attack action.
        
        Args:
            attacker (Character): The character performing the attack
            target (Character): The target of the attack
        """
        result = attacker.calculate_damage(target)
        damage = target.take_damage(result['damage'])
        
        # Create battle log message
        msg = f"{attacker.name} attacks {target.name} for {damage} damage!"
        if result['is_critical']:
            msg = f"Critical hit! {msg}"
        self.battle_log.append(msg)

    def _handle_defend(self, character):
        """
        Process a defend action, which reduces damage taken next turn.
        
        Args:
            character (Character): The character defending
        """
        # Implement defense bonus (handled in damage calculations)
        self.battle_log.append(f"{character.name} takes a defensive stance!")

    def _handle_ability(self, ability_name):
        """
        Process a special ability action.
        
        Args:
            ability_name (str): Name of the ability to use
        """
        if ability_name == "Cheer":
            self.player.strength += 2
            self.battle_log.append(f"{self.player.name} uses Cheer! Strength increased!")
        elif ability_name == "Provoke":
            # Implement provoke effects
            self.battle_log.append(f"{self.player.name} provokes the enemy!")
        elif ability_name == "Steal":
            # Simple steal implementation
            steal_chance = self.player.luck / 100
            if random.random() < steal_chance:
                self.battle_log.append(f"{self.player.name} successfully steals an item!")
            else:
                self.battle_log.append(f"{self.player.name}'s steal attempt failed!")

    def _handle_skill(self, skill_name):
        """
        Process a skill action.
        
        Args:
            skill_name (str): Name of the skill to use
        """
        mp_cost = {
            'Power Break': 10,
            'Armor Break': 10,
            'Dark Attack': 8,
            'Flee': 4
        }
        
        if not self.player.use_mp(mp_cost.get(skill_name, 0)):
            self.battle_log.append(f"Not enough MP to use {skill_name}!")
            return
            
        if skill_name == "Power Break":
            self.enemy.strength = max(1, self.enemy.strength - 5)
            self.battle_log.append(f"{self.player.name} uses Power Break! Enemy's strength decreased!")
        elif skill_name == "Armor Break":
            self.enemy.defense = max(1, self.enemy.defense - 5)
            self.battle_log.append(f"{self.player.name} uses Armor Break! Enemy's defense decreased!")
        elif skill_name == "Dark Attack":
            # Implement accuracy reduction
            self.battle_log.append(f"{self.player.name} uses Dark Attack! Enemy's accuracy decreased!")
        elif skill_name == "Flee":
            # 50% chance to flee
            if random.random() < 0.5:
                self.battle_over = True
                self.battle_log.append(f"{self.player.name} successfully fled from battle!")
            else:
                self.battle_log.append(f"{self.player.name}'s attempt to flee failed!")

    def _handle_magic(self, spell_name, magic_type):
        """
        Process a magic spell action.
        
        Args:
            spell_name (str): Name of the spell to cast
            magic_type (str): Type of magic (black or white)
        """
        mp_cost = 4  # Base MP cost for spells
        
        if not self.player.use_mp(mp_cost):
            self.battle_log.append(f"Not enough MP to cast {spell_name}!")
            return
            
        if magic_type == 'black_magic':
            spell_power = {
                'Fire': 20,
                'Thunder': 20,
                'Blizzard': 20
            }.get(spell_name, 0)
            
            result = self.player.calculate_magic_damage(self.enemy, spell_power)
            damage = self.enemy.take_damage(result['damage'])
            
            msg = f"{self.player.name} casts {spell_name} for {damage} damage!"
            if result['is_critical']:
                msg = f"Critical hit! {msg}"
            self.battle_log.append(msg)
            
        elif magic_type == 'white_magic':
            if spell_name == 'Cure':
                heal_amount = int(self.player.magic * 1.5)
                self.player.heal(heal_amount)
                self.battle_log.append(f"{self.player.name} casts Cure and recovers {heal_amount} HP!")

    def _check_battle_end(self):
        """
        Check if the battle has ended (either character defeated).
        Updates battle_over and victory flags accordingly.
        """
        # Debug logging
        print(f"Checking battle end:")
        print(f"Player HP: {self.player.current_hp}/{self.player.max_hp}")
        print(f"Enemy HP: {self.enemy.current_hp}/{self.enemy.max_hp}")
        print(f"Enemy alive: {self.enemy.is_alive()}")
        
        if not self.player.is_alive():
            print("Player defeated")
            self.battle_over = True
            self.victory = False
            self.battle_log.append(f"{self.player.name} has been defeated!")
        elif not self.enemy.is_alive():
            print("Enemy defeated")
            self.battle_over = True
            self.victory = True
            exp_gain = self.enemy.exp_value
            self.player.gain_experience(exp_gain)
            self.battle_log.append(f"{self.enemy.name} has been defeated!")
            self.battle_log.append(f"{self.player.name} gains {exp_gain} experience!")
            
            # Future implementation: Handle item drops
            # if random.random() < drop_chance:
            #     dropped_item = random.choice(self.enemy.drops)
            #     self.battle_log.append(f"The enemy dropped a {dropped_item}!")

    def _get_battle_state(self):
        """
        Get the current state of the battle.
        
        Returns:
            dict: Current battle state including character stats and battle progress
        """
        return {
            'player': self.player.to_dict(),
            'enemy': self.enemy.to_dict(),
            'turn': self.turn,
            'battle_log': self.battle_log,
            'battle_over': self.battle_over,
            'victory': self.victory
        } 