from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api

db = SQLAlchemy()
ma = Marshmallow()


def create_app() -> Flask:
    """
    Create and configure the Flask application instance.

    This function sets up the Flask app, initializes extensions (SQLAlchemy, Marshmallow),
    and registers the API routes.

    It also configures the app based on the settings from the config module and sets
    up the API with a Swagger UI documentation.

    Returns:
        Flask: The initialized Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    ma.init_app(app)

    api = Api(app, doc="/swagger/")

    from app.view.weather_analytics_view import weather_analytics

    api.add_namespace(weather_analytics, path="/api/weather")

    return app