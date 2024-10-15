import os
from app import create_app, db
from app.config import DevelopmentConfig, ProductionConfig

# Set up the app
config_class = (
    DevelopmentConfig if os.getenv("FLASK_ENV") == "development" else ProductionConfig
)
app = create_app(config_class=config_class)

# Import models after the app is created
from app.models import User, UserActiveStatusChange

if __name__ == "__main__":
    with app.app_context():
        print("Registered tables:")
        for table in db.metadata.tables:
            print(f"- {table}")

        # print("\nAttempting to create tables...")
        # db.create_all()
        # print("Tables created successfully.")

    app.run(debug=True)
