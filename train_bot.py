import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartHomeProject.settings")  # укажи свой путь к settings
django.setup()

from chat.nlp_ml import ChatbotNLP

chatbot = ChatbotNLP()
chatbot.train_model()
