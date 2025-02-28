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
        'hp': 100,
        'attack': 15,
        'defense': 10,
        'speed': 8,
        'description': 'A strong melee fighter with high HP and attack power.'
    },
    'mage': {
        'name': 'Mage',
        'hp': 70,
        'attack': 20,
        'defense': 5,
        'speed': 7,
        'description': 'A powerful spellcaster with high attack but low defense.'
    },
    'rogue': {
        'name': 'Rogue',
        'hp': 80,
        'attack': 12,
        'defense': 7,
        'speed': 15,
        'description': 'A quick fighter with high speed and balanced stats.'
    }
}

@app.route('/')
def index():
    # Clear any existing battle state when returning to character selection
    if 'battle_state' in session:
        del session['battle_state']
    return render_template('index.html', characters=CHARACTERS)

@app.route('/select_character', methods=['POST'])
def select_character():
    character_type = request.form.get('character_type')
    if character_type not in CHARACTERS:
        return jsonify({'error': 'Invalid character type'}), 400
    
    char_data = CHARACTERS[character_type]
    player = Character(
        char_data['name'],
        char_data['hp'],
        char_data['attack'],
        char_data['defense'],
        char_data['speed']
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
    if 'player' not in session or 'battle_state' not in session:
        return jsonify({'error': 'No active battle'}), 400
    
    action = request.form.get('action')
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

if __name__ == '__main__':
    app.run(debug=True) 