import re
import json
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "chatbot_ml_model.pkl")
DATA_PATH = os.path.join(settings.BASE_DIR, "chatbot_training_data.json")

# Обычные команды (интенты)
DEFAULT_COMMAND_INTENTS = {
    "greeting": ["привет", "здравствуй", "добрый день", "хай"],
    "farewell": ["пока", "до свидания", "увидимся", "бай"],
    "help": ["помощь", "что ты умеешь", "help"],
}

# Команды связанные с графиками
DEFAULT_CHART_INTENTS = {
    "price": ["цена", "стоимость", "цену", "ценах", "price"],
    "sales": ["продажи", "продано", "количество", "продажи", "sales"],
    "size": ["площадь", "размер", "метров", "площади", "метр", "size"],
    "district": ["район", "районы", "районе", "районов", "место", "места", "локация", "локации", "локаций", "district"],
    "chart": ["график", "диаграмма", "chart", "plot", "графики"]
}



class ChatbotNLP:
    def __init__(self):
        self.pipeline = None
        self.load_model()

    def load_training_data(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            data = {"texts": [], "labels": []}
            # Объединяем оба словаря, чтобы обучить модель на всех интентах
            combined_intents = {**DEFAULT_COMMAND_INTENTS, **DEFAULT_CHART_INTENTS}
            for label, examples in combined_intents.items():
                data["texts"].extend(examples)
                data["labels"].extend([label] * len(examples))
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            return data

    def save_training_data(self, data):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def train_model(self):
        data = self.load_training_data()
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LogisticRegression(max_iter=1000))
        ])
        self.pipeline.fit(data["texts"], data["labels"])
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self.pipeline, f)

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                self.pipeline = pickle.load(f)
        else:
            self.train_model()

    def predict_intent(self, text: str) -> str:
        if not self.pipeline:
            self.train_model()
        pred = self.pipeline.predict([text])[0]
        return pred

    def update_training(self, text: str, label: str):
        data = self.load_training_data()
        data["texts"].append(text)
        data["labels"].append(label)
        self.save_training_data(data)
        self.train_model()

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r"[^а-яa-z0-9\s]", "", text)
        return text

    def handle_message(self, text: str):
        text = self.preprocess_text(text)
        intent = self.predict_intent(text)
        return intent
