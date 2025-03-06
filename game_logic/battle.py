import random
from .character import Character
from .enemy_database import get_random_enemy
from .skills import get_skill_cost, get_spell_power

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
        action_success = self._process_player_action(action)
        
        # Only proceed with enemy turn if player's action was successful
        if action_success and self.enemy.is_alive() and not self.battle_over:
            self._process_enemy_turn()
            self.turn += 1
        
        # Check battle end conditions
        self._check_battle_end()
        
        # Include action success in battle state
        battle_state = self._get_battle_state()
        battle_state['action_success'] = action_success
        return battle_state

    def _process_player_action(self, action):
        """
        Handle the player's chosen action for their turn.
        
        Args:
            action (dict): Contains action type and name
            
        Returns:
            bool: Whether the action was successfully executed
        """
        action_type = action.get('type', 'basic')
        action_name = action.get('name', 'attack')
        
        # Process different types of actions
        if action_type == 'basic':
            if action_name == 'attack':
                self._handle_attack(self.player, self.enemy)
                return True
            elif action_name == 'defend':
                self._handle_defend(self.player)
                return True
                
        elif action_type == 'abilities':
            return self._handle_ability(action_name)
            
        elif action_type == 'skills':
            return self._handle_skill(action_name)
            
        elif action_type in ['black_magic', 'white_magic']:
            return self._handle_magic(action_name, action_type)
            
        return True  # Default to true for unknown actions

    def _process_enemy_turn(self):
        """
        Handle the enemy's turn using simple AI logic.
        Enemy will generally attack, but may use special abilities
        when below certain HP thresholds.
        """
        # Enemy AI: More likely to use special moves when HP is low
        hp_percent = (self.enemy.current_hp / self.enemy.max_hp) * 100
        
        if hp_percent < 30 and random.random() < 0.4 and self.enemy.special_move:
            # Use special move when low on HP
            result = self.enemy.calculate_damage(self.player, is_special_move=True)
            damage = self.player.take_damage(result['damage'])
            self.battle_log.append(f"{self.enemy.name} uses {self.enemy.special_move} for {damage} damage!")
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
        
        # Debug logging
        if isinstance(target, Character) and target == self.enemy:
            print(f"Enemy HP after damage: {target.current_hp}/{target.max_hp}")
            print(f"Enemy alive status: {target.is_alive()}")
        
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
            
        Returns:
            bool: Whether the ability was successfully used
        """
        if not self.player.use_mp(get_skill_cost(ability_name)):
            self.battle_log.append(f"Not enough MP to use {ability_name}!")
            return False
            
        if ability_name == "Cheer":
            self.player.strength += 2
            self.battle_log.append(f"{self.player.name} uses Cheer! Strength increased!")
        elif ability_name == "Provoke":
            # Implement provoke effects
            self.enemy.defense -= 5
            self.enemy.strength += 2
            self.battle_log.append(f"{self.player.name} provokes the enemy!")
        elif ability_name == "Steal":
            # Simple steal implementation
            steal_chance = self.player.luck / 100
            if random.random() < steal_chance:
                self.battle_log.append(f"{self.player.name} successfully steals an item!")
            else:
                self.battle_log.append(f"{self.player.name}'s steal attempt failed!")
        return True

    def _handle_skill(self, skill_name):
        """
        Process a skill action.
        
        Args:
            skill_name (str): Name of the skill to use
            
        Returns:
            bool: Whether the skill was successfully used
        """
        if not self.player.use_mp(get_skill_cost(skill_name)):
            self.battle_log.append(f"Not enough MP to use {skill_name}!")
            return False
            
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
        return True

    def _handle_magic(self, spell_name, magic_type):
        """
        Process a magic spell action.
        
        Args:
            spell_name (str): Name of the spell to cast
            magic_type (str): Type of magic (black or white)
            
        Returns:
            bool: Whether the spell was successfully cast
        """
        if not self.player.use_mp(get_skill_cost(spell_name)):
            self.battle_log.append(f"Not enough MP to cast {spell_name}!")
            return False
            
        if magic_type == 'black_magic':
            result = self.player.calculate_magic_damage(self.enemy, spell_name)
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
        return True

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