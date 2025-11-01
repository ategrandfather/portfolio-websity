from main import app, db
from main import About, Status, ProjectPost
from datetime import datetime, timezone

with app.app_context():
    # Create default About entry
    if not About.query.get("main"):
        about = About(id="main", content="Imma default change me lol")
        db.session.add(about)

    # Create default Status entry
    if not Status.query.get("main"):
        status = Status(id="main", message="Imma default change me")
        db.session.add(status)

    # Create default ProjectPost entry
    if not ProjectPost.query.first():  # check if any project exists
        project = ProjectPost(
            title="Default Project Title",
            link="https://example.com",
            description="This is a default project description",
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(project)

    db.session.commit()

print("About, Status, and ProjectPost entries created!")
