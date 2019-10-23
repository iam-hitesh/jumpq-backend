from datetime import datetime

from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for All Kind Of Users
    """

    default_lang = serializers.CharField(source='get_default_lang_display')
    user_type = serializers.CharField(source='get_user_type_display')

    class Meta(object):
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'write_only': True},
            'is_staff': {'write_only': True},
        }