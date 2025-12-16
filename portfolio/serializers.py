from rest_framework import serializers
from .models import StudentProfile
from .models import Document


class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    patronymic = serializers.CharField(source='user.patronymic', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email', 'avatar', 'bio', 'birth_date',
                  'phone_number']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'recognized_text']
