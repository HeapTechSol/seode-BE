import bcrypt
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

from seode.models.config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(120), nullable=False)
    firstName = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    isVerified = db.Column(db.Boolean(), nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, firstName, lastName, email, password, isVerified=False):
        self.email = email
        self.lastName = lastName
        self.firstName = firstName
        self.set_password(password)
        self.isVerified = isVerified

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
      
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

