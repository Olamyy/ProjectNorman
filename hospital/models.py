# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from Norman.database import db, PasswordField
from Norman.extensions import bcrypt


class Hospital(UserMixin, db.Document):
    name = db.StringField(required=True, max_length=200, min_length=3)
    username = db.StringField(required=True, max_length=50, min_length=10)
    password = PasswordField(required=True, max_length=50, min_length=10)
    email = db.StringField(required=True, max_length=50, min_length=10)
    created_at = db.DateTimeField(default=dt.datetime.now())
    active = db.BoolField(default=False)
    is_admin = db.BoolField(default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Hospital({name!r})>'.format(name=self.name)
