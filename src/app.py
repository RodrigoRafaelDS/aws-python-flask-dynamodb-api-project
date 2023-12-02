from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from mangum import Mangum

from src.handlerInfos import save_info
from src.handlerUser import create_user, validate_login
from src.jwt_utils import validate_jwt
from src.validations import is_strong_password, is_valid_email

app = FastAPI()


@app.post("/saveUser")
def save_user(user: dict):
    email = user.get("email")
    password = user.get("password")

    if not is_valid_email(email):
        return JSONResponse({"error": "Please provide a valid email and password"}), 400

    if not is_strong_password(password):
        return JSONResponse({"error": "Please provide a valid password"}), 400

    return create_user(email, password)


@app.post("/login")
def login(user: dict):
    email = user.get("email")
    password = user.get("password")

    if not is_valid_email(email):
        return JSONResponse({"error": "Please provide a valid email and password"}), 400

    if not is_strong_password(password):
        return JSONResponse({"error": "Please provide a valid password"}), 400

    return validate_login(email, password)


@app.post("/saveInfo")
def save_info_endpoint(user_info: dict, authorization=Header()):
    data = user_info

    email = data.get("email")
    name = data.get("name")
    address = data.get("address")
    phone = data.get("phone")

    if not email or not name or not address or not phone:
        return JSONResponse({"error": "Please provide all required fields"}), 400

    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse({"error": "Authorization required"}), 401

    token = authorization.split(" ")[1]
    decoded_token = validate_jwt(token)

    if not decoded_token or "email" not in decoded_token:
        return JSONResponse({"error": "Invalid token"}), 401

    token_email = decoded_token["email"]

    if not token_email or token_email != email:
        return JSONResponse({"error": "Invalid token (email)"}), 401

    result = save_info(email, name, address, phone)
    return result


handler = Mangum(app)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

# @app.errorhandler(404)
# def resource_not_found(e):
#     return make_response(JSONResponse(error="Not found!"), 404)
