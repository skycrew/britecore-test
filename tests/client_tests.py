import unittest
from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy_utils import create_database, drop_database
from web.app import create_app
from web.models import db
from web.init_db import create_dummy_data


class TestClient(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TESTING")
        self.app_context = self.app.app_context()
        self.app_context.push()

        create_database(self.app.config["SQLALCHEMY_DATABASE_URI"])
        db.create_all()
        create_dummy_data()

        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        drop_database(self.app.config["SQLALCHEMY_DATABASE_URI"])

        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config_name == "TESTING")

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("List of Feature Requests" in response.get_data(as_text=True))
        self.assertTrue("Client A" in response.get_data(as_text=True))
        self.assertTrue("Client B" in response.get_data(as_text=True))
        self.assertTrue("Client C" in response.get_data(as_text=True))

    def test_client_feature_requests(self):
        response = self.client.get("/client/Client C")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("List of Feature Requests" in response.get_data(as_text=True))
        self.assertTrue("Sample title 1" in response.get_data(as_text=True))
        self.assertTrue('<td><a href="/client/Client C">Client C</a></td>' in response.get_data(as_text=True))
        self.assertFalse('<td><a href="/client/Client A">Client A</a></td>' in response.get_data(as_text=True))

    def test_successfully_add_feature_request(self):
        form_data = {
            "frTitle": "Unit test title",
            "frDescription": "Unit test description",
            "frClient": "3",
            "frPriority": "10",
            "frTargetDate": "2018-11-15",
            "frProduct": "1"
        }
        response = self.client.post("/add", data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals('{"url":"/"}\n', response.get_data())

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Unit test title" in response.get_data(as_text=True))

    def test_failed_add_feature_request(self):
        form_data = {
            "frTitle": "",
            "frDescription": "Unit test description",
            "frClient": "3",
            "frPriority": "10",
            "frTargetDate": "2018-11-15",
            "frProduct": "1"
        }
        response = self.client.post("/add", data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals('{"errors":["Title is empty!"]}\n', response.get_data())

    def test_priority_reordered_after_add_feature_request(self):
        for i in range(2, 10):
            self.client.get("/delete/%d" % i)

        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(1 == response.json["priority"])

        form_data = {
            "frTitle": "Unit test title",
            "frDescription": "Unit test description",
            "frClient": "3",
            "frPriority": "1",
            "frTargetDate": "2018-11-15",
            "frProduct": "1"
        }
        self.client.post("/add", data=form_data)

        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(2 == response.json["priority"])

    def test_edit_feature_request(self):
        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Sample title 1" == response.json["title"])
        description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sodales efficitur convallis." \
                      " Fusce blandit turpis non laoreet blandit. Fusce aliquam ipsum eget eros volutpat egestas. " \
                      "Fusce viverra leo id molestie molestie. Morbi sagittis orci sed felis maximus scelerisque. " \
                      "Etiam magna ante, sollicitudin porta euismod sed, porttitor nec felis."
        self.assertTrue(description == response.json["description"])
        self.assertTrue(3 == response.json["clientId"])
        self.assertTrue(1 == response.json["priority"])
        self.assertTrue((datetime.utcnow() + timedelta(days=10)).strftime("%Y-%m-%d") == response.json["targetDate"])
        self.assertTrue(2 == response.json["productId"])

        form_data = {
            "frTitleEdit": "Unit test title",
            "frDescriptionEdit": "Unit test description",
            "frClientEdit": "3",
            "frPriorityEdit": "1",
            "frTargetDateEdit": "2018-12-12",
            "frProductEdit": "1"
        }

        response = self.client.post("/edit/1", data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals('{"url":"/"}\n', response.get_data())

        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Unit test title" == response.json["title"])
        self.assertTrue("Unit test description" == response.json["description"])
        self.assertTrue(3 == response.json["clientId"])
        self.assertTrue(1 == response.json["priority"])
        self.assertTrue("2018-12-12" == response.json["targetDate"])
        self.assertTrue(1 == response.json["productId"])

    def test_failed_edit_feature_request(self):
        form_data = {
            "frTitleEdit": "Unit test title",
            "frDescriptionEdit": None,
            "frClientEdit": "3",
            "frPriorityEdit": "1",
            "frTargetDateEdit": "2018-12-12",
            "frProductEdit": "1"
        }
        response = self.client.post("/edit/1", data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals('{"errors":["Description is empty!"]}\n', response.get_data())

    def test_edit_unknown_feature_request(self):
        response = self.client.get("/edit/100")
        self.assertEqual(response.status_code, 404)

    def test_delete_feature_request(self):
        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Sample title 1" == response.json["title"])

        response = self.client.get("/delete/1")
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 404)
