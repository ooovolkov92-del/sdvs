import os
import requests
import google.generativeai as genai

# GitHub сам подставит эти значения из раздела Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_ai_summary():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Найди новости за последние 24 часа о внедрении ИИ в бизнес-процессы. Напиши краткую выжимку на русском языке с эмодзи для Telegram. Добавь ссылки на источники информации"
    
    response = model.generate_content(prompt)
    return response.text

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    summary = get_ai_summary()
    send_to_telegram(summary)
