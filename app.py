import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Drink, Consumption, ShoppingList, Expense

import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv
load_dotenv()



def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///brewbuddy.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ---------- GOOGLE OAUTH CONFIG ----------
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")


    # ---------- ROUTES ----------

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

        # check if user already exists
        existing = User.query.filter_by(user_name=username).first()
        if existing:
            flash("This username is already taken")
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

        if not user or not user.password or not check_password_hash(user.password, password):
            flash("Invalid username or password")
            return redirect(url_for("home"))

        session["user_id"] = user.id
        session["username"] = user.user_name
        return redirect(url_for("dashboard"))

    # ---------- GOOGLE LOGIN ROUTES ----------

    @app.route("/login/google")
    def google_login():
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        redirect_uri = url_for("google_callback", _external=True)

        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri],
                }
            },
            scopes=["openid", "email", "profile"],
        )
        flow.redirect_uri = redirect_uri

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )

        session["oauth_state"] = state
        return redirect(authorization_url)

    @app.route("/login/google/callback")
    def google_callback():
        state = session.get("oauth_state")

        redirect_uri = url_for("google_callback", _external=True)

        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri],
                }
            },
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"
            ],
            state=state,
        )

        flow.redirect_uri = redirect_uri

        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials

        id_info = id_token.verify_oauth2_token(
            credentials._id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )

        email = id_info.get("email")
        google_id = id_info.get("sub")
        name = id_info.get("name")

        user = User.query.filter_by(google_id=google_id).first()

        if not user:
            user = User.query.filter_by(user_name=email).first()

        if not user:
            user = User(
                user_name=email,
                password=None,
                google_id=google_id,
            )
            db.session.add(user)
            db.session.commit()
        else:
            if not user.google_id:
                user.google_id = google_id
                db.session.commit()

        session["user_id"] = user.id
        session["username"] = user.user_name

        return redirect(url_for("dashboard"))


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

    

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out successfully")
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
