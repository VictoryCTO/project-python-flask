from .user_routes import user_bp
from .roles_routes import role_bp

# Import any other blueprints you may have


def register_blueprints(app):
    """Function to register all blueprints."""
    app.register_blueprint(user_bp)  # Register user routes
    app.register_blueprint(role_bp)  # Register role routes
    # Add other blueprints here if needed
