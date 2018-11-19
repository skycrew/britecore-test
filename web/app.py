import os
from dateutil.parser import parse
from flask import Flask, render_template, redirect, url_for, request, jsonify, send_from_directory
from flask.blueprints import Blueprint
from models import db, User, UserType, ProductArea, FeatureRequest


bp = Blueprint("frapp", __name__)


def create_app(config_name="PRODUCTION"):
    app = Flask(__name__)

    if config_name == "PRODUCTION":
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/frapp"

    if config_name == "TESTING":
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/frapp_testing"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config_name = config_name
    db.init_app(app)
    app.register_blueprint(bp)
    return app


app = create_app("PRODUCTION")


@bp.route("/")
def index():
    """
    Index page
    :return: list of feature requests, list of clients and products (for form)
    """
    all_feature_requests = FeatureRequest.query.join(FeatureRequest.client).\
        order_by(User.fullname, FeatureRequest.targetDate).all()
    all_clients = User.query.filter(User.user_type.has(name="Client")).order_by(User.fullname)
    all_products = ProductArea.query.all()

    return render_template("home.html", **{
        "all_feature_requests": all_feature_requests,
        "all_clients": all_clients,
        "all_products": all_products
    })


@bp.route("/client/<client_name>")
def client_feature_requests(client_name):
    """
    Client page, show feature requests for specific client
    :param client_name: String
    :return: list of feature requests for specific client, list of clients and products (for form) and client name
    """
    if not client_name:
        return redirect(url_for("frapp.index"))

    all_feature_requests = FeatureRequest.query.\
        filter(FeatureRequest.client.has(fullname=client_name)).\
        order_by(FeatureRequest.targetDate)
    all_clients = User.query.filter(User.user_type.has(name="Client")).order_by(User.fullname)
    all_products = ProductArea.query.all()

    return render_template("home.html", **{
        "all_feature_requests": all_feature_requests,
        "all_clients": all_clients,
        "all_products": all_products,
        "client_name": client_name
    })


@bp.route("/add", methods=["POST"])
def add():
    """
    Create feature requests handler
    :return: errors if any otherwise return url
    """
    title = request.form.get("frTitle", None)
    description = request.form.get("frDescription", None)
    client_id = request.form.get("frClient", None)
    priority = request.form.get("frPriority", None)
    target_date = request.form.get("frTargetDate", None)
    product_area_id = request.form.get("frProduct", None)

    errors, priority, target_date = validate_input(title, description, priority, target_date)

    if errors:
        return jsonify(errors=errors)

    if is_duplicate_priority(client_id, priority):
        reorder_priority(priority, client_id)

    fr = FeatureRequest(title=title,
                        description=description,
                        clientId=int(client_id),
                        priority=priority,
                        targetDate=target_date,
                        productAreaId=int(product_area_id),
                        createdBy=User.query.filter_by(username="staff1").first().id)

    db.session.add(fr)
    db.session.commit()

    return jsonify(url=url_for("frapp.index"))


@bp.route("/edit/<int:feature_request_id>", methods=["GET", "POST"])
def edit(feature_request_id):
    """
    Edit feature request handler. Support both GET and POST
    :param feature_request_id: Feature request ID
    :return: Specific feature request (GET), url (POST)
    """
    if request.method == "GET":
        fr = FeatureRequest.query.filter(FeatureRequest.id == feature_request_id).first_or_404()

        return jsonify(
            title=fr.title,
            description=fr.description,
            clientId=fr.client.id,
            priority=fr.priority,
            targetDate=fr.targetDate.strftime("%Y-%m-%d"),
            productId=fr.product_area.id
        )

    if request.method == "POST":
        title = request.form.get("frTitleEdit", None)
        description = request.form.get("frDescriptionEdit", None)
        client_id = request.form.get("frClientEdit", None)
        priority = request.form.get("frPriorityEdit", None)
        target_date = request.form.get("frTargetDateEdit", None)
        product_area_id = request.form.get("frProductEdit", None)

        errors, priority, target_date = validate_input(title, description, priority, target_date)

        if errors:
            return jsonify(errors=errors)

        fr = FeatureRequest.query.filter(FeatureRequest.id == feature_request_id).first()

        if fr.priority != priority and is_duplicate_priority(client_id, priority):
            reorder_priority(priority, client_id)

        if fr.title != title:
            fr.title = title

        if fr.description != description:
            fr.description = description

        if fr.clientId != client_id:
            fr.clientId = client_id

        if fr.priority != priority:
            fr.priority = priority

        if fr.targetDate != target_date:
            fr.targetDate = target_date

        if fr.productAreaId != product_area_id:
            fr.productAreaId = product_area_id

        db.session.commit()

        return jsonify(url=url_for("frapp.index"))


@bp.route("/delete/<int:feature_request_id>")
def delete(feature_request_id):
    """
    Delete feature request handler
    :param feature_request_id: Feature request ID
    :return: Referrer url
    """
    FeatureRequest.query.filter(FeatureRequest.id == feature_request_id).delete()
    db.session.commit()

    return redirect(request.referrer)


@bp.route('/favicon.ico')
def favicon():
    """
    Favicon handler
    :return: Favicon url
    """
    return send_from_directory(
        os.path.join(app.root_path, "static/img"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon")


def validate_input(title, description, priority, target_date):
    """
    Validate feature request form input
    :param title: (String) Feature request title
    :param description: (String) Feature request description
    :param priority: (String) Feature request priority
    :param target_date: (String) Feature request targetDate
    :return: List of errors if any, (int) priority, (DateTime) target_date
    """
    errors = []

    if not title:
        errors.append("Title is empty!")

    if not description:
        errors.append("Description is empty!")

    if not priority:
        errors.append("Priority is empty!")

    try:
        priority = int(priority)
    except ValueError:
        errors.append("Priority is not a number!")

    if not target_date:
        errors.append("Target date is empty!")

    try:
        target_date = parse(target_date)
    except ValueError:
        errors.append("Target date is not correct!")

    return errors, priority, target_date


def is_duplicate_priority(client_id, priority):
    """
    Check priority for specific client
    :param client_id: (String) Client ID
    :param priority: (int) Priority
    :return: True if priority is in the DB, otherwise return False
    """
    fr = FeatureRequest.query.filter(FeatureRequest.clientId == client_id, FeatureRequest.priority == priority).count()
    return True if fr != 0 else False


def reorder_priority(priority, client_id):
    """
    Reorder client priority. If a priority is set on a new feature as "1",
    then all other feature requests for that client should be reordered.
    :param priority: (int) Priority
    :param client_id: (int) Client ID
    :return: None
    """
    FeatureRequest.query.filter(FeatureRequest.priority >= priority, FeatureRequest.clientId == client_id). \
        update({FeatureRequest.priority: (FeatureRequest.priority + 1)})


app.register_blueprint(bp)
