from rest_framework import serializers
from .models import CustomUser


class StudentRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic', 'gender', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'patronymic': {'required': False, 'allow_blank': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data, role=CustomUser.Role.STUDENT)
        return user
