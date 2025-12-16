from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', _('Студент')
        TUTOR = 'TUTOR', _('Тьютор')
        STAFF = 'STAFF', _('Сотрудник')
        COMPANY = 'COMPANY', _('Представитель компании')

    class Gender(models.TextChoices):
        MALE = 'MALE', _('Мужской')
        FEMALE = 'FEMALE', _('Женский')

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    patronymic = models.CharField(_('Отчество'), max_length=150, blank=True)

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(_('Роль'), max_length=50, choices=Role.choices, default=Role.STUDENT)
    gender = models.CharField(_('Пол'), max_length=10, choices=Gender.choices, blank=True)

    # TODO: EMAIL LOGIN (NOW ONLY USERNAME)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        """Возвращает полное ФИО."""
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()
