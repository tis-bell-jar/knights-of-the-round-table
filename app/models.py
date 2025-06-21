# app/models.py

from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    notes    = db.relationship('Note', backref='owner', lazy=True)

class Unit(db.Model):
    __tablename__ = 'unit'
    id    = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    notes = db.relationship('Note', backref='unit', lazy=True)

class Note(db.Model):
    __tablename__ = 'note'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'),   nullable=False)
    unit_id    = db.Column(db.Integer, db.ForeignKey('unit.id'),   nullable=False)
    content    = db.Column(db.Text,    nullable=False, default='')
    bg_color   = db.Column(db.String(7), default='#fffb85')
    x          = db.Column(db.Integer, default=50)
    y          = db.Column(db.Integer, default=50)
    width      = db.Column(db.Integer, default=200)
    height     = db.Column(db.Integer, default=200)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow )
    is_flashcard = db.Column(db.Boolean, default=False)
    front_content = db.Column(db.Text, nullable=True)
    back_content = db.Column(db.Text, nullable=True)
