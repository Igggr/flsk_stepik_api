from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from wtforms import StringField
from .models import db, Event, Participant, Enrollment, Location

admin = Admin()


class EventView(ModelView):
    column_list = ('location', 'title', 'description', 'date', 'time', 'type', 'category', 'address', 'seats')




admin.add_view(ModelView(Participant, db.session))
admin.add_view(EventView(Event, db.session))
admin.add_view(ModelView(Enrollment, db.session))
admin.add_view(ModelView(Location, db.session))

