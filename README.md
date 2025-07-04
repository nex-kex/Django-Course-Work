# Сервис управления рассылками сообщений

## Описание проекта
Веб-приложение на Django для управления email-рассылками, клиентами и сообщениями. Сервис позволяет создавать, редактировать и отправлять рассылки, собирать статистику и управлять доступом пользователей.

## Функционал (Часть 1)
### 1. Управление клиентами
- Добавление / редактирование / удаление получателей рассылки
- Поля модели:
  - Email (уникальный)
  - ФИО
  - Комментарий

### 2. Управление сообщениями
- CRUD для шаблонов писем
- Поля:
  - Тема письма
  - Тело письма

### 3. Управление рассылками
- Создание / редактирование / удаление рассылок
- Поля:
  - Время начала / окончания
  - Статус
    - Создана
    - Запущена
    - Завершена
  - Связанное сообщение
  - Список получателей

### 4. Отправка сообщений
- Ручной запуск через UI и командную строку

### 5. Логирование попыток
- История отправок с:
  - Временем попытки
  - Статусом (успех / неудача)
  - Ответом сервера

### 6. Главная страница
- Статистика:
  - Всего рассылок
  - Активных рассылок
  - Уникальных клиентов

## Расширенный функционал (Часть 2)
### 7. Аутентификация
- Регистрация с подтверждением email
- Вход / выход
- Восстановление пароля

### 8. Статистика
- Отчеты по успешным / неудачным попыткам рассылок
- Количество отправленных сообщений

### 9. Система ролей
**Пользователь:**
- Управление своими рассылками и клиентами
- Просмотр своей статистики

**Менеджер:**
- Просмотр всех рассылок и клиентов
- Блокировка пользователей
- Отключение рассылок

### 10. Кеширование
- Серверное и клиентское кеширование

## Установка
1. Клонировать репозиторий
2. Настроить .env файл по примеру `.env.example`
3. Выполнить миграции: `python manage.py migrate`
4. Запустить сервер: `python manage.py runserver`

## Использование
- Админ-панель: `/admin`
- Главная страница: `/`
