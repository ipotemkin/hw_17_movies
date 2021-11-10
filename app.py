# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from app import app


if __name__ == '__main__':
    app.run(debug=True)
