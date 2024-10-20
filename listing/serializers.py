from rest_framework import serializers
from .models import Property, Agent
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    # def create(self, validated_data):
    #     user = User(**validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    class Meta:
        model = Agent
        fields = '__all__'

    def get_properties(self, obj):
        serializer = PropertySerializer(obj.products.all(), many=True)
        return serializer.data

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = User.objects.create(**user_data)
    #     agent = Agent.objects.create(user=user, **validated_data)
    #     return agent


