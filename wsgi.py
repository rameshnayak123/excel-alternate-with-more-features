from app import app
from models import db
from routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.secret_key = 'my-secret-key'  # Change this to your own secret key
    app.config['SESSION_TYPE'] = 'filesystem'  # Change this to your desired session type

    # Start the Gunicorn server
    # You can customize the number of worker processes, the bind address, and other settings here
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '0.0.0.0:8000',
                'workers': 2
            }

        def load(self):
            return app

    application = FlaskApplication()
    application.run()
