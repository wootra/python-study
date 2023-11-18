from server import db, app

if __name__ == "__main__":
    with app.app_context():
        print("creating database...")
        db.create_all()
