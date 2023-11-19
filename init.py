from server import db, app
from server.models.user import User

if __name__ == "__main__":
    with app.app_context():
        print("creating database...")
        db.create_all()
        db.session.add(User(username="admin", email="admin@my.com"))
        db.session.commit()
        