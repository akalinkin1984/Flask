import flask
from flask import jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, Advertisement, User
from schema import CreateAdv, UpdateAdv, CreateUser, UpdateUser

app = flask.Flask("app")
bcrypt = Bcrypt(app)


def hash_password(password: str):
    return bcrypt.generate_password_hash(password.encode()).decode()


def check_password(password: str, hashed_password: str):
    return bcrypt.check_password_hash(hashed_password.encode(), password.encode())


class HttpError(Exception):

    def __init__(self, status_code: int, error_msg: str | dict | list):
        self.status_code = status_code
        self.error_msg = error_msg


@app.errorhandler(HttpError)
def http_error_handler(err: HttpError):
    http_response = jsonify({'status': 'error', 'message': err.error_msg})
    http_response.status_code = err.status_code
    return http_response


def validate_json(json_data: dict, schema_cls: type[CreateAdv] | type[UpdateAdv]):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response: flask.Response):
    request.session.close()
    return http_response


def get_adv(adv_id):
    adv = request.session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, 'Объявление не найдено')
    return adv


def add_adv(adv: Advertisement):
    request.session.add(adv)
    request.session.commit()
    return adv


def get_user(user_id):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'Юзер не найден')
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, 'Пользователь уже существует')
    return user


class AdvView(MethodView):

    def get(self, adv_id: int):
        adv = get_adv(adv_id)
        return jsonify(adv.json)

    def post(self):
        json_data = validate_json(request.json, CreateAdv)
        adv = Advertisement(**json_data)
        adv = add_adv(adv)
        return jsonify({'status': 'Объявление размещено', 'id': adv.id})

    def patch(self, adv_id: int):
        json_data = validate_json(request.json, UpdateAdv)
        adv = get_adv(adv_id)
        for field, value in json_data.items():
            setattr(adv, field, value)
        adv = add_adv(adv)
        return jsonify(adv.json)

    def delete(self, adv_id: int):
        adv = get_adv(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({'status': 'Объявление удалено'})


class UserView(MethodView):

    def get(self, user_id: int):
        user = get_user(user_id)
        return jsonify(user.json)

    def post(self):
        json_data = validate_json(request.json, CreateUser)
        json_data['password'] = hash_password(json_data['password'])
        user = User(**json_data)
        user = add_user(user)
        return jsonify({'status': 'Пользователь зарегестрирован', 'id': user.id})

    def patch(self, user_id: int):
        json_data = validate_json(request.json, UpdateUser)
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        user = get_user(user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
        user = add_user(user)
        return jsonify(user.json)

    def delete(self, user_id: int):
        user = get_adv(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({'status': 'Пользователь удален'})


adv_view = AdvView.as_view('adv')
user_view = UserView.as_view('user')

app.add_url_rule('/adv/', view_func=adv_view, methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>/', view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])

app.add_url_rule('/user/', view_func=user_view, methods=['POST'])
app.add_url_rule('/user/<int:adv_id>/', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])

app.run()
