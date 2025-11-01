from main import app, db
from main import About, Status

with app.app_context():
    if not About.query.get("main"):
        about = About(id="main", content="Imma default change me lol")
        db.session.add(about)

    if not Status.query.get("main"):
        status = Status(id="main", message="Imma default change me")
        db.session.add(status)

    db.session.commit()

print("About and Status entries created!")
