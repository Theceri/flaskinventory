import secrets
import os

class Base:
    FLASK_APP = os.environ.get("FLASK_APP")
    SQLALCHEMY_TRACKMODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16)

class Development(Base):
    FLASK_ENV= os.environ.get("FLASK_ENV")
    DATABASE = os.environ.get("DATABASE")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    # SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")

class Staging(Base):
    pass

class Production(Base):
    SQLALCHEMY_DATABASE_URI=postgres://epvmspvrysesob:b7a049bb4d4c1f70cf35aa3a1783d9b9e107c929bcb37b5b2688934e513de6c8@ec2-54-74-14-109.eu-west-1.compute.amazonaws.com:5432/dd2gvjikckce4t