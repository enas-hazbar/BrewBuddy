from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Drink, Consumption, ShoppingList, Expense  # import db from models


def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///brewbuddy.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # Attach the app to SQLAlchemy

    # Import models here, AFTER db.init_app
    from models import User, Drink, Consumption, ShoppingList, Expense

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/register", methods=["POST"])
    def register():
        username = request.form.get("username")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")

        if not username or not password:
            flash("Username and password required")
            return redirect(url_for("home"))

        if password != repeat_password:
            flash("Passwords do not match")
            return redirect(url_for("home"))

        hashed_password = generate_password_hash(password)
        new_user = User(user_name=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("User registered successfully!")
        return redirect(url_for("home"))

    @app.route("/login", methods=["POST"])
    def login():
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(user_name=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.user_name
            return redirect(url_for("dashboard"))
        flash("Invalid username or password")
        return redirect(url_for("home"))

    @app.route("/dashboard")
    def dashboard():
        if "user_id" not in session:
            flash("Please log in first")
            return redirect(url_for("home"))
        username = session["username"]
        return render_template("dashboard.html", username=username)


    @app.route("/favourites")
    def favourites():
        if "user_id" not in session:
            flash("Please log in first")
            return redirect(url_for("home"))
        username = session["username"]
        return render_template("favourites.html", username=username)

    @app.route("/basket")
    def basket():
        if "user_id" not in session:
            flash("Please log in first")
            return redirect(url_for("home"))
        username = session["username"]
        return render_template("basket.html", username=username)

    @app.route("/profile")
    def profile():
        if "user_id" not in session:
            flash("Please log in first")
            return redirect(url_for("home"))
        username = session["username"]
        return render_template("profile.html", username=username)

    # -----------------------------------------

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out successfully")
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
