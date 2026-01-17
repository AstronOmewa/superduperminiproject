from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Book
import os

# Создаем абсолютный путь к папке с шаблонами
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "frontend", "templates")
DB_DIR = os.path.join(BASE_DIR, "..", "database")

# Создаем папку для базы данных
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config["SECRET_KEY"] = "super-secret-key-12345"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DB_DIR, 'catalog.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def get_current_user():
    if "user_id" in session:
        return {"is_authentificated": True, "id": session["user_id"], "username": session["username"]}
    return {"is_authentificated": False}

@app.route("/")
def index():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "book_count": len(user.books)
        })
    current_user = get_current_user()
    return render_template("index.html", users=users_list, current_user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Добро пожаловать!", "success")
            return redirect(url_for("index"))
        else:
            flash("Неверный логин или пароль", "danger")
    current_user = get_current_user()
    return render_template("login.html", current_user=current_user)

@app.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        if not username or not password:
            flash("Заполните все поля", "warning")
            return render_template("register.html", current_user=get_current_user())
        if password != confirm:
            flash("Пароли не совпадают", "danger")
            return render_template("register.html", current_user=get_current_user())
        if User.query.filter_by(username=username).first():
            flash("Такой пользователь уже есть", "danger")
            return render_template("register.html", current_user=get_current_user())
        user = User(username=username)
        user.password_hash = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        flash("Регистрация успешна! Войдите", "success")
        return redirect(url_for("login"))
    return render_template("register.html", current_user=get_current_user())

@app.route("/users")
def user_list():
    users = User.query.all()
    return render_template("users/user_list.html", users=users, current_user=get_current_user())

@app.route("/users/<int:user_id>")
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/user_profile.html", user=user, current_user=get_current_user())

@app.route("/books")
def book_list():
    books = Book.query.all()
    return render_template("books/user_book_list.html", books=books, current_user=get_current_user(), all_books=True)

@app.route("/my-books")
def my_books():
    if "user_id" not in session:
        flash("Сначала войдите", "warning")
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    books = Book.query.filter_by(user_id=user.id).all()
    return render_template("books/user_book_list.html", books=books, current_user=get_current_user())

@app.route("/users/<int:user_id>/books")
def user_books(user_id):
    user = User.query.get_or_404(user_id)
    books = Book.query.filter_by(user_id=user_id).all()
    return render_template("books/user_book_list.html", books=books, user=user, current_user=get_current_user())

@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if "user_id" not in session:
        flash("Сначала войдите", "warning")
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")
        genre = request.form.get("genre")
        description = request.form.get("description")
        if not title or not author:
            flash("Название и автор обязательны", "warning")
            return render_template("books/add.html", current_user=get_current_user())
        book = Book(
            title=title,
            author=author,
            year=int(year) if year else None,
            genre=genre,
            description=description,
            user_id=session["user_id"],
            status="not_started"
        )
        db.session.add(book)
        db.session.commit()
        flash("Книга добавлена", "success")
        return redirect(url_for("my_books"))
    return render_template("books/add.html", current_user=get_current_user())

@app.route("/books/<int:book_id>/view")
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("books/view.html", book=book, current_user=get_current_user())

@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    if "user_id" not in session:
        flash("Сначала войдите", "warning")
        return redirect(url_for("login"))
    book = Book.query.get_or_404(book_id)
    if book.user_id != session["user_id"]:
        flash("Это не ваша книга", "danger")
        return redirect(url_for("view_book", book_id=book_id))
    if request.method == "POST":
        book.title = request.form.get("title")
        book.author = request.form.get("author")
        book.year = int(request.form.get("year")) if request.form.get("year") else None
        book.genre = request.form.get("genre")
        book.description = request.form.get("description")
        db.session.commit()
        flash("Книга обновлена", "success")
        return redirect(url_for("view_book", book_id=book_id))
    return render_template("books/edit.html", book=book, current_user=get_current_user())

@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    if "user_id" not in session:
        flash("Сначала войдите", "warning")
        return redirect(url_for("login"))
    book = Book.query.get_or_404(book_id)
    if book.user_id != session["user_id"]:
        flash("Это не ваша книга", "danger")
        return redirect(url_for("view_book", book_id=book_id))
    db.session.delete(book)
    db.session.commit()
    flash("Книга удалена", "success")
    return redirect(url_for("my_books"))

@app.route("/books/<int:book_id>/status", methods=["POST"])
def update_status(book_id):
    if "user_id" not in session:
        flash("Сначала войдите", "warning")
        return redirect(url_for("login"))
    book = Book.query.get_or_404(book_id)
    if book.user_id != session["user_id"]:
        flash("Это не ваша книга", "danger")
        return redirect(url_for("view_book", book_id=book_id))
    status = request.form.get("status")
    if status in ["not_started", "reading", "finished"]:
        book.status = status
        db.session.commit()
        flash("Статус обновлен", "success")
    return redirect(url_for("view_book", book_id=book_id))

@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        flash("Сначала войдите", "warning")
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    if request.method == "POST":
        new_username = request.form.get("username")
        if new_username != user.username:
            if User.query.filter_by(username=new_username).first():
                flash("Такое имя уже занято", "danger")
                return render_template("edit_profile.html", user=user, current_user=get_current_user())
        user.username = new_username
        db.session.commit()
        session["username"] = new_username
        flash("Профиль обновлен", "success")
        return redirect(url_for("user_profile", user_id=user.id))
    return render_template("edit_profile.html", user=user, current_user=get_current_user())


for number in [404, 403, 500]:
    @app.errorhandler(number)
    def page_not_found(e):
        return render_template('error.html', error_code=number), number

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)