from flask import jsonify, request
from flask.views import MethodView
from app import app
from .models import Location, Event
from .schema import event_schema, location_schema


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


@app.route('/register/')
def register():
    return jsonify({"status": "ok", "id": 1})


@app.route('/auth/')
def auth():
    return jsonify({"status": "success", "key": 111111111})


@app.route('/profile/')
def profile():
    return jsonify({"id": 1, "picture": "", "city": "nsk", "about": "", "enrollments": []})
