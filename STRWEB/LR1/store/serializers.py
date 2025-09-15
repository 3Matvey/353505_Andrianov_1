from rest_framework import serializers
from .models import CompanyNews

class CompanyNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyNews
        fields = ['id', 'title', 'content', 'image', 'published_at']
        read_only_fields = ['id', 'published_at']
