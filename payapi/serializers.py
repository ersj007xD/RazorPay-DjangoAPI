from rest_framework import serializers
from .models import Coffee

class CofeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = ['id', 'name', 'amount', 'payment_id', 'paid']