from django.urls import path
from .views import (
    MyProfileView,
    DocumentUploadView,
    UserPhotoView,
    UserProfileDetailView,
    UserAchievementsListView,
    CreateAchievementView,
    AchievementDetailView
)

urlpatterns = [
    # Текущий профиль и документы
    path('me/', MyProfileView.as_view(), name='my_profile'),
    path('upload/', DocumentUploadView.as_view(), name='document_upload'),

    # Управление фото (/photo GET, POST, DELETE)
    path('photo/', UserPhotoView.as_view(), name='user_photo'),

    # Просмотр/Редактирование любого пользователя (/user/{id} GET, POST)
    path('user/<int:user__id>/', UserProfileDetailView.as_view(), name='user_detail'),

    # Ачивки пользователя (/user/{id}/achievments GET)
    path('user/<int:user_id>/achievments/', UserAchievementsListView.as_view(), name='user_achievements'),

    # Создание ачивки (POST /achievment)
    path('achievment/', CreateAchievementView.as_view(), name='achievement_create'),

    # Управление конкретной ачивкой (/achievment/{id} GET, POST, DELETE)
    path('achievment/<int:id>/', AchievementDetailView.as_view(), name='achievement_detail'),
]
