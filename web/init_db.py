from datetime import datetime, timedelta
from sqlalchemy_utils import create_database, database_exists, drop_database

from app import create_app
from models import db, User, UserType, ProductArea, FeatureRequest


app = create_app()
app.app_context().push()


def create_fresh_db():
    url = app.config["SQLALCHEMY_DATABASE_URI"]

    if database_exists(url):
        drop_database(url)

    create_database(url)
    db.create_all()


def create_dummy_feature_request(client_username):
    title = "Sample title"
    description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sodales efficitur convallis. " \
                  "Fusce blandit turpis non laoreet blandit. Fusce aliquam ipsum eget eros volutpat egestas. " \
                  "Fusce viverra leo id molestie molestie. Morbi sagittis orci sed felis maximus scelerisque. " \
                  "Etiam magna ante, sollicitudin porta euismod sed, porttitor nec felis."
    created_by = User.query.filter_by(username="staff1").first().id
    products = {1: "Billing", 2: "Claims", 3: "Reports"}

    # Create dummy feature requests for Client A
    client_id = User.query.filter_by(username=client_username).first().id

    for i in range(1, 4):
        db.session.add(
            FeatureRequest(
                title=title + " " + str(i),
                description=description,
                clientId=client_id,
                priority=i,
                targetDate=datetime.utcnow() + timedelta(days=10 * i),
                productAreaId=ProductArea.query.filter_by(name=products[i]).first().id,
                createdBy=created_by
            )
        )


def create_dummy_data():
    default_user_type = ["Admin", "Staff", "Client"]
    for user_type in default_user_type:
        db.session.add(UserType(name=user_type))
    db.session.commit()

    # Create product area
    default_product_area = ["Policies", "Billing", "Claims", "Reports"]
    for product_area in default_product_area:
        db.session.add(ProductArea(name=product_area))
    db.session.commit()

    # Create dummy user
    admin = User(username="admin", email="admin@iws.com", userTypeId=get_user_type("Admin"), fullname="Administrator")
    staff = User(username="staff1", email="staff1@iws.com", userTypeId=get_user_type("Staff"), fullname="Staff 1")
    clienta = User(username="clienta", email="client@a.com", userTypeId=get_user_type("Client"), fullname="Client A")
    clientb = User(username="clientb", email="client@b.com", userTypeId=get_user_type("Client"), fullname="Client B")
    clientc = User(username="clientc", email="client@c.com", userTypeId=get_user_type("Client"), fullname="Client C")

    users = [admin, staff, clienta, clientb, clientc]
    for user in users:
        db.session.add(user)
    db.session.commit()

    for client_username in ["clienta", "clientb", "clientc"]:
        create_dummy_feature_request(client_username)
    db.session.commit()


def get_user_type(name):
    return UserType.query.filter_by(name=name).first().id


if __name__ == "__main__":
    create_fresh_db()
    create_dummy_data()
