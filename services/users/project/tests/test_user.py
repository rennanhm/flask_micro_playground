import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly"""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "rennan", "email": "rennan@almeida.teste",
                     "password": "greaterthaneight"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("rennan@almeida.teste was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                "/users", data=json.dumps({}), content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "rennan@almeida.teste"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "rennan", "email": "rennan@almeida.teste",
                     "password": "greaterthaneight"}
                ),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "rennan", "email": "rennan@almeida.teste",
                     "password": "greaterthaneight"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That email already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user("rennan", "rennan@almeida.teste", "graterthaneight")
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("rennan", data["data"]["username"])
            self.assertIn("rennan@almeida.teste", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get("/users/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_user(self):
        """Ensure get all users behaves correcly."""
        add_user("rennan", "rennan@almeida.teste", "graterthaneight")
        add_user("paulo", "paulo@notreal.teste", "graterthaneight")
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("rennan", data["data"]["users"][0]["username"])
            self.assertIn(
                "rennan@almeida.teste", data["data"]["users"][0]["email"]
            )
            self.assertIn("paulo", data["data"]["users"][1]["username"])
            self.assertIn(
                "paulo@notreal.teste", data["data"]["users"][1]["email"]
            )
            self.assertIn("success", data["status"])

    def test_main_no_users(self):
        """
        Ensure the main route behaves correctly when no users have been added
        to the database.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Users", response.data)
        self.assertIn(b"<p>No users!</p>", response.data)

    def test_main_with_users(self):
        add_user("rennan", "rennan@almeida.com", "graterthaneight")
        add_user("paulo", "paulo@fakeemail.com", "graterthaneight")
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"rennan", response.data)
            self.assertIn(b"paulo", response.data)

    def test_main_add_user(self):
        """
        Ensure a new user can be added to the database via a POST request.
        """
        with self.client:
            response = self.client.post(
                "/",
                data=dict(
                    username="rennan",
                    email="rennan@almeida.com",
                    password="graterthaneight"
                ),
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"rennan", response.data)

    def test_add_user_invalid_json_key_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='rennan',
                    email='rennan@almeida.com'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])


if __name__ == "__main__":
    unittest.main()
