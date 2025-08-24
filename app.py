from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "instance/users.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------
# User Model
# -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Extra fields
    full_name = db.Column(db.String(150))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))

    rating = db.Column(db.Float, default=0.0)
    balance = db.Column(db.Float, default=0.0)

    # Admin flag
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"

# -------------------
# Routes
# -------------------

# Welcome Page
@app.route("/")
def welcome():
    return render_template("welcome.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("register"))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["is_admin"] = user.is_admin
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

# Dashboard (User)
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user)

# Admin Login
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        code = request.form["admin_code"]
        if code == "200820080":  # Your admin passcode
            session["is_admin"] = True
            flash("Welcome Admin!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin code", "danger")
    return render_template("admin_login.html")

# Admin Dashboard
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        flash("Unauthorized access!", "danger")
        return redirect(url_for("welcome"))
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("welcome"))

# -------------------
# Run app
# -------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
