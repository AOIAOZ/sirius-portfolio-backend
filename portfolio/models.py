from django.db import models
from users.models import CustomUser


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='studentprofile')

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')

    def __str__(self):
        return f"Профиль студента {self.user.username}"


class Document(models.Model):
    """Модель для хранения загруженных документов."""
    title = models.CharField(max_length=255, verbose_name="Название документа")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    # upload_to='documents/' - все файлы будут складываться в папку media/documents/
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    recognized_text = models.TextField(blank=True, null=True, verbose_name="Распознанный текст")

    def __str__(self):
        return self.title
