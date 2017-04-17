from tasks import db, bcrypt
from sqlalchemy.dialects.postgresql import JSON
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
import datetime



class Result(db.Model):
    __tablename__ = 'Result'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    task_id = db.Column(db.String(500))
    search_name  = db.Column(db.String(500))


class Token(db.Model):
	__tablename__ = 'Token'
	id = db.Column(db.Integer,primary_key=True)
	fb_token = db.Column(db.String(500))

class InstagramResult(db.Model):
	__tablename__ = 'InstagramResult'
	id = db.Column(db.Integer,primary_key=True)
	ig_name = db.Column(db.String(100))
	task_id = db.Column(db.String(100))


class Users(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password, confirmed,
                 paid=False, admin=False, confirmed_on=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
