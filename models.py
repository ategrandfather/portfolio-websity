"""
Defining different tables of one DB for simplicity sake

project_post - all about projects
about - lil story about me
status - what am i doing currently
admin - admin duh
"""

from typing import override
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class ProjectPost(db.Model):
    __tablename__ = "project_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(150), nullable=False, default="This meant to be a title"
    )
    link = db.Column(db.String(150), nullable=False, default="This meant to be a link")
    description = db.Column(
        db.Text, nullable=False, default="This meant to be a description"
    )
    # timezone aware
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class About(db.Model):
    __tablename__ = "about"
    id = db.Column(db.String(50), primary_key=True, default="main")
    content = db.Column(db.Text, nullable=False, default="Valik update me pls")


class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.String(50), primary_key=True, default="main")
    message = db.Column(db.Text, nullable=False, default="Valik update me pls")


class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @override
    def __repr__(self) -> str:
        return f"<Admin {self.username}>"
