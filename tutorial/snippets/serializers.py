from rest_framework import serializers
from django.contrib.auth import get_user_model

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


USER = get_user_model()


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Snippet
        fields = [
            'id', 'title', 'code', 'linenos', 'language', 'style',
            'owner',
            ]


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all())
    
    class Meta:
        model = USER
        fields = ['id', 'email', 'snippets']
