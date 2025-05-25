from channels.generic.websocket import AsyncWebsocketConsumer
import json

# This will be a simple in-memory set for demo purposes.
# In production, use Redis or a persistent store.
ONLINE_USERS = set()

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        ONLINE_USERS.add(self.user_id)
        await self.channel_layer.group_add("online_users", self.channel_name)
        await self.accept()
        # Broadcast updated user list
        await self.channel_layer.group_send(
            "online_users",
            {
                "type": "online.users",
                "users": list(ONLINE_USERS)
            }
        )

    async def disconnect(self, close_code):
        ONLINE_USERS.discard(self.user_id)
        await self.channel_layer.group_discard("online_users", self.channel_name)
        # Broadcast updated user list
        await self.channel_layer.group_send(
            "online_users",
            {
                "type": "online.users",
                "users": list(ONLINE_USERS)
            }
        )

    async def online_users(self, event):
        await self.send(text_data=json.dumps({
            "event": "getOnlineUsers",
            "users": event["users"]
        }))
