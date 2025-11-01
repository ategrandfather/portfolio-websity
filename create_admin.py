from models import Admin, db
from main import app
import getpass

with app.app_context():
    existing = Admin.query.first()
    if existing:
        print(f"An admin already exists (username: {existing.username}). Exiting.")
    else:
        username = input("Enter admin username: ").strip()
        if not username:
            print("Username cannot be empty.")
            raise SystemExit(1)

        password = getpass.getpass("Enter password:")
        confirm_pass = getpass.getpass("Confirm password: ")
        if password != confirm_pass:
            print("Passwords do not match. Exiting.")
            raise SystemExit(1)

        admin = Admin(username=username, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.sesion.commit()
        print(f"Admin user added: {username}")
