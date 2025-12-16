from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .models import StudentProfile


@receiver(post_save, sender=CustomUser)
def create_student_profile(sender, instance, created, **kwargs):
    """
    @receiver - отвечает за выполнение функции после того, как...
    Сигнал для автоматического создания профиля, когда создается новый
    пользователь с ролью СТУДЕНТ.
    """
    if created and instance.role == CustomUser.Role.STUDENT:
        StudentProfile.objects.create(user=instance)
