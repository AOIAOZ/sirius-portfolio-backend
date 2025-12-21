from rest_framework import serializers
from .models import StudentProfile, Document, Achievement
from users.models import CustomUser
from tags.models import Tag


class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    patronymic = serializers.CharField(source='user.patronymic', required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    edyear = serializers.IntegerField(source='education_year', required=False, allow_null=True)
    spec = serializers.CharField(source='specialty', required=False, allow_blank=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'patronymic', 'role',
            'edyear', 'spec',
            'avatar', 'bio', 'birth_date', 'phone_number'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Если пришли данные для User, обновляем их
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'patronymic' in user_data:
            user.patronymic = user_data['patronymic']

        user.save()

        return super().update(instance, validated_data)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'recognized_text']


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']


class AchievementSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='value',
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Achievement
        fields = ['id', 'title', 'description', 'file', 'is_verified', 'created_at', 'tags']
        read_only_fields = ['id', 'is_verified', 'created_at']
