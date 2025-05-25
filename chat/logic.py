from .nlp_ml import ChatbotNLP, DEFAULT_CHART_INTENTS
from .utils import generate_chart
from .search import search_duckduckgo

greeting_variants = {
    "привет", "здравствуй", "здравствуйте", "добрый день", "доброе утро",
    "хай", "йо", "здорово", "прив", "приветик", "приветище", "дарова",
    "добрый вечер", "хэллоу"
}
greeting_replies = [
    "Привет! Чем могу помочь?",
    "Здравствуйте! Рад вас видеть!",
    "Добрый день!",
    "Хэй! Чем помочь?",
    "Привет-привет! Как ваши дела?",
    "Здорово! Что нового?"
]

how_are_you_variants = {
    "как дела", "чё делаешь", "как ты", "что делаешь", "как поживаешь",
    "как жизнь", "как настроение", "чем занимаешься"
}
how_are_you_replies = [
    "Всё отлично, спасибо! А у вас?",
    "Работаю для вас, спрашивайте!",
    "Отлично! Чем могу помочь?",
    "Нормально, а вы как?",
    "Всё хорошо, чем могу помочь сегодня?"
]

farewell_variants = {
    "пока", "до свидания", "досвидания", "увидимся", "бай", "до встречи",
    "счастливо", "прощай", "удачи"
}
farewell_replies = [
    "До встречи!", "Пока-пока!", "Хорошего дня!", "Всего доброго!",
    "Удачи!", "Буду ждать вас снова!"
]

help_message = (
    "Вот что я умею:\n"
    "- Отвечать на приветствия и прощания\n"
    "- Строить графики (цены, продажи, площадь, районы)\n"
    "- Искать в интернете\n"
    "- Обучаться новым темам по вашим запросам\n"
    "- Поддержка голосового ввода и подсказки\n"
    "- Пишите /help чтобы увидеть это сообщение"
)

chatbot_nlp = ChatbotNLP()

def get_valid_chart_types():
    chart_keys = ["price", "sales", "size", "district"]
    valid_chart_types = {}
    for key in chart_keys:
        for synonym in DEFAULT_CHART_INTENTS.get(key, []):
            valid_chart_types[synonym] = key
    return valid_chart_types


def find_chart_type_in_message(msg):
    for key, synonyms in DEFAULT_INTENTS.items():
        if key in ["price", "sales", "size", "district"]:
            for syn in synonyms:
                if syn in msg:
                    return key
    return None
def process_user_message(user_message: str):
    low_msg = user_message.lower()

    # Удалил проверку неизвестных тем, т.к. в ChatbotNLP её нет

    # Приветствия
    if any(word in low_msg for word in greeting_variants):
        return greeting_replies[0], None  # random.choice убрал, т.к. random не импортирован

    # Как дела
    if any(word in low_msg for word in how_are_you_variants):
        return how_are_you_replies[0], None

    # Прощания
    if any(word in low_msg for word in farewell_variants):
        return farewell_replies[0], None

    # Помощь
    if low_msg in {"help", "/help", "помощь", "что ты умеешь"}:
        return help_message, None

    # Запрос графиков
    if "график" in low_msg or "диаграмма" in low_msg:
        valid_chart_types = get_valid_chart_types()
        requested_types = [valid_chart_types[word] for word in valid_chart_types if word in low_msg]

        if not requested_types:
            return ("А какой график вас интересует? Например: цены, продажи, площадь, районы."), None

        chart_type = requested_types[0]

        topic = None


        chart_url = generate_chart(chart_type)

        reply_map = {
            "price": f"Вот график цен {topic}." if topic else "Вот график цен.",
            "sales": f"Вот график количества продаж {topic}." if topic else "Вот график количества продаж.",
            "size": f"Вот график средней площади {topic}." if topic else "Вот график средней площади.",
            "district": f"Вот график по районам."
        }

        return reply_map.get(chart_type, "Вот ваш график."), chart_url

    # Поиск в интернете
    return search_duckduckgo(user_message), None