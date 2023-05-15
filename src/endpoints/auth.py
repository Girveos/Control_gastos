from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, create_access_token, jwt_required, current_user, set_access_cookies, unset_jwt_cookies
from http import HTTPStatus
from datetime import datetime, timedelta, timezone

from src.models.user import User, user_schema, users_schema
from src.database import jwt

auth = Blueprint("auth",
                __name__,
                url_prefix="/api/v1/auth")

@auth.post("/login")
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=username).one_or_none()
    if not user or not user.check_password(password):
        return {"error": "Wrong username or password"}, HTTPStatus.UNAUTHORIZED
    
    access_token = create_access_token(identity=user_schema.dump(user))

    response = {"access_token": access_token}

    set_access_cookies(jsonify(response), access_token)
    
    return response, HTTPStatus.OK

@auth.route("/logout", methods=["POST"])
def logout():
    response = {"message": "logout successful"}
    unset_jwt_cookies(jsonify(response))
    return response, HTTPStatus.OK

@auth.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
