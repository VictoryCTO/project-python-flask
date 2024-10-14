import os
from app.config import DevelopmentConfig, ProductionConfig
from app import create_app, db

config_class = (
    DevelopmentConfig if os.getenv("FLASK_ENV") == "development" else ProductionConfig
)
app = create_app(config_class=config_class)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
