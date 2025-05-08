# serializers.py
from rest_framework import serializers
from .models import Benevole

class BenevoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benevole
        fields = '__all__'
