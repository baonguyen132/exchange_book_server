from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger

from routers.router_book import book_bp
from routers.router_cart import cart_bp
from routers.router_transaction import transaction
from routers.router_tyepBook import type_book_bp
from routers.router_user import user_bp
from services.sendEmail import sendMail

from routers.router_image import image_bp



app = Flask(__name__)
CORS(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Exchange Book Server API",
        "description": "API documentation for Exchange Book Server",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getmyData"
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


@app.route('/sendOtp', methods=['POST'])
def send_otp():
    """
    Send OTP to email
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - code
          properties:
            email:
              type: string
              format: email
              example: "user@example.com"
              description: "Email address to send OTP"
            code:
              type: string
              example: "123456"
              description: "OTP code to send"
    responses:
      200:
        description: OTP sent successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Mã OTP đã được gửi!"
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Thiếu email hoặc mã OTP!"
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Server error message"
    """
    try:
        data = request.get_json()
        if not data or "email" not in data or "code" not in data:
            return jsonify({"error": "Thiếu email hoặc mã OTP!"}), 400

        sendMail(data["email"], "Code Otp", f"Mã OTP của bạn là: {data['code']}")
        # Note: sendMail function is commented out - implement email service

        return jsonify({"message": "Mã OTP đã được gửi!"}), 200
    except Exception as e:
        print(f"❌ Lỗi trong send_otp(): {e}")
        return jsonify({"error": str(e)}), 500


app.register_blueprint(image_bp)
app.register_blueprint(type_book_bp)
app.register_blueprint(book_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(user_bp)
app.register_blueprint(transaction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)