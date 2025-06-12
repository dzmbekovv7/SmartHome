from rest_framework import serializers
from .models import House, Comment
from apiauth.models import User
from .models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'rate', 'description']

class CurrencyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'rate', 'description', 'updated_at']
class HouseSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = [
            'id', 'name', 'description', 'image',
            'latitude', 'longitude',
            'rooms', 'square', 'price', 'has_pool',
            'features_internal', 'features_external',
            'views', 'likes', 'comments', 'location'
        ]

    def get_likes(self, obj):
        return [user.id for user in obj.liked_by.all()]

# serializers.py

class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']

class CommentSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'house', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

# serializers.py

class LikeSerializer(serializers.Serializer):
    house = serializers.PrimaryKeyRelatedField(queryset=House.objects.all())
    liked = serializers.BooleanField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
