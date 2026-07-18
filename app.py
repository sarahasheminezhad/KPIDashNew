from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from models import db, User

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import check_password_hash


barname_df = pd.read_excel(
    os.path.join(BASE_DIR, "static", "data", "barname.xlsx")
)
df1 = pd.read_excel(
    os.path.join(BASE_DIR, "static", "data", "1405-02.xlsx")
)
df2 = pd.read_excel(
    os.path.join(BASE_DIR, "static", "data", "1405-03.xlsx")
)
df = pd.concat([df1, df2], ignore_index=True)

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key"
)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///" + os.path.join(BASE_DIR, "users.db")

db.init_app(app)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/ranking")
def ranking():
    return jsonify(df.to_dict(orient="records"))

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            if user.role == "admin":
                return redirect(url_for("admin"))

            return redirect(url_for("my_dashboard"))

        return render_template(
            "login.html",
            error="نام کاربری یا رمز عبور اشتباه است."
        )

    return render_template("login.html")




@app.route("/my-dashboard")
@login_required
def my_dashboard():

    my_data = barname_df[
        barname_df["بازاریاب"] == current_user.marketer
    ]

    return render_template(

        "my_dashboard.html",

        user=current_user,

        data=my_data.to_dict(orient="records"),

        total_waybills=len(my_data),

        total_customers=my_data["فرستنده"].nunique(),

        total_weight=my_data["وزن"].sum()

    )
@app.route("/admin")
@login_required
def admin():

    if current_user.role != "admin":
        return "Access Denied", 403

    return render_template(
        "admin.html",
        users=barname_df.to_dict(orient="records")
    )

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")


with app.app_context():
    db.create_all()
if __name__ == "__main__":
    
    app.run(debug=True)
