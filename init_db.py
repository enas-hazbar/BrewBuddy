from app import create_app, db
import models  # registers models with SQLAlchemy

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Database created: brewbuddy.db")
