from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, Event, Participant, Enrollment, Location

admin = Admin()

admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Participant, db.session))
admin.add_view(ModelView(Enrollment, db.session))
admin.add_view(ModelView(Location, db.session))

