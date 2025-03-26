from rest_framework import serializers
from .models import Feedbacks

class FeedbacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = '__all__'