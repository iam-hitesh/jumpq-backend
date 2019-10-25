from datetime import datetime

from rest_framework import serializers

from users import models


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for All Kind Of Users
    """

    default_lang = serializers.CharField(source='get_default_lang_display')
    user_type = serializers.CharField(source='get_user_type_display')

    class Meta(object):
        model = models.User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'write_only': True},
            'is_staff': {'write_only': True},
            'user_type': {'write_only': True},
        }
        read_only_fields = ['user_id']
        lookup_field = 'mobile'

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        instance.save()

        return instance


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for Country
    """

    class Meta(object):
        model = models.Country
        fields = '__all__'
        read_only_fields = ['country_id']
        filter_kwargs = {'is_deleted': False}


class StateSerializer(serializers.ModelSerializer):
    """
    Serializer for State
    """

    class Meta(object):
        model = models.State
        fields = '__all__'
        extra_kwargs = {
            'country': {'lookup_field': 'country_name'}
        }
        filter_kwargs = {'is_deleted': False}


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer for State
    """

    class Meta(object):
        model = models.City
        fields = '__all__'
        extra_kwargs = {
            'state': {'lookup_field': 'state_name'}
        }
        filter_kwargs = {'is_deleted': False}