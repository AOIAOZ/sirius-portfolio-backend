from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from portfolio.models import Achievement
from tags.models import Tag


class PortfolioTests(APITestCase):
    def setUp(self):
        # 1. Создаем пользователей
        self.user = CustomUser.objects.create_user(
            username='student1',
            email='s1@test.com',
            password='password123',
            first_name='Ivan',
            last_name='Ivanov',
            role=CustomUser.Role.STUDENT
        )
        self.other_user = CustomUser.objects.create_user(
            username='student2',
            email='s2@test.com',
            password='password123',
            role=CustomUser.Role.STUDENT
        )

        # 2. Создаем тег
        self.tag_science = Tag.objects.create(value='science', label='Наука')

        # 3. Получаем JWT токен для основного юзера
        response = self.client.post('/api/v1/auth/token/', {
            'username': 'student1',
            'password': 'password123'
        })
        self.token = response.data['access']

        # Настраиваем клиент на использование токена
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_my_profile(self):
        """Тест получения своего профиля"""
        url = reverse('my_profile')  # /api/v1/profile/me/
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'student1')

    def test_update_profile_mapping(self):
        """Тест обновления профиля с маппингом полей (edyear, spec)"""
        url = reverse('my_profile')
        data = {
            "first_name": "NewName",
            "edyear": 3,
            "spec": "Robotics"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем базу данных
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "NewName")
        self.assertEqual(self.user.studentprofile.education_year, 3)
        self.assertEqual(self.user.studentprofile.specialty, "Robotics")

    def test_create_achievement(self):
        """Тест создания достижения с тегами"""
        url = reverse('achievement_create')  # /api/v1/profile/achievment/
        data = {
            "title": "Hackathon Winner",
            "description": "First place",
            "tags": ["science"]  # Отправляем список value тегов
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что ачивка создалась и привязалась к юзеру
        achievement = Achievement.objects.get(title="Hackathon Winner")
        self.assertTrue(self.user in achievement.users.all())
        self.assertTrue(self.tag_science in achievement.tags.all())

    def test_security_edit_others_achievement(self):
        """Тест безопасности: нельзя редактировать чужую ачивку"""
        # Создаем ачивку второго пользователя
        ach = Achievement.objects.create(title="User2 Achievement")
        ach.users.add(self.other_user)

        url = reverse('achievement_detail', kwargs={'id': ach.id})

        # Пытаемся редактировать от имени student1
        data = {"title": "Hacked Title"}
        response = self.client.post(url, data)  # POST Update

        # Должен быть 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_achievement(self):
        """Тест удаления своей ачивки"""
        ach = Achievement.objects.create(title="My Achievement")
        ach.users.add(self.user)

        url = reverse('achievement_detail', kwargs={'id': ach.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Achievement.objects.filter(id=ach.id).exists())
