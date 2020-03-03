from flask import Blueprint
from flask import jsonify, request
from flask.views import MethodView
#from app import db
from .models import Location, Event, Participant, Enrollment, db
from .schema import EventSchema, LocationSchema, ParticipantSchema


api_blueprint = Blueprint('api_blueprint', __name__)

locations_schema = LocationSchema(many=True)
events_schema = EventSchema(many=True)
participant_schema = ParticipantSchema()

@api_blueprint.route('/locations/')
def locations():
    return jsonify(locations_schema.dump(Location.query)), 200


@api_blueprint.route('/events/')
def events():
    eventtype = request.values.get('eventtype')
    location = request.values.get('location')
    events = Event.query
    if eventtype and hasattr(Event.TypeEnum, eventtype.upper()):
        requested_type = getattr(Event.TypeEnum, eventtype.upper())
        events = events.filter(Event._type==requested_type.value)
    if location:
        events = events.filter(Event.location.has(code=location))
    return jsonify(events_schema.dump(events)), 200


class EnrollmentView(MethodView):
    """task was ambigious. It id impossible to deletee enrollments if we know only event.
    We must also know user - for which we delete enrollments.
    I assume, that his email is given in the body of post request"""
    
    methods = ["POST", "DELETE"]

    @staticmethod
    def post(eventid):
        event = Event.query.get(eventid)
        email = request.json.get('email')
        participant = Participant.query.filter_by(email=email)
        if event and participant and event.seats:
            enrollment = Enrollment(event_id=eventid, participant=participant.first())
            event.seats -= 1
            enrollment.save()
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 400

    @staticmethod
    def delete(eventid):
        event = Event.query.get(eventid)
        email = request.json.get('email')
        participant = Participant.query.filter_by(email=email).first()
        if not participant:
            return jsonify({"status": "error"}), 400
        enrollment = [e for e in participant.enrollments if e.event_id == eventid][0]
        db.session.delete(enrollment)
        event.seats += 1
        db.session.commit()
        return jsonify({"status": "success"}), 200


api_blueprint.add_url_rule('/enrollments/id=<int:eventid>', view_func=EnrollmentView.as_view('enrollments'))


@api_blueprint.route('/register/', methods=['POST'])
def register():
    name = request.json['name']
    email = request.json['email']
    location = request.json['location']
    about = request.json['about']
    password = request.json['password']
    if not name or not email or not location or not about or not password:
        print("need more bytes")
        return jsonify({"status": "error"}), 400
    if Participant.query.filter_by(email=email).first():
        print("exist")
        return jsonify({"status": "error"}), 400
    participant = Participant(name=name, email=email, location=location, about=about)
    participant.password = password
    participant.save()

    return jsonify(participant_schema.dump(participant)), 200


@api_blueprint.route('/auth/', methods=["POST"])
def auth():
    print(request.get_json())
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        print("недостаточно данных")
        return jsonify(), 400
    user = Participant.query.filter_by(email=email).first()
    if not user:
        print('not exist')
        return jsonify(), 400
    if user.check_password(password):
        return jsonify(participant_schema.dump(user)), 200
    print("wrong password")
    return jsonify(), 400


@api_blueprint.route('/profile/<int:uid>')
def profile(uid):
    user = Participant.query.get(uid)
    if not user:
        return jsonify(), 400
    return jsonify(participant_schema.dump(user))
