from .models import HstaData
from rest_framework import serializers


class HstaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HstaData
        fields = ['id', 'ISBN', 'title', 'author', 'chapter', 'edition', 'zip_file', 'email']
