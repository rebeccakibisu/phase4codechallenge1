from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association model — join table
class Signup(db.Model):
    __tablename__ = "signups"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))

    # Relationships back to parent objects
    camper = db.relationship("Camper", back_populates="signups")
    activity = db.relationship("Activity", back_populates="signups")


class Camper(db.Model):
    __tablename__ = "campers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Camper has many Signups
    signups = db.relationship(
        "Signup", back_populates="camper", cascade="all, delete-orphan"
    )

    # Camper has many Activities through Signups
    activities = db.relationship(
        "Activity",
        secondary="signups",
        back_populates="campers",
        viewonly=True,
    )


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    # Activity has many Signups
    signups = db.relationship(
        "Signup",
        back_populates="activity",
        cascade="all, delete-orphan",  # ensures cascade delete
    )

    # Activity has many Campers through Signups
    campers = db.relationship(
        "Camper",
        secondary="signups",
        back_populates="activities",
        viewonly=True,
    )
