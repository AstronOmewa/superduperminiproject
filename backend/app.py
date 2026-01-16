from flask import Flask
from flask import render_template
import os

# Создаем абсолютный путь к папке с шаблонами
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "frontend", "templates")

app = Flask(__name__, template_folder = TEMPLATE_DIR)

@app.route("/login")
def login():
    current_user = {"is_authentificated" : True, "username" : "User0"}
    
    return render_template("login.html", current_user = current_user, )

@app.route("/index")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run()