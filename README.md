# Каталог книг

Веб-приложение для управления личной библиотекой с возможностью отслеживания статуса прочтения книг.

**Команда**: P3121 "The Mandela Catalogue"
**Фреймворк**: Flask (Python)
**Архитектура**: MVC (Model-View-Controller)
**База данных**: SQLite + SQLAlchemy ORM

---

## Архитектура приложения

### MVC Pattern

```
┌─────────────────────────────────────────────────────┐
│                    VIEW (Шаблоны)                    │
│  frontend/templates/ - Jinja2 + Bootstrap 5         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│              CONTROLLER (Логика)                     │
│  backend/app.py - Роуты и обработка запросов        │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│                 MODEL (Данные)                       │
│  backend/models.py - SQLAlchemy ORM модели          │
└─────────────────────────────────────────────────────┘
```

### Компоненты

####  Model (Модель) — `backend/models.py`
Отвечает за структуру данных и работу с базой данных.

**Сущности**:
- **User** — пользователь системы
  - `id`, `username`, `password_hash`
  - Связь один-ко-многим с Book

- **Book** — книга в каталоге
  - `id`, `title`, `author`, `year`, `genre`, `description`
  - `status`: not_started | reading | finished
  - `user_id`: внешний ключ на User

####  Controller (Контроллер) — `backend/app.py`
Обрабатывает HTTP-запросы и координирует работу компонентов.

**Основные функции**:
- `/`, `/login`, `/register`, `/logout` — auth
- `/users`, `/users/<id>` — пользователи
- `/books`, `/my-books`, `/books/add` — книги
- `/books/<id>/view`, `/books/<id>/edit`, `/books/<id>/delete` — CRUD
- `/books/<id>/status` — обновление статуса
- `/profile/edit` — профиль

#### View (Представление) — `frontend/templates/`
Отвечает за отображение данных пользователю.

```
templates/
├── base.html              # Layout (navbar, footer)
├── index.html             # Главная страница
├── login.html / register.html
├── error.html
├── books/
│   ├── add.html
│   ├── edit.html
│   ├── view.html
│   └── user_book_list.html
└── users/
    ├── user_list.html
    └── user_profile.html
```

---

### Работа в команде (Git Flow)

**Модель ветвления**: GitLab Flow с feature-ветками

```
main                # Стабильная версия
├── backend         # Серверная логика
├── frontend        # Клиентская часть
├── frontend-templates  # HTML-шаблоны
└── backend-models  # Модели данных
```

**Процесс**:
1. Создаём feature-ветку от `main`
2. Разрабатываем функционал
3. Делаем Pull Request
4. После код-ревью — merge в `main`

---

# Инструкция по развертыванию
## Создание виртуального окружения и активация
0. Если не установлен ```pip``` и ```python```, то установите (зависит от ОС).
1. В терминале с проектом: 
    > ```python -m venv venv```
2. Активация
    1. Windows: 
        > ```cd venv/Scripts/activate.ps1``` (PS)

        ИЛИ
        
        >  ```cd venv/Scripts/activate.bat``` (Terminal)


    2. macOS/Linux/WSL:
        > ```source venv/bin/activate```
    
## Установка зависимостей

В корневом каталоге проекта:

> ```pip install -r requirements.txt```

## Запуск

1. > ```cd backend```

2. > ```python app.py```

3. В браузере введите ```ip``` из консоли (например, 127.0.0.1) и порт (5000). Таким образом, строка поиска должна выглядеть следующим образом: ```http://127.0.0.1:5000/```


# План реализации проекта "Каталог книг"

## 1. Введение

Проект представляет собой веб-приложение для управления личной библиотекой книг с возможностью регистрации пользователей, добавления, редактирования и отслеживания статуса прочтения книг.

**Фреймворк**: Flask (Python)
**Архитектурный паттерн**: MVC (Model-View-Controller)
**База данных**: SQLite (через SQLAlchemy ORM)

---

## 2. Реализация модели ветвления кода (GitLab Flow)

### 2.1 Выранная модель
Для управления версионностью использовалась модификация **GitLab Flow** с feature-based разработкой.

### 2.2 Структура веток
- **`main`** — основная ветка, содержит стабильный код
- **`backend`** — ветка для разработки серверной логики и API
- **`frontend`** — ветка для разработки пользовательского интерфейса
- **`frontend-templates`** — ветка для работы с HTML-шаблонами
- **`backend-models`** — ветка для разработки моделей данных
- **`mvc`** — экспериментальная ветка для тестирования архитектуры MVC

### 2.3 Процесс работы
1. Создание feature-веток от `main` для каждой задачи
2. Разработка функционала в изолированных ветках
3. Использование Pull Request для код-ревью
4. Слияние (merge) утверждённых изменений в `main`
5. Создание промежуточных слияний (`Merge branch 'backend'`)

### 2.4 Примеры из истории коммитов
```
* 91670a3 Merge branch 'backend'
* 80edcbd FINALLY WE DONE WE ARE SO DONE
* c13ec4c modified: README.md
```

---

## 3. Реализация MVC во Flask

### 3.1 Model (Модель) — `backend/models.py`

**Ответственность**: управление данными и бизнес-логика

**Модели данных**:

```python
class User(db.Model):
    - id: первичный ключ
    - username: уникальное имя пользователя
    - password_hash: хеш пароля (Werkzeug security)
    - books: связь один-ко-многим с таблицей Book

class Book(db.Model):
    - id: первичный ключ
    - title: название книги
    - author: автор
    - year: год издания
    - genre: жанр
    - description: описание
    - status: статус чтения (not_started/reading/finished)
    - user_id: внешний ключ на User
```

**Особенности**:
- Использование SQLAlchemy ORM
- Каскадное удаление (`delete-orphan`)
- Ленивая загрузка связанных данных (`lazy=True`)

### 3.2 View (Представление) — `frontend/templates/`

**Ответственность**: отображение данных пользователю

**Структура шаблонов**:
```
frontend/templates/
├── base.html              # Базовый шаблон (layout)
├── index.html             # Главная страница
├── login.html             # Форма входа
├── register.html          # Форма регистрации
├── edit_profile.html      # Редактирование профиля
├── error.html             # Страница ошибок
├── books/
│   ├── add.html           # Добавление книги
│   ├── edit.html          # Редактирование книги
│   ├── user_book_list.html # Список книг
│   └── view.html          # Просмотр книги
└── users/
    ├── user_list.html     # Список пользователей
    └── user_profile.html  # Профиль пользователя
```

**Технологии**:
- Jinja2 (шаблонизатор Flask)
- Bootstrap 5 (CSS фреймворк)
- Bootstrap Icons
- Наследование шаблонов (`{% block %}`)

### 3.3 Controller (Контроллер) — `backend/app.py`

**Ответственность**: обработка HTTP-запросов и координация

**Основные функции-контроллеры**:

| Роут | Метод | Описание |
|------|-------|----------|
| `/` | GET | Главная страница со списком пользователей |
| `/login` | GET/POST | Аутентификация пользователя |
| `/register` | GET/POST | Регистрация нового пользователя |
| `/logout` | GET | Завершение сессии |
| `/users` | GET | Список всех пользователей |
| `/users/<id>` | GET | Профиль пользователя |
| `/books` | GET | Все книги |
| `/my-books` | GET | Кни текущего пользователя |
| `/users/<id>/books` | GET | Книги конкретного пользователя |
| `/books/add` | GET/POST | Добавление новой книги |
| `/books/<id>/view` | GET | Просмотр книги |
| `/books/<id>/edit` | GET/POST | Редактирование книги |
| `/books/<id>/delete` | POST | Удаление книги |
| `/books/<id>/status` | POST | Обновление статуса |
| `/profile/edit` | GET/POST | Редактирование профиля |

---

## 4. Маршрутизация во Flask

### 4.1 Декоратор `@app.route`

```python
@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    # book_id автоматически извлекается из URL
```

### 4.2 Особенности реализации
- **Динамические URL**: использование переменных в роутах (`<int:user_id>`)
- **Разделение методов**: разные обработчики для GET и POST
- **URL generation**: `url_for()` для генерации ссылок
- **Обработка ошибок**: `@app.errorhandler(404, 403, 500)`

### 4.3 Пример сложного роута

```python
@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    # Проверка авторизации
    if "user_id" not in session:
        flash("Сначала войдите", "warning")
        return redirect(url_for("login"))

    # Получение книги с обработкой 404
    book = Book.query.get_or_404(book_id)

    # Проверка прав доступа
    if book.user_id != session["user_id"]:
        flash("Это не ваша книга", "danger")
        return redirect(url_for("view_book", book_id=book_id))

    # Обработка формы
    if request.method == "POST":
        # Обновление данных
        # ...

    return render_template("books/edit.html", book=book, current_user=get_current_user())
```

---

## 5. Работа с базой данных

### 5.1 SQLAlchemy ORM

**Настройка подключения**:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DB_DIR, 'catalog.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
```

### 5.2 CRUD операции

**Create** (создание):
```python
user = User(username=username)
user.password_hash = generate_password_hash(password)
db.session.add(user)
db.session.commit()
```

**Read** (чтение):
```python
# Получить все записи
users = User.query.all()

# Фильтрация
user = User.query.filter_by(username=username).first()

# Получить с обработкой 404
book = Book.query.get_or_404(book_id)
```

**Update** (обновление):
```python
book.title = request.form.get("title")
db.session.commit()
```

**Delete** (удаление):
```python
db.session.delete(book)
db.session.commit()
```

### 5.3 Связи между таблицами

```python
# В модели User
books = db.relationship(
    "Book",
    backref="user",
    lazy=True,
    cascade="all, delete-orphan"
)

# В модели Book
user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
```

### 5.4 Инициализация БД

```python
with app.app_context():
    db.create_all()
```

---

## 6. Работа с шаблонами (Jinja2)

### 6.1 Наследование

**Базовый шаблон** (`base.html`):
```html
{% block title %}{% endblock %}
{% block extra_css %}{% endblock %}
{% block content %}{% endblock %}
{% block extra_js %}{% endblock %}
```

**Дочерний шаблон**:
```html
{% extends "base.html" %}

{% block title %}Мои книги{% endblock %}

{% block content %}
    <h1>Список книг</h1>
{% endblock %}
```

### 6.2 Передача данных из контроллера

```python
return render_template("books/view.html",
                     book=book,
                     current_user=get_current_user())
```

### 6.3 Использование в шаблоне

```html
<h1>{{ book.title }}</h1>
<p>Автор: {{ book.author }}</p>

{% if current_user.is_authentificated %}
    <button>Редактировать</button>
{% endif %}
```

### 6.4 Flash-сообщения

```python
# В контроллере
flash("Книга добавлена", "success")

# В шаблоне
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}
```

---

## 7. Распределение ответственности

### 7.1 Команда "The Mandela Catalogue" (группа P3121)

| Роль | Ответственность | Компоненты |
|------|-----------------|------------|
| **Backend-разработчик** | Серверная логика, API, БД | `app.py`, `models.py` |
| **Frontend-разработчик** | Пользовательский интерфейс | `frontend/templates/`, стили |
| **DevOps/Git-мастер** | Ветвление, слияние, деплой | `.gitignore`, README, git flow |

### 7.2 Особенности командной работы
1. Разделение по веткам: `backend`, `frontend`, `mvc`
2. Использование Merge Request для код-ревью
3. Единый coding style (PEP 8 для Python)
4. Комментирование сложных участков кода

---

## 8. Вызовы и сложности

### 8.1 Технические сложности

| Проблема | Решение |
|----------|---------|
| **Ошибки Jinja2 тегов** | Удаление неподдерживаемых тегов (`{% now %}`) |
| **Конфликты при слиянии** | Использование `git merge` с разрешением конфликтов |
| **Пути к файлам** | Использование `os.path.join()` для кроссплатформенности |
| **Безопасность паролей** | Хеширование через `werkzeug.security` |
| **Сессии** | Использование Flask `session` с SECRET_KEY |

### 8.2 Архитектурные сложности

1. **Разделение MVC в одном файле**:
   - Контроллер (`app.py`) содержит много логики
   - Потенциально требует рефакторинга на модули

2. **Дублирование кода**:
   - Проверка авторизации повторяется
   - Решение: создать декоратор `@login_required`

3. **Валидация форм**:
   - Ручная проверка полей
   - Решение: использовать Flask-WTF

### 8.3 Организационные сложности

1. **Координация между ветками**:
   - Запоздалое слияние изменений
   - Конфликты при merge

2. **Поддержка документации**:
   - Отставание документации от кода
   - Решение: обязательное обновление README при коммите

---

## 9. Особенности проекта

### 9.1 Безопасность
- Хеширование паролей (не хранение в открытом виде)
- Проверка прав доступа к книгам
- Защита от CSRF (potential improvement)

### 9.2 UX-решения
- Flash-сообщения для обратной связи
- Адаптивный дизайн (Bootstrap 5)
- Статусы чтения с цветовой индикацией

### 9.3 Архитектурные решения
- Отделение шаблонов от логики
- Использование ORM вместо чистого SQL
- Централизованная обработка ошибок

---

- Добавить комментарии к книгам
- Рейтинги и рекомендации
