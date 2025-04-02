### API для Django-проекта Yatube | Яндекс Практикум  

## Краткое описание  
Это API для социальной платформы Yatube, разработанное на Django REST Framework. Позволяет:  
- Создавать, редактировать и удалять публикации  
- Оставлять комментарии  
- Подписываться на авторов и управлять подписками  

## Установка и запуск  
1. Клонируйте репозиторий:  
   ```bash
   git clone <адрес репозитория>
   ```  

2. Перейдите в папку проекта и создайте виртуальное окружение (Python 3.12+):  
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   .\venv\Scripts\activate   # для Windows
   ```  

3. Установите зависимости:  
   ```bash
   pip install -r requirements.txt
   ```  

4. Примените миграции:  
   ```bash
   python yatube_api/manage.py migrate
   ```  

5. Создайте суперпользователя (опционально):  
   ```bash
   python yatube_api/manage.py createsuperuser
   ```  

6. Запустите сервер:  
   ```bash
   python yatube_api/manage.py runserver
   ```  

---  

## Работа с API  

### Для неавторизованных пользователей (только чтение)  
- `GET /api/v1/posts/` – список публикаций (с пагинацией через `limit` и `offset`)  
- `GET /api/v1/posts/{id}/` – детали публикации  
- `GET /api/v1/groups/` – список сообществ  
- `GET /api/v1/groups/{id}/` – информация о сообществе  
- `GET /api/v1/{post_id}/comments/` – комментарии к публикации  
- `GET /api/v1/{post_id}/comments/{id}/` – конкретный комментарий  

### Для авторизованных пользователей  
**Публикации:**  
- `POST /api/v1/posts/` – создать запись  
  ```json
  {
    "text": "Текст поста",
    "image": "base64-encoded изображение (опционально)",
    "group": "ID сообщества (опционально)"
  }
  ```  
- `PUT/PATCH /api/v1/posts/{id}/` – обновить запись (полное/частичное)  
- `DELETE /api/v1/posts/{id}/` – удалить запись  

**Комментарии:**  
- `POST /api/v1/posts/{post_id}/comments/` – добавить комментарий  
- `PUT/PATCH/DELETE /api/v1/posts/{post_id}/comments/{id}/` – управление комментарием  

**Подписки:**  
- `GET /api/v1/follow/` – список подписок  
- `POST /api/v1/follow/` – подписаться на автора  
  ```json
  {
    "following": "username автора"
  }
  ```  

> **Важно:**  
> - Изменять или удалять контент могут только его авторы.  
> - Анонимные запросы на запись запрещены.  

API использует JWT-аутентификацию. Для доступа к закрытым эндпоинтам добавьте заголовок:  
```
Authorization: Bearer <ваш_токен>
```
