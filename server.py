from flask import Flask, request, jsonify
import json
import random
import os

app = Flask(__name__)

# Загрузка данных из JSON файлов
def load_json(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

words = load_json('words.json')
users = load_json('users.json')
connections = load_json('connections.json')

@app.route('/register', methods=['POST'])
def register():
    nick = request.json.get('nick')
    user_id = len(users) + 1
    users.append({'id': user_id, 'nick': nick})
    save_json('users.json', users)
    
    for word in words:
        connections.append({'user_id': user_id, 'word_id': word['id'], 'status': 'not learned'})
    save_json('connections.json', connections)
    
    return jsonify({'id': user_id, 'nick': nick})

@app.route('/login', methods=['POST'])
def login():
    nick = request.json.get('nick')
    user = next((u for u in users if u['nick'] == nick), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/get_words', methods=['POST'])
def get_words():
    user_id = request.json.get('user_id')
    user_words = [c for c in connections if c['user_id'] == user_id and c['status'] in ['not learned', 'to repeat']]
    random_words = random.sample(user_words, min(10, len(user_words)))
    words_to_study = [w for w in words if any(rw['word_id'] == w['id'] for rw in random_words)]
    return jsonify(words_to_study)

@app.route('/update_status', methods=['POST'])
def update_status():
    user_id = request.json.get('user_id')
    word_id = request.json.get('word_id')
    status = request.json.get('status')
    
    for connection in connections:
        if connection['user_id'] == user_id and connection['word_id'] == word_id:
            connection['status'] = status
            break
    save_json('connections.json', connections)
    
    return jsonify({'message': 'Status updated'})

if __name__ == '__main__':
    app.run(debug=True)
