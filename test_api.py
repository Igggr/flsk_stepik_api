import requests
import pytest
import json
from app import create_app, db, Event, Participant, Location, Enrollment
from app.schema import ParticipantSchema, LocationSchema, EnrollmentSchema, EventSchema


events_schema = EventSchema(many=True)
locations_schema = LocationSchema(many=True)
enrollments_schema = EnrollmentSchema(many=True)
participant_schema = ParticipantSchema()

headers = {'Content-type': 'application/json'}


@pytest.fixture(scope='module', autouse=True)
def test_client():
    flask_app = create_app('app.config.TestConfig')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module', autouse=True)
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    loc1 = Location(title="New-York", code="NY")
    loc2 = Location(title="Los-Angeles", code="LA")
    loc3 = Location(title="San-Fransicko", code="SF")
    loc4 = Location(title="London", code="LO")
    loc5 = Location(title="Berlin", code="BR")
    loc6 = Location(title="Paris", code="PR")
    loc7 = Location(title="Mocsow", code="MSC")
    loc8 = Location(title="Saint-Petersburg", code="SPB")
    loc9 = Location(title="Omsk", code="OMG")
    db.session.add_all([loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc7, loc8, loc9])

    user1 = Participant(name="bob", email="bob@mail.com", location=loc1.code)
    user2 = Participant(name="bil", email="bill@mail.com", location=loc2.code)
    user3 = Participant(name="djon", email="djon@mail.com", location=loc3.code)
    user4 = Participant(name="djek", email="djek@mail.com", location=loc4.code)
    user5 = Participant(name="max", email="max@mail.com", location=loc5.code)
    user6 = Participant(name="elena", email="elena@mail.com", location=loc6.code)
    user7 = Participant(name="olga", email="olga@mail.com", location=loc7.code)
    user8 = Participant(name="ruslan", email="ruslan@mail.com", location=loc8.code)
    user9 = Participant(name="vova", email="vova@mail.com", location=loc9.code)
    users = [user1, user2, user3, user4, user5, user6, user7, user8, user9]
    for user in users:
        user.about = ''
        user.picture = ''
        user.password = '1111'

    evt1 = Event(title="Async or else", description="don't wait for least slow. go in parallel",
                 _type=Event.TypeEnum.LECTURE.value, location=loc1, address="ball street, 34", seats=0,
                 _category=Event.CategoryEnum.PYTHON.value)
    evt2 = Event(title="Monkey testing and it's perspective", description="why you want reliable test?",
                 _type=Event.TypeEnum.LECTURE.value, location=loc2, address="bay of bug, 41", seats=134,
                 _category=Event.CategoryEnum.PROJECT_MANAGMENT.value)
    evt3 = Event(title="Making a word a better place throuth a inspiring speeches", description="don't wait for least slow. go in parallel",
                 _type=Event.TypeEnum.INSPIRING_BULLSHIT.value, location=loc3, address="ball street, 34", seats=28,
                 _category=Event.CategoryEnum.PROJECT_MANAGMENT.value)
    evt4 = Event(title="prolog and you", description="have you some basic logic? let's check",
                 _type=Event.TypeEnum.HACKATON.value, location=loc4, address="irvish street, 63", seats=12,
                 _category=Event.CategoryEnum.ESOLANG.value)

    enr1 = Enrollment(event=evt1, participant=user3)
    enr2 = Enrollment(event=evt1, participant=user3)
    enr3 = Enrollment(event=evt2, participant=user3)
    enr4 = Enrollment(event=evt2, participant=user1)
    enr5 = Enrollment(event=evt4, participant=user6)
    enr6 = Enrollment(event=evt3, participant=user2)


    db.session.add_all([evt1, evt2, evt3, evt4])
    db.session.add_all(users)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    Enrollment.query.delete()
    Event.query.delete()
    Participant.query.delete()
    Location.query.delete()
    db.session.commit()

    #db.drop_all()  # зависнет


def test_locations():
    response = requests.get('http://localhost:5000/locations/')
    assert response.status_code == 200
    resp = response.json()
    assert locations_schema.validate(resp)
    assert len(resp) == 9


def test_events():
    response = requests.get('http://localhost:5000/events/')
    assert response.status_code == 200
    resp = response.json()
    assert events_schema.validate(resp)


def test_non_existing_profile():
    response = requests.get('http://localhost:5000/profile/999999999999999')
    assert response.status_code == 400
    resp = response.json()
    assert resp == {}


@pytest.mark.xfail
def test_existing_profile():
    uid = Participant.query.first().uid
    response = requests.get(f'http://localhost:5000/profile/{uid}')
    assert response.status_code == 200
    resp = response.json()
    assert participant_schema.validate(resp)  # how ???????????


def test_can_register_on_event_with_seats():
    participant = Participant.query.first()
    event = Event.query.filter(Event.seats != 0).first()
    email = participant.email
    response = requests.post(f'http://localhost:5000/enrollments/id={event.uid}',
                             data=json.dumps({'email': email}),
                             headers=headers)
    assert response.status_code == 200


def test_cant_register_on_event_without_seats():
    participant = Participant.query.first()
    event = Event.query.filter(Event.seats == 0).first()
    response = requests.post(f'http://localhost:5000/enrollments/id={event.uid}',
                             data=json.dumps({'email': "bob"}),
                             headers=headers)
    assert response.status_code == 400


def test_can_delete_existing_enrollment():
    enrollment = Enrollment.query.first()
    event_id = enrollment.event_id
    email = enrollment.participant.email
    headers = {'Content-type': 'application/json'}
    response = requests.delete(f'http://localhost:5000/enrollments/id={event_id}',
                               data=json.dumps({'email': email}),
                               headers=headers)
    assert response.status_code == 200


def test_cant_delete_nonexistent_enrollments():
    participant = Participant.query.first()
    email = participant.email
    event = Event.query.first()
    event_id = event.uid
    for e in participant.enrollments:
        db.session.delete(e)
    response = requests.delete(f'http://localhost:5000/enrollments/id={event_id}',
                               data=({'email': email}),
                               headers=headers)
    assert response.status_code == 400


@pytest.mark.skip
def test_can_create_nonexisting_user():
    user = Participant(name="Fredi", email='newnew@mail.ru', location='NY', about="")
    user.password = "1111"
    response = requests.post('http://localhost:5000/register/',
                               data=participant_schema.dump(user),
                               headers=headers)
    assert response.status_code == 200


def test_cant_create_existing_user():
    user = Participant(name="bob", email="bob@mail.com", location="NY", about="")
    user.password = "1111"
    response = requests.post('http://localhost:5000/register/',
                               data=participant_schema.dump(user),
                               headers=headers)
    assert response.status_code == 400


def test_cant_create_user_without_data():
    user = Participant()
    response = requests.post('http://localhost:5000/register/',
                               data=participant_schema.dump(user),
                               headers=headers)
    assert response.status_code == 400


def test_can_auth_with_right_data():
    user = Participant.query.first()
    password = '11111'
    user.password = password
    response = requests.post('http://localhost:5000/auth/',
                             data={'email': user.email, 'password': password},
                             headers=headers)
    assert response.status_code == 200


