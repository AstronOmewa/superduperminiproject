from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Модель пользователя.

    Атрибуты:
        id (int): первичный ключ
        username (str): уникальное имя пользователя
        password_hash (str): хеш пароля
        books (list[Book]): список книг пользователя
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    books = db.relationship(
        "Book",                    # Имя связанной модели
        backref="user",            # Атрибут для обратной связи
        lazy=True,                 # Ленивое подгружение
        cascade="all, delete-orphan"  # При удалении пользователя удалить книги
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Book(db.Model):
    """Модель книги.

    Атрибуты:
        id (int): первичный ключ
        title (str): название книги
        author (str): автор книги
        year (int): год издания
        genre (str): жанр книги
        description (str): краткое описание книги
        status (str): статус чтения (not_started / reading / finished)
        user_id (int): внешний ключ на пользователя
    """
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    description = db.Column(db.Text)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="not_started"  # Значения: not_started | reading | finished
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),  # Связь с пользователем
        nullable=False
    )

    def __repr__(self):
        return f"<Book {self.title}>"
