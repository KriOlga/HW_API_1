import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

url = "https://api.foursquare.com/v3/places/search"

# API_KEY из переменных окружения
headers = {
    "Accept": "application/json",
    "Authorization": os.getenv("API_KEY")
}

# Ввод пользователем интересущих его города и категории
city = input("Введите название города: ")
category = input("Введите наименование категории: ")

params = {
    "near": city,
    "query": category
}

# Запроса API и получение ответа
response = requests.get(url, headers=headers, params=params)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Запрос обработан. Список " + category + ":")
    data = response.json()  # Извлечение данных в формате JSON
    venues = data.get("results", [])
    
    if venues:
        results = []  # Список для хранения результатов
        for venue in venues:
            venue_info = {
                "Название": venue["name"],
                "Адрес": venue["location"].get("address", "Нет адреса"),
                "Рейтинг": venue.get("rating", "Нет рейтинга")
            }
            results.append(venue_info)  # Добавляем информацию о месте в список результатов
            
            # Вывод информации по запросу в консоль
            print(f'Название: "{venue_info["Название"]}",')
            print(f'Адрес: "{venue_info["Адрес"]}",')
            print(f'Рейтинг: "{venue_info["Рейтинг"]}"')
            print()

        # Запись полученных данных в файл
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4) 
    else:
        print("Нет результатов по вашему запросу.")
else:
    print("Запрос не удался с кодом состояния:", response.status_code)
    print(response.text)