from flask import Flask, render_template, jsonify, request, session
from game_logic.character import Character
from game_logic.battle import Battle
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Available character classes
CHARACTERS = {
    'warrior': {
        'name': 'Warrior',
        'hp': 840,
        'mp': 56,
        'strength': 20,
        'defense': 15,
        'magic': 5,
        'magic_defense': 10,
        'agility': 12,
        'luck': 15,
        'description': 'A strong physical fighter with high HP and strength.'
    },
    'mage': {
        'name': 'Black Mage',
        'hp': 572,
        'mp': 84,
        'strength': 8,
        'defense': 8,
        'magic': 22,
        'magic_defense': 18,
        'agility': 10,
        'luck': 17,
        'description': 'A powerful spellcaster with high magic and MP.'
    },
    'rogue': {
        'name': 'Thief',
        'hp': 690,
        'mp': 70,
        'strength': 15,
        'defense': 10,
        'magic': 10,
        'magic_defense': 12,
        'agility': 25,
        'luck': 20,
        'description': 'An agile fighter with high speed and luck.'
    }
}

@app.route('/')
def index():
    """
    Main route that displays the character selection screen.
    Players can choose their character class from available templates.
    """
    # Clear any existing battle state when returning to character selection
    if 'battle_state' in session:
        del session['battle_state']
    return render_template('index.html', characters=CHARACTERS)

@app.route('/select_character', methods=['POST'])
def select_character():
    """
    Handle character selection and create a new character instance.
    The selected character's stats are loaded from templates and stored in session.
    
    Returns:
        redirect: Redirects to battle page after character creation
    """
    character_type = request.form.get('character_type')
    if character_type not in CHARACTERS:
        return jsonify({'error': 'Invalid character type'}), 400
    
    char_data = CHARACTERS[character_type]
    player = Character(
        char_data['name'],
        char_data['hp'],
        char_data['mp'],
        char_data['strength'],
        char_data['defense'],
        char_data['magic'],
        char_data['magic_defense'],
        char_data['agility'],
        char_data['luck']
    )
    session['player'] = player.to_dict()
    return jsonify({'success': True, 'character': player.to_dict()})

@app.route('/battle')
def battle():
    if 'player' not in session:
        return jsonify({'error': 'No character selected'}), 400
    return render_template('battle.html', player=session['player'])

@app.route('/start_battle', methods=['POST'])
def start_battle():
    """
    Initialize a new battle instance with the player's character.
    Creates a new Battle object and stores it in the session.
    
    Returns:
        json: Initial battle state including player and enemy information
    """
    if 'player' not in session:
        return jsonify({'error': 'No character selected'}), 400
    
    player = Character.from_dict(session['player'])
    battle = Battle(player)
    battle_state = battle.start_battle()
    
    # Store both battle state and enemy state in session
    session['battle_state'] = {
        'turn': battle_state['turn'],
        'battle_log': battle_state['battle_log'],
        'enemy': battle_state['enemy']
    }
    
    return jsonify(battle_state)

@app.route('/battle_action', methods=['POST'])
def battle_action():
    """
    Process a battle action from the player.
    Handles various action types (attack, defend, abilities, magic)
    and updates the battle state accordingly.
    
    Returns:
        json: Updated battle state after the action is processed
    """
    if 'player' not in session or 'battle_state' not in session:
        return jsonify({'error': 'No active battle', 'battle_over': True}), 400
    
    action = request.get_json()  # Get JSON data instead of form data
    if not action:
        return jsonify({'error': 'Invalid action data', 'battle_over': True}), 400
    
    try:
        player = Character.from_dict(session['player'])
        
        # Recreate battle state from session
        battle = Battle(player)
        battle.turn = session['battle_state']['turn']
        battle.battle_log = session['battle_state']['battle_log']
        battle.enemy = Character.from_dict(session['battle_state']['enemy'])
        
        result = battle.process_turn(action)
        
        # Update session with new battle state
        session['player'] = result['player']
        session['battle_state'] = {
            'turn': result['turn'],
            'battle_log': result['battle_log'],
            'enemy': result['enemy']
        }
        
        return jsonify(result)
    except Exception as e:
        # Log the error for debugging
        print(f"Error in battle_action: {str(e)}")
        # Return a JSON response even in case of error
        return jsonify({
            'error': 'An error occurred during battle',
            'battle_over': True
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 