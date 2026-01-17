from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt

from routes.auth import auth_bp
from routes.student import student_bp
from routes.mentor import mentor_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(mentor_bp)

    return app

app = create_app()
