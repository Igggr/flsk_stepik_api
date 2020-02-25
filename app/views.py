from flask import jsonify
from flask.views import MethodView
from app import app


@app.route('/locations/')
def locations():
    return jsonify([])


@app.route('/events/')
def events():
    return jsonify([])


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
