from rest_framework import serializers
from .models import Paste


class CreatePasteSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_blank=False)
    ttl_seconds = serializers.IntegerField(required=False, min_value=1)
    max_views = serializers.IntegerField(required=False, min_value=1)
    
    
    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty")
        return value
    

class PasteResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    url = serializers.CharField()
    
    
class PasteDetailSerializer(serializers.Serializer):
    content = serializers.CharField()
    remaining_views = serializers.IntegerField(allow_null=True)
    expires_at = serializers.IntegerField(allow_null=True)