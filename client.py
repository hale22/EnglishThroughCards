import requests

BASE_URL = 'http://127.0.0.1:5000'

def register(nick):
    response = requests.post(f'{BASE_URL}/register', json={'nick': nick})
    return response.json()

def login(nick):
    response = requests.post(f'{BASE_URL}/login', json={'nick': nick})
    return response.json()

def get_words(user_id):
    response = requests.post(f'{BASE_URL}/get_words', json={'user_id': user_id})
    return response.json()

def update_status(user_id, word_id, status):
    response = requests.post(f'{BASE_URL}/update_status', json={'user_id': user_id, 'word_id': word_id, 'status': status})
    return response.json()

def main():
    print("Добро пожаловать в приложение для изучения английского!")
    choice = input("Введите 'r' для регистрации или 'l' для входа: ").strip().lower()
    
    if choice == 'r':
        nick = input("Введите ваш ник: ").strip()
        user = register(nick)
    elif choice == 'l':
        nick = input("Введите ваш ник: ").strip()
        user = login(nick)
        if 'error' in user:
            print("Пользователь не найден!")
            return
    else:
        print("Неверный выбор!")
        return
    
    user_id = user['id']
    words = get_words(user_id)
    
    print("Изучите следующие слова:")
    for word in words:
        print(f"Слово: {word['en']} ({word['tr']}) - Перевод: {word['ru']}")
    
    input("Нажмите Enter, чтобы начать тестирование...")
    
    for word in words:
        translation = input(f"Введите перевод для слова '{word['en']}': ").strip()
        if translation.lower() == word['ru'].lower():
            update_status(user_id, word['id'], 'learned')
            print("Правильно!")
        else:
            update_status(user_id, word['id'], 'to repeat')
            print("Неправильно! Слово будет повторено.")
    
    print("Обучение завершено!")

if __name__ == '__main__':
    main()
ko