import json
import uuid
from datetime import datetime

import bcrypt
from app import db
from sqlalchemy.dialects.postgresql import UUID

user_child = db.Table(
    'user_child',
    db.Column('user_id', UUID, db.ForeignKey('user_account.id', ondelete="CASCADE"), primary_key=True),
    db.Column('child_id', UUID, db.ForeignKey('child.id', ondelete="CASCADE"), primary_key=True),
    db.Index('ix_user_child_child_id_user_id', 'child_id', 'user_id', unique=True)
)


class User(db.Model):
    __tablename__ = 'user_account'

    # Fields
    id = db.Column(UUID, primary_key=True)
    password = db.Column(db.Binary, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False, unique=True)
    activated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    login_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relationships
    children = db.relationship('Child', secondary=user_child, lazy=False, backref=db.backref('users', lazy=True))
    events = db.relationship('Event', backref='user', lazy=True)

    # Methods
    def __init__(self, password, first_name, last_name, email_address):
        self.id = str(uuid.uuid4())
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email_address = email_address.lower()
        self.created_at = datetime.utcnow()
        self.set_password(password)

    def __repr__(self):
        return json.dumps(self.as_dict(), sort_keys=True, separators=(',', ':'))

    def as_dict(self):
        child_ids = []
        for child in self.children:
            child_ids.append(str(child.id))

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "activated_at": self.activated_at.isoformat() if self.activated_at else self.activated_at,
            "login_at": self.login_at.isoformat() if self.login_at else self.login_at,
            "children": child_ids,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else self.updated_at,
        }

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password)


class Child(db.Model):
    __tablename__ = 'child'

    # Fields
    id = db.Column(UUID, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relationships
    events = db.relationship('Event', backref='child', lazy=True, passive_deletes=True)

    # Methods
    def __init__(self, first_name, last_name, date_of_birth):
        self.id = str(uuid.uuid4())
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.date_of_birth = date_of_birth
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return json.dumps(self.as_dict(), sort_keys=True, separators=(',', ':'))

    def as_dict(self):
        user_ids = []
        for user in self.users:
            user_ids.append(str(user.id))

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat(),
            "users": user_ids,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else self.updated_at,
        }


class Event(db.Model):
    __tablename__ = 'event'
    # Fields
    id = db.Column(UUID, primary_key=True)
    user_id = db.Column(UUID, db.ForeignKey('user_account.id', ondelete="SET NULL"), nullable=True, index=True)
    child_id = db.Column(UUID, db.ForeignKey('child.id', ondelete="CASCADE"), nullable=False, index=True)
    type = db.Column(db.String, nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    ended_at = db.Column(db.DateTime(timezone=True), nullable=True)
    amount = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String, nullable=True)
    side = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Methods
    def __init__(self, user_id, child_id, type, started_at):
        self.id = str(uuid.uuid4())
        self.user_id = str(uuid.UUID(user_id, version=4))
        self.child_id = str(uuid.UUID(child_id, version=4))
        self.type = type
        self.started_at = started_at
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return json.dumps(self.as_dict(), sort_keys=True, separators=(',', ':'))

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "child_id": self.child_id,
            "type": self.type,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else self.ended_at,
            "amount": self.amount,
            "unit": self.unit,
            "side": self.side,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else self.updated_at
        }
