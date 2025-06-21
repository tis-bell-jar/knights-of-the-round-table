# seed_unit.py

from run import app
from app import db
from app.models import Unit

def seed():
    with app.app_context():
        # Ensure tables exist
        db.create_all()

        # Create Unit #1 if it doesn’t exist
        if not Unit.query.get(1):
            unit = Unit(id=1, title="Sample Unit")
            db.session.add(unit)
            db.session.commit()
            print("Created Unit #1")
        else:
            print("Unit #1 already exists")

if __name__ == '__main__':
    seed()
