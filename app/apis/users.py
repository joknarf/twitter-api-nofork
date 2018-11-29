import uuid
from flask_restplus import Namespace, Resource, fields
from flask import abort, request
#from flask_login import current_user
from app import db
#from app.db import user_repository
from app.models import User

api = Namespace('users')

json_user = api.model('User', {
    'id': fields.Integer,
    'name': fields.String,
    'api_token': fields.String,
})

json_new_user = api.model('New user', {
    'name': fields.String(required=True)
})

@api.route('/<string:name>')
@api.response(404, 'User not found')
@api.param('name', 'The user unique name')
class UserName(Resource):
    @api.marshal_with(json_user)
    def get(self, name):
        user = db.session.query(User).filter_by(name=name).first()
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            return user


@api.route('/<int:id>')
@api.response(404, 'User not found')
@api.param('id', 'The user unique identifier')
class UserResource(Resource):
    @api.marshal_with(json_user)
    def get(self, id):
        user = db.session.query(User).get(id)
        db.session.commit()
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            return user

    @api.marshal_with(json_user, code=200)
    @api.expect(json_new_user, validate=True)
    def patch(self, id):
        user = db.session.query(User).get(id)
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            user.name = api.payload["name"]
            db.session.commit()
            return user

    def delete(self, id):
        user = db.session.query(User).get(id)
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            db.session.delete(user)
            db.session.commit()
            return None

@api.route('')
@api.response(422, 'Invalid user')
class UsersResource(Resource):
    @api.marshal_with(json_user, code=201)
    @api.expect(json_new_user, validate=True)
    def post(self):
        name = api.payload["name"]
        user = user = db.session.query(User).filter_by(name=name).first()
        if user is not None:
            return user, 201
        if len(name) > 0:
            user = User()
            user.name = name
            user.api_token = str(uuid.uuid1())
            db.session.add(user)
            db.session.commit()
            return user, 201
        else:
            return abort(422, "User name can't be empty")
