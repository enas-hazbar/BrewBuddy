from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # SQLite file in project root: brewbuddy.db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///brewbuddy.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Home route
    @app.route("/")
    def home():
        return render_template("home.html")
    return app

# allow: python app.py to run the dev server
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
