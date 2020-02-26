from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import enum

db = SQLAlchemy()


class TypeEnum(enum.Enum):
    HACKATON = 1
    MEETUP = 2
    LECTURE = 3


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

    TypeEnum = TypeEnum

    def __str__(self):
        return f"{self.title}"

    @property
    def type(self):
        self._type = type

    @type.setter
    def type(self, type_enum):
        self._type = type_enum


class Participant(db.Model):
    __tablename__ = 'participants'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    _password = db.Column(db.String)
    picture = db.Column(db.String)
    location = db.Column(db.String)
    about = db.Column(db.String)

    enrollments = db.relationship("Enrollment", back_populates='participant')

    def __str__(self):
        return f"{self.name}, {self.email}"

    @property
    def password(self):
        raise ValueError('Не положено знать')

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return check_password_hash(plaintext, self._password)


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

    def __str__(self):
        return f"{self.title}, {self.code}"
