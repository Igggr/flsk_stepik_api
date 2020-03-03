from flask import Flask
import os
from app.models import db, Event, Participant, Enrollment, Location
from app.admin import admin


def create_app(config_obj=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config.from_object(config_obj)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    admin.init_app(app)


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from app.views import api_blueprint
    app.register_blueprint(api_blueprint)


if __name__ == "__main__":
    app = create_app(config_obj='app.config.DebugConfig')
    app.run()
