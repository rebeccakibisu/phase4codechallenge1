import pytest
from server.models import Camper, Activity, Signup

def test_camper_requires_name(app, db):
    with app.app_context():
        camper = Camper(name="", age=10)
        db.session.add(camper)

        with pytest.raises(Exception):
            db.session.commit()
            db.session.rollback()

def test_camper_age_range(app, db):
    with app.app_context():
        camper = Camper(name="John", age=20)
        db.session.add(camper)

        with pytest.raises(Exception):
            db.session.commit()
            db.session.rollback()

def test_signup_time_range(app, db):
    with app.app_context():
        camper = Camper(name="Jane", age=12)
        activity = Activity(name="Swimming", difficulty=3)

        db.session.add_all([camper, activity])
        db.session.commit()

        signup = Signup(camper_id=camper.id, activity_id=activity.id, time=30)
        db.session.add(signup)

        with pytest.raises(Exception):
            db.session.commit()
            db.session.rollback()

def test_activity_cascade_delete(app, db):
    with app.app_context():
        camper = Camper(name="Bob", age=14)
        activity = Activity(name="Hiking", difficulty=2)

        db.session.add_all([camper, activity])
        db.session.commit()

        signup = Signup(camper_id=camper.id, activity_id=activity.id, time=8)
        db.session.add(signup)
        db.session.commit()

        # delete activity
        db.session.delete(activity)
        db.session.commit()

        assert Signup.query.count() == 0
