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
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'yoursecretkey'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    bio = db.Column(db.Text, default="")

# Edit Profile Route
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if "user_id" not in session:
        flash("You must be logged in first!", "danger")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        user.username = request.form["username"]
        user.email = request.form["email"]
        user.bio = request.form["bio"]

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("edit_profile.html", user=user)

# Profile page
@app.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'yoursecretkey'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    bio = db.Column(db.Text, default="")

# Edit Profile Route
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if "user_id" not in session:
        flash("You must be logged in first!", "danger")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        user.username = request.form["username"]
        user.email = request.form["email"]
        user.bio = request.form["bio"]

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("edit_profile.html", user=user)

# Profile page
@app.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, default="")

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    user = db.relationship("User", backref="services")
    category = db.relationship("Category", backref="services")

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Text, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    service = db.relationship("Service", backref="reports")
    user = db.relationship("User", backref="reports")@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if "user_id" not in session:
        flash("Login required!", "danger")
        return redirect(url_for("login"))

    categories = Category.query.all()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        category_id = request.form["category"]

        new_service = Service(
            title=title,
            description=description,
            user_id=session["user_id"],
            category_id=category_id
        )
        db.session.add(new_service)
        db.session.commit()
        flash("Service added successfully!", "success")
        return redirect(url_for("browse_services"))

    return render_template("add_service.html", categories=categories)

@app.route('/report/<int:service_id>', methods=['GET', 'POST'])
def report_service(service_id):
    if "user_id" not in session:
        flash("Login required to report!", "danger")
        return redirect(url_for("login"))

    service = Service.query.get_or_404(service_id)

    if request.method == "POST":
        reason = request.form["reason"]
        report = Report(reason=reason, service_id=service.id, user_id=session["user_id"])
        db.session.add(report)
        db.session.commit()
        flash("Report submitted!", "success")
        return redirect(url_for("browse_services"))

    return render_template("report.html", service=service)
@app.route('/services')
def browse_services():
    query = request.args.get("q")
    category_id = request.args.get("category")

    services = Service.query

    if query:
        services = services.filter(Service.title.contains(query) | Service.description.contains(query))
    if category_id:
        services = services.filter_by(category_id=category_id)

    services = services.all()
    categories = Category.query.all()

    return render_template("browse_services.html", services=services, categories=categories)

