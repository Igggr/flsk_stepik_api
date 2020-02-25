from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = 'events'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    _type = db.Column(db.String)
    _category = db.Column(db.String)
    address = db.Column(db.String)
    seats = db.Column(db.Integer)

    location_id = db.Column(db.Integer, db.ForeignKey("locations.uid"))

    location = db.relationship("Location", back_populates='events')
    enrollments = db.relationship("Enrollment", back_populates='event')


class Participant(db.Model):
    __tablename__ = 'participants'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    _password = db.Column(db.String)
    picture = db.Column(db.String)
    location = db.Column(db.String)
    about = db.Column(db.String)

    enrollments = db.relationship("Enrollment", back_populates='participants')


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    uid = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)

    participant_id = db.Column(db.Integer, db.ForeignKey('participants.uid'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.uid'))

    participant = db.relationship(Participant, back_populates="enrollments")
    event = db.relationship(Event, back_populates="enrollments")


class Location(db.Model):
    __tablename__ = 'locations'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    code = db.Column(db.String)

    events = db.relationship(Event, back_populates='location')
