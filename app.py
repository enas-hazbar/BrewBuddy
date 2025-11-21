# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Drink, Consumption, ShoppingList, Expense, Favourite

import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv
load_dotenv()


BEERS = [
    {
        "key": "hertog_jan_bock",
        "name": "Hertog Jan",
        "image": "../static/BeerIcons/Bockbier.png",
        "description": "Dark, malty, caramel-forward with low bitterness.",
        "count": 30,
    },
    {
        "key": "duvel",
        "name": "Duvel",
        "image": "../static/BeerIcons/Duvel.png",
        "description": "Strong golden ale, high carbonation, citrus and pepper flavors.",
        "count": 30,
    },
    {
        "key": "hoegaarde",
        "name": "Hoegaarde",
        "image": "../static/BeerIcons/Hoegaarde.png",
        "description": "Wheat beer with coriander and orange peel, hazy and refreshing.",
        "count": 30,
    },
    {
        "key": "lagunitas_ipa",
        "name": "Lagunitas IPA",
        "image": "../static/BeerIcons/IPA.png",
        "description": "Hoppy bitterness, citrus and pinenotes, medium body.",
        "count": 30,
    },
    {
        "key": "la_chouffe",
        "name": "La Chouffe",
        "image": "../static/BeerIcons/La_Chouffe.png",
        "description": "Belgian blond ale with fruity notes and a spicy yeast character.",
        "count": 30,
    },
    {
        "key": "stella_artois",
        "name": "Stella Artois",
        "image": "../static/BeerIcons/Stella_Artois.png",
        "description": "European lager with floral hops and a sharp, clean finish.",
        "count": 30,
    },
    {
        "key": "triple_karmeliet",
        "name": "Triple Karmeliet",
        "image": "../static/BeerIcons/Triple-Karmeliet.png",
        "description": "Belgian tripel with complex grain flavors and fruity yeast profile.",
        "count": 30,
    },
    {
        "key": "weihenstephaner",
        "name": "Weihenstephaner",
        "image": "../static/BeerIcons/Weihenstephaner.png",
        "description": "Classic wheat beer with banana and clove from the yeast.",
        "count": 30,
    },
    {
        "key": "amstel_pilsener",
        "name": "Amstel Pilsener",
        "image": "../static/amstel.png",
        "description": "A simple, smooth pilsner with a tiny bit of bitterness.",
        "count": 30,
    },
    {
        "key": "corona_premier",
        "name": "Corona Premier",
        "image": "../static/Corona-Premier.png",
        "description": "A light and smooth beer that’s super easy to drink.",
        "count": 30,
    },
    {
        "key": "hertog_jan_pils",
        "name": "Hertog Jan",
        "image": "../static/hertog jan.png",
        "description": "A fuller Dutch pilsner with a richer taste than most.",
        "count": 30,
    },
    {
        "key": "bud_light",
        "name": "Bud Light",
        "image": "../static/bud light.png",
        "description": "A very light lager that’s clean and easy to sip.",
        "count": 30,
    },
    {
        "key": "guinness",
        "name": "Guinness",
        "image": "../static/guinness.png",
        "description": "A creamy dark beer with a deep roasted flavour.",
        "count": 30,
    },
    {
        "key": "heineken_0",
        "name": "Heineken",
        "image": "../static/heineken.png",
        "description": "A non-alcoholic option that still tastes fresh and balanced.",
        "count": 30,
    },
    {
        "key": "miller_lite",
        "name": "Miller Lite",
        "image": "../static/miller.png",
        "description": "A crisp, low-calorie lager made for easy drinking.",
        "count": 30,
    },
    {
        "key": "grolsch",
        "name": "Grolsch",
        "image": "../static/grolsh.png",
        "description": "A refreshing pilsner with a clean, slightly hoppy taste.",
        "count": 30,
    },
]


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///brewbuddy.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

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

        user_id = session["user_id"]
        username = session["username"]

        fav_rows = Favourite.query.filter_by(user_id=user_id).all()
        fav_keys = [f.drink_key for f in fav_rows]

        return render_template(
            "dashboard.html",
            username=username,
            beers=BEERS,
            fav_keys=fav_keys,
        )

    @app.route("/favourites")
    def favourites():
        if "user_id" not in session:
            flash("Please log in first")
            return redirect(url_for("home"))

        user_id = session["user_id"]
        username = session["username"]

        fav_rows = Favourite.query.filter_by(user_id=user_id).all()
        fav_keys = {f.drink_key for f in fav_rows}
        fav_beers = [b for b in BEERS if b["key"] in fav_keys]

        return render_template(
            "favourites.html",
            username=username,
            beers=fav_beers,
            fav_keys=list(fav_keys),
        )

    @app.route("/api/favourites/toggle", methods=["POST"])
    def toggle_favourite():
        if "user_id" not in session:
            return jsonify({"error": "unauthorized"}), 401

        user_id = session["user_id"]
        data = request.get_json(silent=True) or {}
        drink_key = data.get("drink_key") or request.form.get("drink_key")

        if not drink_key:
            return jsonify({"error": "missing drink_key"}), 400

        existing = Favourite.query.filter_by(user_id=user_id, drink_key=drink_key).first()

        if existing:
            db.session.delete(existing)
            db.session.commit()
            return jsonify({"favourited": False})
        else:
            new_fav = Favourite(user_id=user_id, drink_key=drink_key)
            db.session.add(new_fav)
            db.session.commit()
            return jsonify({"favourited": True})

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
