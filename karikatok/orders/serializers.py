from rest_framework import serializers
from .models import Orders

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username in responses

    class Meta:
        model = Orders
        fields = ['id', 'user', 'data', 'qr_code', 'created_at']
        read_only_fields = ['user', 'qr_code', 'created_at']
