from flask_testing import TestCase
from app import create_app, db
from app.models import User
#from app.db import user_repository

class TestUserViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_show(self):
        first_user = User()
        first_user.name = "First user"
        db.session.add(first_user)
        db.session.commit()
        response = self.client.get("/users/1")
        response_user = response.json
        self.assertEqual(response_user["id"], 1)
        self.assertEqual(response_user["name"], "First user")


    def test_user_create(self):
        response = self.client.post("/users", json={'name': 'New user!'})
        created_user = response.json
        print(created_user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_user["id"], 1)
        self.assertEqual(created_user["name"], "New user!")
        self.assertIsNotNone(created_user["api_token"])

    def test_user_update(self):
        first_user = User()
        first_user.name = "First user"
        db.session.add(first_user)
        db.session.commit()
        response = self.client.patch("/users/1", json={'name': 'New name'})
        updated_user = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_user["id"], 1)
        self.assertEqual(updated_user["name"], "New name")

    def test_user_delete(self):
        first_user = User()
        first_user.name = "First user"
        db.session.add(first_user)
        db.session.commit()
        self.client.delete("/users/1")
        self.assertIsNone(db.session.query(User).get(1))
