from django.db import models
from users.models import CustomUser
from tags.models import Tag


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='studentprofile')

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')

    education_year = models.PositiveIntegerField(null=True, blank=True, verbose_name='Курс обучения')
    specialty = models.CharField(max_length=255, null=True, blank=True, verbose_name='Специальность')

    def __str__(self):
        return f"Профиль студента {self.user.username}"


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название документа")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    recognized_text = models.TextField(blank=True, null=True, verbose_name="Распознанный текст")

    def __str__(self):
        return self.title


class Achievement(models.Model):
    users = models.ManyToManyField(CustomUser, related_name='achievements', verbose_name="Пользователи")

    tags = models.ManyToManyField(Tag, blank=True, related_name='achievements', verbose_name="Теги")

    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание/Комментарии")
    file = models.FileField(upload_to='achievements/', null=True,
                            blank=True, verbose_name="Файл подтверждения")

    is_verified = models.BooleanField(default=False, verbose_name="Подтверждено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title
