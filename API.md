### 🔐 1. Авторизация (Auth)

**Base URL:** `/api/v1/auth/`

#### Получение токена (Логин)

- **POST** `/token/`
- **Body:** `{ "username": "login", "password": "123" }`
- **Response:** `{ "access": "...", "refresh": "..." }`
- _Примечание:_ `access` токен живет недолго, его нужно посылать в заголовке `Authorization: Bearer <token>` ко всем закрытым запросам.

#### Регистрация

- **POST** `/register/`
- **Body:**
  ```json
  {
    "username": "Ivan2000",
    "email": "ivan@example.com",
    "password": "pass",
    "password2": "pass",
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "patronymic": "Ivanovich",
    "gender": "MALE"
  }
  ```

---

### 👤 2. Профиль (Profile)

**Base URL:** `/api/v1/profile/`

#### Мой профиль (Текущий юзер)

- **GET** `/me/` — получить данные.
- **PATCH / PUT** `/me/` — обновить данные.
- **Response / Body:**
  ```json
  {
    "id": 1,
    "username": "Ivan2000",
    "email": "ivan@mail.ru",
    "first_name": "Иван",
    "last_name": "Иванов",
    "patronymic": "Иванович",
    "role": "STUDENT",
    "edyear": 2, // Курс (mapped from education_year)
    "spec": "Informatics", // Специальность (mapped from specialty)
    "avatar": "http://.../media/avatars/img.jpg",
    "bio": "О себе...",
    "phone_number": "8900..."
  }
  ```

#### Управление Аватаром

- **GET** `/photo/` — получить ссылку на аватар.
- **POST** `/photo/` — загрузить/обновить аватар.
  - **Header:** `Content-Type: multipart/form-data`
  - **Body (FormData):** поле `file` (или `avatar`) = файл картинки.
- **DELETE** `/photo/` — удалить аватар.

#### Профиль любого пользователя (по ID)

- **GET** `/user/{id}/` — просмотр чужого/своего профиля.
- **POST** `/user/{id}/` — обновление (работает как PUT, доступно только владельцу или админу).
- **Body:** Те же поля, что и в `/me/` (`edyear`, `spec`, `first_name` и т.д.).

---

### 🏆 3. Достижения (Achievements)

**Base URL:** `/api/v1/profile/`

#### Список достижений пользователя

- **GET** `/user/{id}/achievments/`
- **Query Params:** `?page=1` (Пагинация, по 10 штук).
- **Response:**
  ```json
  {
    "count": 15,
    "next": "http://.../?page=2",
    "previous": null,
    "results": [
      {
        "id": 10,
        "title": "Хакатон 2024",
        "description": "1 место",
        "file": "http://.../file.pdf",
        "is_verified": true,
        "created_at": "2024-05-20T10:00:00Z",
        "tags": ["science", "IT"] // Массив строк (slugs)
      }
    ]
  }
  ```

#### Создание достижения

- **POST** `/achievment/`
- **Header:** `Content-Type: multipart/form-data` (если шлем файл).
- **Body (FormData):**
  - `title`: (string, required) "Название"
  - `description`: (string) "Описание"
  - `file`: (file) Сам файл
  - `tags`: (list of strings) `["science", "sport"]` — отправлять несколько полей с одним именем `tags` или через запятую, зависит от клиента, но лучше слать массив значений `value` тегов.

#### Управление конкретным достижением

- **GET** `/achievment/{id}/` — детальная инфа.
- **POST / PUT / PATCH** `/achievment/{id}/` — редактирование.
  - _Важно:_ Если редактирует обычный студент, поле `is_verified` сбрасывается в `false`.
  - _Важно:_ Если достижение групповое (владельцев > 1), редактирование запрещено (403 Forbidden), нужно писать админу.
- **DELETE** `/achievment/{id}/` — удаление.
  - Если владелец один — удаляется ачивка.
  - Если владельцев много — текущий юзер удаляется из списка владельцев ачивки.

---

### 🏷️ 4. Теги (Tags)

**Base URL:** `/api/v1/tags`

#### Список всех тегов

- **GET** `/api/v1/tags`
- **Query Params:** `?limit=10&offset=0`
- **Response:**
  ```json
  {
    "tags": [
      { "id": 1, "value": "science", "label": "Наука" },
      { "id": 2, "value": "sport", "label": "Спорт" }
    ],
    "count": 2
  }
  ```
- _Использование:_ Фронт получает этот список, чтобы показать в выпадающем списке (Select) при создании ачивки. В ачивку отправляем `value`.

---

### 📄 5. ML / Документы (Доп.)

**Base URL:** `/api/v1/profile/`

#### Загрузка документа с распознаванием

- **POST** `/upload/`
- **Query Param:** `?recognize=true`
- **Header:** `Content-Type: multipart/form-data`
- **Body:** `file`
- **Response:** Возвращает объект документа + поле `recognized_text` (если ML отработал).
