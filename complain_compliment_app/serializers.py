from rest_framework import serializers
from .models import Feedbacks, AdminResponse

class FeedbacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = '__all__'

class AdminResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminResponse
        fields = '__all__'