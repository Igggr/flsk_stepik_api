from flask import jsonify, request
from flask.views import MethodView
from app import app
from .models import Location, Event, Participant
from .schema import event_schema, location_schema, participant_schema


@app.route('/locations/')
def locations():
    return jsonify(location_schema.dump(Location.query))


@app.route('/events/')
def events():
    eventtype = request.values.get('eventtype')
    location = request.values.get('location')
    events = Event.query
    if eventtype:
        events = events.filter_by(type=Event.TypeEnum(eventtype))
    if location:
        events = events.filter(Event.location.has(code=location))
    return jsonify(event_schema.dump(events))


class EnrollmentView(MethodView):
    methods = ["POST", "DELETE"]

    def post(self, eventid):
         return jsonify({"status": "success"})

    def delete(self, eventid):
         return jsonify({"status": "success"})


app.add_url_rule('/enrollments/id=<int:eventid>', view_func=EnrollmentView.as_view('enrollments'))


@app.route('/register/', methods=['POST'])
def register():
    name = request.json['name']
    email = request.json['email']
    location = request.json['location']
    about = request.json['about']
    password = request.json['password']
    if not name or not email or not location or not about or not password:
        return jsonify({"status": "error"})
    if Participant.query.filter_by(email=email).first():
        return jsonify({"status": "error"})
    participant = Participant(name=name, email=email, location=location, about=about)
    participant.password = password
    participant.save()

    return jsonify(participant_schema.dump(participant))


@app.route('/auth/')
def auth():
    return jsonify({"status": "success", "key": 111111111})


@app.route('/profile/')
def profile():
    return jsonify({"id": 1, "picture": "", "city": "nsk", "about": "", "enrollments": []})
