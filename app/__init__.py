from flask import Flask
from flask_migrate import Migrate
import os
from app.models import db, Event, Participant, Enrollment, Location


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db.init_app(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def shell():
    return {'db': db, 'Event': Event, 'Participant': Participant,
            'Enrollment': Enrollment, 'Location': Location}


from app.views import *

if __name__ == "__main__":
    app.run()
