from app import app
from models import db, Camper, Activity, Signup

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create Campers
    alice = Camper(name="Alice", age=10)
    bob = Camper(name="Bob", age=12)

    # Create Activities
    hiking = Activity(name="Hiking", difficulty=2)
    archery = Activity(name="Archery", difficulty=3)

    db.session.add_all([alice, bob, hiking, archery])
    db.session.commit()

    # Create Signups
    s1 = Signup(time=10, camper=alice, activity=hiking)
    s2 = Signup(time=11, camper=bob, activity=archery)

    db.session.add_all([s1, s2])
    db.session.commit()
