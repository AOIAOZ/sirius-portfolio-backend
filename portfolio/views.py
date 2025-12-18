from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import StudentProfile, Achievement
from .serializers import StudentProfileSerializer, DocumentSerializer, AchievementSerializer


class MyProfileView(generics.RetrieveUpdateAPIView):
    """
    Получение и обновление профиля ТЕКУЩЕГО пользователя.
    """
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.studentprofile


class DocumentUploadView(APIView):
    """
    Эндпоинт для загрузки документов.
    Принимает POST-запросы с multipart/form-data.
    Может опционально распознавать текст в файле.
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        document = serializer.save()
        response_data = serializer.data

        should_recognize = (request.query_params.get('recognize', 'false').lower() == 'true' or
                            request.data.get('recognize', 'false').lower() == 'true')

        if should_recognize:
            try:
                recognized_text = "Mocked Text Result"
                if recognized_text:
                    document.recognized_text = recognized_text
                    document.save()
                    response_data['recognized_text'] = recognized_text
            except Exception as e:
                print(f"Error: {e}")

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserPhotoView(APIView):
    """
    /photo GET, POST, DELETE
    Управление аватаром ТЕКУЩЕГО пользователя.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile = request.user.studentprofile
        if profile.avatar:
            return Response({'avatar': request.build_absolute_uri(profile.avatar.url)})
        return Response({'avatar': None})

    def post(self, request):
        profile = request.user.studentprofile

        file_obj = request.FILES.get('file') or request.FILES.get('avatar')

        if not file_obj and request.FILES:
            file_obj = list(request.FILES.values())[0]

        if not file_obj:
            return Response({"error": "Файл не предоставлен"}, status=status.HTTP_400_BAD_REQUEST)

        profile.avatar = file_obj
        profile.save()
        return Response({
            'status': 'Avatar updated',
            'avatar': request.build_absolute_uri(profile.avatar.url)
        })

    def delete(self, request):
        profile = request.user.studentprofile
        if profile.avatar:
            profile.avatar.delete(save=False)
            profile.avatar = None
            profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    /user/{id} GET, POST
    Получение данных пользователя по ID.
    Обновление разрешено только владельцу или админу.
    """
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'user__id'

    def get_object(self):
        user_id = self.kwargs.get('user__id')
        return get_object_or_404(StudentProfile, user__id=user_id)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if (request.method in ['PUT', 'PATCH', 'POST']
                and obj.user != request.user
                and not request.user.is_staff):
            self.permission_denied(request, message="Вы не можете редактировать чужой профиль.")

    def post(self, request, *args, **kwargs):
        """Эмуляция PUT через POST для совместимости."""
        return self.update(request, *args, **kwargs)


class CreateAchievementView(generics.CreateAPIView):
    """
    POST /achievment/
    Создание достижения. Текущий пользователь становится владельцем.
    """
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        achievement = serializer.save()
        achievement.users.add(self.request.user)


class UserAchievementsListView(generics.ListAPIView):
    """
    GET /user/{id}/achievments
    Список достижений конкретного пользователя.
    """
    serializer_class = AchievementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Achievement.objects.filter(users__id=user_id).order_by('-created_at')


class AchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, POST (Update), DELETE /achievment/{id}
    """
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if not user.is_staff:
            if not instance.users.filter(id=user.id).exists():
                return Response(
                    {"detail": "Вы не являетесь владельцем этого достижения."},
                    status=status.HTTP_403_FORBIDDEN
                )

            if instance.users.count() > 1:
                return Response(
                    {"detail": "Групповое достижение редактировать нельзя."},
                    status=status.HTTP_403_FORBIDDEN
                )

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(is_verified=False)
        else:
            serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if not user.is_staff:
            if instance.users.count() > 1:
                instance.users.remove(user)
            else:
                instance.delete()
        else:
            instance.delete()

    def post(self, request, *args, **kwargs):
        """Эмуляция Update через POST."""
        return self.update(request, *args, **kwargs)
