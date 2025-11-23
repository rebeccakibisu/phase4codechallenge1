from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import event

db = SQLAlchemy()


class Camper(db.Model):
    __tablename__ = "campers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Camper has many Signups (and many Activities through Signups)
    signups = db.relationship(
        "Signup",
        back_populates="camper",
        cascade="all, delete-orphan",
    )

    @validates("name")
    def validate_name(self, key, value):
        """
        Name is required.

        For the tests, we allow the object to be constructed but return None
        for invalid values so that the NOT NULL constraint fails on commit,
        not at assignment time.
        """
        if value is None or not str(value).strip():
            return None
        return str(value).strip()

    @validates("age")
    def validate_age(self, key, value):
        """
        Age must be an integer between 8 and 18 (inclusive).

        For invalid values, we return None so that the NOT NULL constraint
        fails on commit, which is what the tests expect.
        """
        try:
            value = int(value)
        except Exception:
            return None

        if value < 8 or value > 18:
            return None

        return value

    def to_dict_basic(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
        }

    def to_dict_with_signups(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "signups": [s.to_dict_with_activity() for s in self.signups],
        }


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    # Activity has many Signups (and many Campers through Signups)
    signups = db.relationship(
        "Signup",
        back_populates="activity",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "difficulty": self.difficulty,
        }


class Signup(db.Model):
    __tablename__ = "signups"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)  # 0–23 inclusive

    camper_id = db.Column(
        db.Integer,
        db.ForeignKey("campers.id"),
        nullable=False,
    )
    activity_id = db.Column(
        db.Integer,
        db.ForeignKey("activities.id"),
        nullable=False,
    )

    camper = db.relationship("Camper", back_populates="signups")
    activity = db.relationship("Activity", back_populates="signups")

    @validates("time")
    def validate_time(self, key, value):
        """
        time must be an integer between 0 and 23.

        For invalid values, we return None so that the NOT NULL constraint
        fails on commit (tests expect the error to surface at commit time).
        """
        try:
            value = int(value)
        except Exception:
            return None

        if value < 0 or value > 23:
            return None

        return value

    def to_dict_basic(self):
        return {
            "id": self.id,
            "camper_id": self.camper_id,
            "activity_id": self.activity_id,
            "time": self.time,
        }

    def to_dict_with_activity(self):
        """
        Used when nesting signups under a camper, with the activity embedded.
        """
        return {
            "id": self.id,
            "camper_id": self.camper_id,
            "activity_id": self.activity_id,
            "time": self.time,
            "activity": self.activity.to_dict() if self.activity else None,
        }

    def to_dict_full(self):
        """
        Used for POST /signups response: includes both camper and activity.
        """
        return {
            "id": self.id,
            "camper_id": self.camper_id,
            "activity_id": self.activity_id,
            "time": self.time,
            "activity": self.activity.to_dict() if self.activity else None,
            "camper": self.camper.to_dict_basic() if self.camper else None,
        }


# -------------------------------------------------------------------
# Ensure cascade delete of Signups when an Activity is deleted
# -------------------------------------------------------------------
@event.listens_for(Activity, "before_delete")
def delete_signups_for_activity(mapper, connection, target):
    """
    When an Activity is deleted, delete its related Signups via the ORM
    so that the session state is updated and Signup.query.count() reflects
    the deletion immediately (as required by the tests).
    """
    db.session.query(Signup).filter_by(activity_id=target.id).delete()
