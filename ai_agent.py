import os
import requests
import google.generativeai as genai
import sys

# Проверка наличия переменных (чтобы понять, видит ли их GitHub)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_ai_summary():
    if not GEMINI_API_KEY:
        raise ValueError("Ошибка: GEMINI_API_KEY не найден в Secrets!")
    
    genai.configure(api_key=GEMINI_API_KEY)
    # Используем проверенную модель 1.5-flash
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Найди и кратко перескажи 3 главные новости за сегодня о внедрении ИИ в бизнес-процессы. На русском языке, с эмодзи. Прикрпи ссылки на источники."
    
    try:
        response = model.generate_content(prompt)
        if not response.text:
            return "Gemini вернула пустой ответ."
        return response.text
    except Exception as e:
        return f"Ошибка при запросе к Gemini: {str(e)}"

def send_to_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Ошибка: Данные Telegram не найдены в Secrets!")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    
    r = requests.post(url, json=payload)
    if r.status_code != 200:
        print(f"Ошибка Telegram API: {r.text}")

if __name__ == "__main__":
    try:
        summary = get_ai_summary()
        print(f"Подготовленный текст: {summary[:50]}...") # Отладка
        send_to_telegram(summary)
        print("Скрипт завершен успешно.")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1) # Передаем код ошибки GitHub
