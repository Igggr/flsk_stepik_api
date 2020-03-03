from flask_migrate import Migrate
from app import create_app
from app.models import db, Event, Participant, Location, Enrollment

app = create_app(config_obj='app.config.DebugConfig')
migrate = Migrate(app, db)


@app.shell_context_processor
def shell():
    return {'db': db, 'Event': Event, 'Participant': Participant,
            'Enrollment': Enrollment, 'Location': Location}


if __name__ == '__main__':
    app.run()
