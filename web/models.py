from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    User Model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    userTypeId = db.Column(db.Integer, db.ForeignKey("userType.id"))
    fullname = db.Column(db.String(100), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    user_type = db.relationship("UserType", lazy=True, foreign_keys=[userTypeId])

    def __repr__(self):
        return "<User %r>" % self.email


class UserType(db.Model):
    """
    User Type Model
    """
    __tablename__ = "userType"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum("Admin", "Staff", "Client"), nullable=False, default="Staff")

    def __repr__(self):
        return "<User type %r>" % self.name


class ProductArea(db.Model):
    """
    Product Area Model
    """
    __tablename__ = "productArea"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum("Policies", "Billing", "Claims", "Reports"), nullable=False, default="Policies")

    def __repr__(self):
        return "<Product area %r>" % self.name


class FeatureRequest(db.Model):
    """
    Feature Request Model
    """
    __tablename__ = "featureRequest"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    clientId = db.Column(db.Integer, db.ForeignKey("user.id"))
    priority = db.Column(db.Integer, nullable=False)
    targetDate = db.Column(db.DateTime, nullable=False)
    productAreaId = db.Column(db.Integer, db.ForeignKey("productArea.id"))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    createdBy = db.Column(db.Integer, db.ForeignKey("user.id"))

    client = db.relationship("User", lazy=True, foreign_keys=[clientId])
    product_area = db.relationship("ProductArea", lazy=True, foreign_keys=[productAreaId])
    staff = db.relationship("User", lazy=True, foreign_keys=[createdBy])

    def __repr__(self):
        return "<Feature %r>" % self.title
