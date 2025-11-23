from flask import Flask, jsonify, request
from flask_migrate import Migrate

from .config import Config
from .models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return jsonify({"message": "Access Camp API"}), 200


@app.route("/campers", methods=["GET", "POST"])
def campers():
    if request.method == "GET":
        campers = Camper.query.all()
        return jsonify([c.to_dict_basic() for c in campers]), 200

    data = request.get_json() or {}
    try:
        camper = Camper(name=data.get("name"), age=data.get("age"))
        db.session.add(camper)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

    return jsonify(camper.to_dict_basic()), 201


@app.route("/campers/<int:id>", methods=["GET", "PATCH"])
def camper_by_id(id):
    camper = Camper.query.get(id)

    if not camper and request.method == "GET":
        return jsonify({"error": "Camper not found"}), 404

    if request.method == "GET":
        return jsonify(camper.to_dict_with_signups()), 200

    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    data = request.get_json() or {}

    if "name" in data:
        camper.name = data["name"]
    if "age" in data:
        camper.age = data["age"]

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

    return jsonify(camper.to_dict_basic()), 202


@app.route("/activities", methods=["GET", "POST"])
def activities():
    if request.method == "GET":
        activities = Activity.query.all()
        return jsonify([a.to_dict() for a in activities]), 200

    data = request.get_json() or {}

    try:
        activity = Activity(name=data.get("name"), difficulty=data.get("difficulty"))
        db.session.add(activity)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

    return jsonify(activity.to_dict()), 201


@app.route("/activities/<int:id>", methods=["DELETE"])
def activity_by_id(id):
    activity = Activity.query.get(id)

    if not activity:
        return jsonify({"error": "Activity not found"}), 404

    db.session.delete(activity)
    db.session.commit()

    return "", 204


@app.route("/signups", methods=["POST"])
def signups():
    data = request.get_json() or {}

    camper = Camper.query.get(data.get("camper_id"))
    activity = Activity.query.get(data.get("activity_id"))

    if not camper or not activity:
        return jsonify({"errors": ["validation errors"]}), 400

    try:
        signup = Signup(
            camper_id=camper.id,
            activity_id=activity.id,
            time=data.get("time"),
        )
        db.session.add(signup)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

    signup = Signup.query.get(signup.id)
    return jsonify(signup.to_dict_full()), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
