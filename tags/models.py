from django.db import models


class Tag(models.Model):
    """Модель для хранения имеющихся тегов."""
    value = models.CharField(max_length=255, verbose_name="Системное имя тега")
    label = models.CharField(max_length=255, blank=True, verbose_name="Читабельное имя тега")

    def __str__(self):
        return self.value
