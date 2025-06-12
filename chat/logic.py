import random
from .nlp_ml import ChatbotNLP, DEFAULT_CHART_INTENTS
from .utils import generate_chart
from .search import search_duckduckgo
import re
from django.utils.translation import gettext_lazy as _
from houses.models import Currency  # Импорт модели
import os
import json

LEARNED_PATH = os.path.join("chat", "learned_prompts.json")

def load_learned():
    if os.path.exists(LEARNED_PATH):
        with open(LEARNED_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_learned(data):
    with open(LEARNED_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---- Удалена detect_language ----
# Вместо нее определение языка внутри process_user_message

def get_localized_message(lang, message_key):
    translations = {
        "Нет данных о курсах валют.": {
            "ru": "Нет данных о курсах валют.",
            "en": "No currency data available.",
            "kg": "Валюта боюнча маалымат жок."
        },
        "Актуальные курсы валют:\n": {
            "ru": "Актуальные курсы валют:\n",
            "en": "Current exchange rates:\n",
            "kg": "Азыркы акча курстары:\n"
        }
    }
    return translations.get(message_key, {}).get(lang, message_key)

chatbot_nlp = ChatbotNLP()
# Словарь нецензурных слов по языкам
profanity_words = {
    'ru': ['бля', 'сука', 'хуй', 'еба', 'пизд', 'сучка'],
    'en': ['fuck', 'shit', 'bitch', 'asshole', 'bastard', 'damn'],
    'kg': ['окшумай', 'карга', 'тварь', 'ит', 'нерсеге', 'шайтан']
}

profanity_warning = {
    'ru': "Не матерись, пожалуйста.",
    'en': "Please, no swearing.",
    'kg': "Сөгүнбөңүз, суранам."
}
# Приветствия по языкам
greeting_variants = {
    "ru": {"привет", "здравствуй", "здравствуйте", "добрый день", "доброе утро", "хай", "йо", "здорово", "прив", "приветик", "дарова"},
    "en": {"hello", "hi", "hey"},
    "kg": {"салам", "салам алейкум", "ассаламу алейкум", "ассаламу алейкум"}
}
greeting_replies = {
    "ru": ["Привет! Чем могу помочь?", "Здравствуйте! Рад вас видеть!", "Добрый день!", "Привет-привет! Как дела?"],
    "en": ["Hey there! How can I help you?", "Hi! What can I do for you?", "Hello! Nice to meet you!"],
    "kg": ["Салам! Кандай жардам бере алам?", "Валлейкум ассалам!", "Ассаламу алейкум!"]
}

# Как дела — по языкам
how_are_you_variants = {
    "ru": {"как дела", "чё делаешь", "как ты", "что делаешь", "как поживаешь", "как жизнь", "как настроение", "чем занимаешься"},
    "en": {"how are you", "what's up", "how's it going"},
    "kg": {"кандайсын", "жакшысыңбы"}
}
how_are_you_replies = {
    "ru": ["Всё отлично, спасибо! А у вас?", "Работаю для вас, спрашивайте!", "Нормально, а вы как?"],
    "en": ["I’m doing great! How can I assist you?", "I'm good, thanks! What about you?"],
    "kg": ["Жакшы, рахмат! Сизчи?", "Баары сонун! Сиз кандайсыз?"]
}

# Прощания — по языкам
farewell_variants = {
    "ru": {"пока", "до свидания", "досвидания", "увидимся", "бай", "до встречи", "счастливо", "прощай", "удачи"},
    "en": {"goodbye", "bye", "see you"},
    "kg": {"көрүшкөнчө", "саубол", "жакшы кал"}
}
farewell_replies = {
    "ru": ["До встречи!", "Пока-пока!", "Счастливо!", "Удачи!"],
    "en": ["Goodbye!", "Bye! See you soon!", "Take care!"],
    "kg": ["Көрүшкөнчө!", "Саубол!", "Жакшы кал!"]
}


help_message = (
    "Вот что я умею:\n"
    "- Приветствовать на русском, английском и кыргызском\n"
    "- Отвечать на вопросы типа 'как дела'\n"
    "- Строить графики (цены, продажи, площадь, районы)\n"
    "- Искать в интернете\n"
    "- Понимаю 'Салам алейкум'\n"
    "- Команды теперь просто текст, без слэшей"
)
COMMANDS = {
    "lang": [
        "language", "язык", "til", "какие языки", "ты знаешь языки", "ты понимаешь языки", "знаешь ли ты языки",
        "languages", "do you speak", "can you translate", "which languages do you know", "do you understand russian",
        "what languages", "can you speak", "do you know english", "how many languages", "ты говоришь по",
        "ты умеешь говорить"
    ],
    "info": [
        "info", "инфо", "информация", "блог", "о тебе", "кем ты работаешь", "что ты умеешь", "что ты можешь",
        "about you", "tell me about yourself", "who are you", "what can you do", "what is your job", "your skills",
        "your abilities", "что ты такое", "какой ты", "who made you", "your background"
    ],
    "motivate": [
        "motivate", "мотивация", "вдохнови", "смотивируй", "поддержка", "көңүл айт", "дай совет",
        "inspire me", "give me motivation", "help me stay strong", "cheer me up", "say something inspiring",
        "motivation", "can you motivate", "i need motivation", "support me", "encourage me", "дай напутствие"
    ],
    "fact": [
        "факт", "fact", "интересно", "интересный факт", "билим", "знание", "скажи факт", "расскажи факт",
        "tell me a fact", "fun fact", "did you know", "share a fact", "tell something smart", "science fact",
        "give me knowledge", "random fact", "cool fact", "умный факт", "интересно знать"
    ],
    "joke": [
        "joke", "шутка", "анекдот", "весели", "тамаша", "күлкү", "рассмеши", "пошути",
        "make me laugh", "tell me a joke", "funny", "say something funny", "laugh", "crack a joke",
        "fun time", "jokes please", "i need a laugh", "tell me something hilarious", "юмор"
    ],
    "math": [
        "сколько будет", "посчитай", "calculate", "what is", "math", "арифметика", "математика",
        "solve", "count", "addition", "subtraction", "multiplication", "division", "how much",
        "вычисли", "посчитай за меня", "math question", "math help", "can you do math"
    ],
    "quote": [
        "цитата", "quote", "мудрость", "мысль дня", "цитата дня", "великая мысль", "умная цитата",
        "say a quote", "wisdom", "give me a quote", "inspiring quote", "life quote", "deep thought",
        "thought of the day", "share wisdom", "цитируй", "умные слова"
    ],
    "random": [
        "рандом", "случайное число", "random number", "выбери число", "выбери", "случайный выбор",
        "choose randomly", "pick one", "random", "pick for me", "generate a number", "рандомайзер",
        "coin flip", "roll a dice", "дай число", "случайное значение"
    ],
    "weather": [
        "погода", "weather", "какая погода", "погода сейчас", "что на улице", "прогноз погоды",
        "what's the weather", "is it sunny", "is it raining", "weather forecast", "how's the weather",
        "current weather", "температура", "дождь", "снег", "солнечно ли", "погода у тебя"
    ],
    "translate": [
        "переведи", "translate", "перевод", "can you translate", "переведи на", "переводчик",
        "translate this", "help with translation", "how to say", "how do you say", "what does this mean",
        "language help", "перевод слова", "дай перевод", "переведи текст"
    ],
    "timer": [
        "таймер", "timer", "установи таймер", "поставь будильник", "set timer", "alarm", "start timer",
        "set an alarm", "countdown", "напомни", "установи напоминание", "таймер на", "таймер включи",
        "начни отсчет", "отсчет времени", "поставь время"
    ]
}
EXTRA_COMMAND_RESPONSES = {
    "lang": {
        "en": ["Я понимаю русский, английский и кыргызский."],
        "ru": ["I understand Russian, English, and Kyrgyz."],
        "kg": ["Мен орусча, англисче жана кыргызча түшүнөм."]
    },
    "info": {
        "en": ["Я бот, созданный с использованием Django и ИИ. Спроси меня о чём угодно!"],
        "ru": ["I am a bot created using Django and a bit of AI. Ask me anything!"],
        "kg": ["Мен Django жана жасалма акыл колдонуп түзүлгөн ботмун. Каалаган сурооңузду бериңиз!"]
    },
    "motivate": {
        "en": [
            "Не сдавайся! Всё получится, если постараться!",
            "Каждый день — шанс начать заново.",
            "Ты сильнее, чем думаешь!"
        ],
        "ru": [
            "Don't give up! Great things take time!",
            "Every day is a new beginning.",
            "You are stronger than you think!"
        ],
        "kg": [
            "Үмүт үзбө! Баары жакшы болот!",
            "Ар күн — жаңы мүмкүнчүлүк.",
            "Сен ойлогондон да күчтүүсүң!"
        ]
    },
    "fact": {
        "en": [
            "Знаете ли вы? Python назван в честь Monty Python, а не змеи.",
            "У осьминогов три сердца.",
            "Луна со временем отдаляется от Земли."
        ],
        "ru": [
            "Did you know? Python is named after Monty Python, not the snake.",
            "Octopuses have three hearts.",
            "The moon is slowly moving away from Earth."
        ],
        "kg": [
            "Билесизби? Python деген ат Monty Python шоусунан алынган.",
            "Октопустун үч жүрөгү бар.",
            "Ай акырындык менен Жерден алыстап жатат."
        ]
    },
    "joke": {
        "en": [
            "Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 == DEC 25!",
            "Сколько программистов нужно, чтобы поменять лампочку? Ни одного — это аппаратная проблема.",
            "Что сказал ноль восьмерке? Классный ремень!"
        ],
        "ru": [
            "Why do programmers confuse Halloween and Christmas? Because OCT 31 == DEC 25!",
            "How many programmers does it take to change a light bulb? None — that's a hardware issue.",
            "What did the zero say to the eight? Nice belt!"
        ],
        "kg": [
            "Эмне үчүн программисттер Хэллоуин менен Рождествону чаташтырышат? Себеби OCT 31 == DEC 25!",
            "Программист лампочканы кантип алмаштырат? Ал муну аппараттык көйгөй деп эсептейт.",
            "Нөл сегизге эмне деди? Жакшы кур экен!"
        ]
    },
    "math": {
        "en": ["Введите выражение, например: 'сколько будет 5 + 7'"],
        "ru": ["Enter an expression, e.g., 'what is 5 + 7'"],
        "kg": ["Мисалды жазыңыз, мисалы: '5 + 7 канча болот'"]
    },
    "quote": {
        "ru": [
            "“Be yourself; everyone else is already taken.” – Oscar Wilde",
            "“Happiness is a journey, not a destination.”",
            "“It's better to regret what you did than what you didn't do.”"
        ],
        "en": [
            "«Будь собой, прочие роли уже заняты.» – Оскар Уайльд",
            "«Счастье — это путь, а не пункт назначения.»",
            "«Лучше сделать и пожалеть, чем не сделать и пожалеть.»"
        ],
        "kg": [
            "«Өзүң бол, калган ролдор ээленип калган.» – Оскар Уайльд",
            "«Бактылуулук — бул жол, максат эмес.»",
            "«Кылганыңа  өкүнгөн жакшы, кылбаганыңа караганда.»"
        ]
    },
    "random": {
        "en": [f"Случайное число от 1 до 100: {random.randint(1, 100)}"],
        "ru": [f"Random number between 1 and 100: {random.randint(1, 100)}"],
        "kg": [f"1 менен 100 ортосундагы сан: {random.randint(1, 100)}"]
    },
    "weather": {
        "en": ["Я пока не подключён к погодным данным. Но выгляни в окно! ☀️"],
        "ru": ["I'm not connected to weather data yet. But check the window! ☀️"],
        "kg": ["Азырынча аба ырайы боюнча маалымат жок. Терезени кара! ☀️"]
    },
    "translate": {
        "en": ["Укажи язык и текст для перевода: 'переведи на английский привет'"],
        "ru": ["Specify language and text: 'translate to Russian hello'"],
        "kg": ["Кайсы тилге жана кандай сөз — жазыңыз: 'англисче котор' деген сыяктуу"]
    },
    "timer": {
        "ru": ["Укажите, на сколько секунд поставить таймер: 'таймер на 10 секунд'"],
        "en": ["Say how long to set the timer: 'set timer for 10 seconds'"],
        "kg": ["Канча секундка таймер коюуну жазыңыз: '10 секундга таймер'"]
    }
}
# Вопросы про личность
IDENTITY_QUESTIONS = [
    {"phrases": ["ты кто", "ты что", "кто ты"], "response": "Я — бот-помощник.", "lang": "ru"},
    {"phrases": ["who are you", "what are you"], "response": "I am a helpful chatbot.", "lang": "en"},
    {"phrases": ["сен кимсин", "ким болосуң"], "response": "Мен жардамчы ботмун.", "lang": "kg"}
]

def get_response_by_command(command, lang):
    responses = EXTRA_COMMAND_RESPONSES.get(command, {})
    if not responses:
        return None
    return random.choice(responses.get(lang, []))

def evaluate_expression(text):
    try:
        # Простые выражения: 5 + 7, 10 * 2
        text = text.lower().replace("сколько будет", "").replace("what is", "").strip()
        text = re.sub(r"[^\d\+\-\*/\.\(\)]", "", text)
        return str(eval(text))
    except Exception:
        return None
def get_valid_chart_types():
    chart_keys = ["price", "sales", "size", "district"]
    valid_chart_types = {}
    for key in chart_keys:
        for synonym in DEFAULT_CHART_INTENTS.get(key, []):
            valid_chart_types[synonym] = key
    return valid_chart_types

unknown_currency_attempts = {}

def detect_language_by_message(text):
    text = text.lower()

    kyrgyz_words = ['акча', 'сом', 'кандайсын', 'жакшы', 'жардам',
                    'канча', 'валюта', 'курс', 'жардам', 'сен кимсин']

    russian_words = ['привет', 'валюта', 'курс', 'помощь', 'график',
                     'курс', 'валюта', 'ты кто', 'сколько стоит', 'сколько тебе лет']

    english_words = ['hello', 'currency', 'rate', 'help', 'chart',
                     'currency', 'how much', 'who are you', 'what are you', 'rate']

    kg_count = sum(w in text for w in kyrgyz_words)
    ru_count = sum(w in text for w in russian_words)
    en_count = sum(w in text for w in english_words)

    if ru_count >= max(en_count, kg_count):
        return 'ru'
    elif en_count >= max(ru_count, kg_count):
        return 'en'
    else:
        return 'kg'  # По умолчанию киргизский

def process_user_message(user_message: str, user_id=None):
    # Удаляем команды — просто разбиваем текст на 3 части по пробелам, не меняем названия функций
    if user_message.startswith("/"):
        parts = user_message.split(" ", 2)
        if len(parts) < 3:
            # Если меньше 3 частей — добавляем пустые, чтобы не ломать логику
            parts += [""] * (3 - len(parts))
        user_message = " ".join(parts)

    low_msg = user_message.lower().strip()
    lang = detect_language_by_message(user_message)  # Например, 'ru', 'en', 'kg'

    # Проверка фраз типа "Сколько стоит USD?"
    currency_patterns = [
        r"(сколько стоит)\s+([a-zA-Z]{3})",
        r"(what'?s|how much is)\s+([a-zA-Z]{3})",
        r"(канча)\s+([a-zA-Z]{3})"
    ]

    for pattern in currency_patterns:
        match = re.search(pattern, low_msg)
        if match:
            currency_code = match.group(2).upper()
            try:
                currency_obj = Currency.objects.get(code=currency_code)
                return f"{currency_code}: {currency_obj.rate}", None
            except Currency.DoesNotExist:
                if user_id:
                    if unknown_currency_attempts.get(user_id) == currency_code:
                        return {
                            'ru': f"Извините, такой валюты нет в нашей базе.",
                            'en': f"Sorry, this currency is not in our database.",
                            'kg': f"Кечиресиз, бул валюта бизде жок."
                        }[lang], None
                    unknown_currency_attempts[user_id] = currency_code
                return {
                    'ru': f"Вы уверены, что правильно написали валюту {currency_code}?",
                    'en': f"Are you sure you typed the currency {currency_code} correctly?",
                    'kg': f"{currency_code} валютасын туура жаздыңызбы?"
                }[lang], None
    # Проверка на запрос построить график
    valid_chart_types = get_valid_chart_types()
    for word in low_msg.split():
        if word in valid_chart_types:
            chart_type = valid_chart_types[word]
            # Генерация графика
            chart_path = generate_chart(chart_type)
            return _("For sure!:"), chart_path

    # Поиск в интернете (duckduckgo) если есть команда "найди" или "search"
    if "найди" in low_msg or "search" in low_msg:
        query = low_msg.replace("найди", "").replace("search", "").strip()
        search_results = search_duckduckgo(query)
        return search_results, None
    # Проверка на маты
    for lang_code, bad_words in profanity_words.items():
        if any(bad_word in low_msg for bad_word in bad_words):
            return profanity_warning[lang_code], None
    if any(cmd in user_message.lower() for cmd in COMMANDS["math"]):
        lang = detect_language_by_message(user_message)
        result = evaluate_expression(user_message)
        if result:
            return {
                "ru": f"The answer is: {result}",
                "en": f"The answer is: {result}",
                "kg": f"Жооп: {result}"
            }.get(lang, str(result))  # Возвращаем строку напрямую, а не словарь с "text"

    # Проверка на вопросы о личности
    for entry in IDENTITY_QUESTIONS:
        if any(q in low_msg for q in entry["phrases"]):
            return entry["response"], None
    for l, phrases in greeting_variants.items():
        if any(p in low_msg for p in phrases):
            return random.choice(greeting_replies[l])

    # Проверка "как дела"
    for l, phrases in how_are_you_variants.items():
        if any(p in low_msg for p in phrases):
            return random.choice(how_are_you_replies[l])

    # Проверка прощаний
    for l, phrases in farewell_variants.items():
        if any(p in low_msg for p in phrases):
            return random.choice(farewell_replies[l])

    # Команда help
    if "help" in low_msg or "помощь" in low_msg or "жардам" in low_msg:
        return help_message, None

    for command, synonyms in COMMANDS.items():
        if any(syn in low_msg for syn in synonyms):
            return EXTRA_COMMAND_RESPONSES[command][lang], None

    bot_reply = {
        'ru': "Извините, я вас не понял. Попробуйте другую формулировку.",
        'en': "Sorry, I did not understand you. Try rephrasing.",
        'kg': "Кечиресиз, мен сизди түшүнгөн жокмун. Башкача айтыңызчы."
    }[lang]

    return bot_reply, None  # Всегда возвращаем кортеж (ответ, изображение)
