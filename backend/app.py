from flask import Flask
from flask import render_template, request, redirect, url_for
from hashlib import sha256
import os

# Создаем абсолютный путь к папке с шаблонами
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "frontend", "templates")

app = Flask(__name__, template_folder = TEMPLATE_DIR)

@app.route("/login")
def login():
    current_user = {"is_authentificated" : True, "username" : "User0"}
    
    return render_template("login.html", current_user = current_user, )

@app.route("/")
def index():
    current_user = {"is_authentificated" : True, "username" : "User0"}
    
    return render_template("index.html", current_user = current_user)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = current_user = {"is_authentificated" : True, "username" : username, "email" : email, "password" : sha256(b'{password}').decode() }
        return redirect(url_for("index", current_user = current_user))
    else:   
        current_user = {"is_authentificated" : True, "username" : "User0"}
        return render_template("register.html", current_user = current_user)


for number in [404, 403]:
    @ app.errorhandler(number)  
    def page_not_found(e):  
        return render_template('error.html', error_code = number), number  

if __name__=="__main__":
    app.run()