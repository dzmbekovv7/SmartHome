from rest_framework import serializers
from .models import AgentApplication
from .models import AgencyCompany, Advantage, Review

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyCompany
        fields = '__all__'

class AdvantageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantage
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class AgentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentApplication
        fields = [
            'id',
            'created_at',
            'full_name',
            'phone',
            'passport_number',
            'passport_issued_by',
            'passport_issue_date',
            'address',
            'additional_info',
        ]

