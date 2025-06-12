from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatMessage
from .logic import process_user_message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatMessage
from .logic import process_user_message  # Твой бот
import json
from rest_framework import status

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_chat(request):
    if request.method == "POST":
        chat = Chat.objects.create(user=request.user, name="Новый чат")
        return JsonResponse({"chat_id": chat.id, "name": chat.name})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_chats(request):
    chats = Chat.objects.filter(user=request.user).values("id", "name", "created_at")
    return JsonResponse(list(chats), safe=False)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_chat_messages(request, chat_id):
    messages = ChatMessage.objects.filter(chat_id=chat_id).order_by("timestamp").values(
        "id", "text", "is_user", "timestamp", "image_url"
    )
    return JsonResponse(list(messages), safe=False)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request, chat_id):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text")

        user_msg = ChatMessage.objects.create(
            chat_id=chat_id,
            user=request.user,
            text=text,
            is_user=True
        )

        result = process_user_message(text)

        # Проверка, сколько значений вернулось
        if isinstance(result, tuple) and len(result) == 2:
            bot_reply, image_url = result
        else:
            bot_reply = result
            image_url = None

        ChatMessage.objects.create(
            chat_id=chat_id,
            user=request.user,
            text=bot_reply,
            is_user=False,
            image_url=image_url
        )

        return JsonResponse({
            "status": "ok",
            "user_msg": user_msg.text,
            "bot_reply": bot_reply,
            "image_url": image_url
        })
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_chat(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id, user=request.user)
    except Chat.DoesNotExist:
        return Response({"detail": "Чат не найден или доступ запрещён"}, status=status.HTTP_404_NOT_FOUND)

    chat.delete()
    return Response({"status": "ok", "message": "Чат успешно удалён"}, status=status.HTTP_200_OK)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rename_chat(request, chat_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_name = data.get("name")
        Chat.objects.filter(id=chat_id, user=request.user).update(name=new_name)
        return JsonResponse({"status": "ok", "new_name": new_name})

MAX_HISTORY_MESSAGES = 50

def trim_history(user):
    messages = ChatMessage.objects.filter(user=user).order_by("-timestamp")
    if messages.count() > MAX_HISTORY_MESSAGES:
        for msg in messages[MAX_HISTORY_MESSAGES:]:
            msg.delete()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_chat_history(request):
    user = request.user
    messages = ChatMessage.objects.filter(user=user).order_by("timestamp")
    data = [
        {
            "text": msg.text,
            "isUser": msg.is_user,
            "image": msg.image_url,
            "timestamp": msg.timestamp,
        }
        for msg in messages
    ]
    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_view(request):
    user_message = request.data.get("message", "").strip()
    user = request.user

    if not user_message:
        return Response({"bot": "Пожалуйста, введите сообщение.", "image_url": None})

    trim_history(user)

    def save_message(text, is_user=True, image_url=None):
        ChatMessage.objects.create(user=user, text=text, is_user=is_user, image_url=image_url)

    save_message(user_message, is_user=True)

    bot_reply, image_url = process_user_message(user_message)

    save_message(bot_reply, is_user=False, image_url=image_url)

    return Response({"bot": bot_reply, "image_url": image_url})
