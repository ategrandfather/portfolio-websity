from main import app, db
from main import About, Status

with app.app_context():
    if not About.query.get("main"):
        about = About(id="main", content="Write your about text here")
        db.session.add(about)

    if not Status.query.get("main"):
        status = Status(id="main", message="Write your status message here")
        db.session.add(status)

    db.session.commit()

print("About and Status entries created!")
