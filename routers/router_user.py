from flask import Blueprint, request, jsonify
from services.connectDatabase import importData, exportData

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login_user():
    """
    User login
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
              example: "user@example.com"
              description: "User's email address"
            password:
              type: string
              example: "password123"
              description: "User's password"
    responses:
      200:
        description: Login successful
        schema:
          type: array
          items:
            type: string
          example: ["1", "John Doe", "user@example.com", "password123", "active", "123456789", "1990-01-01", "male", "Hanoi", "address", "100", "token123", "2023-01-01", "2023-01-01"]
      400:
        description: Login failed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid credentials"
    """
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        user = exportData(
            sql="SELECT * FROM users WHERE email = %s AND password = %s",
            val=(data["email"], data["password"]),
        )
        # Thanh đổi định dạng ngày trong danh sách
        data_list = list(user)
        data_list[6] = data_list[6].isoformat()
        user = tuple(data_list)
        return jsonify(user), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/register', methods=['POST'])
def register_user():
    """
    User registration
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
            - cccd
            - dob
            - gender
            - address
            - point
            - token
          properties:
            name:
              type: string
              example: "Nguyễn Văn A"
              description: "User's full name"
            email:
              type: string
              format: email
              example: "user@example.com"
              description: "User's email address"
            password:
              type: string
              example: "password123"
              description: "User's password"
            cccd:
              type: string
              example: "123456789012"
              description: "Citizen identification number"
            dob:
              type: string
              format: date
              example: "1990-01-01"
              description: "Date of birth"
            gender:
              type: string
              enum: ["male", "female", "other"]
              example: "male"
              description: "User's gender"
            address:
              type: string
              example: "123 Main Street, Hanoi"
              description: "User's address"
            point:
              type: integer
              example: 0
              description: "User's initial points"
            token:
              type: string
              example: "token123"
              description: "User's device token"
    responses:
      200:
        description: Registration successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Đăng ký thành công!"
      400:
        description: Registration failed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Registration error message"
    """
    try:
        data = request.get_json()  # Nhận JSON từ Flutter

        importData(
            sql="""INSERT INTO `users`
                    (`name`, `email`, `password`, `status`, `cccd`, `dob`, `gender`, `pob`, `address`, `point`, `token`, `created_at`, `updated_at`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())""",
            val=(
                data["name"], data["email"], data["password"],
                "4", data["cccd"], data["dob"], data["gender"],
                "", data["address"],data["point"], data["token"]
            )
        )

        print(data)

        # Trả phản hồi về Flutter
        return jsonify({"message": "Đăng ký thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/loadUser', methods=['POST'])
def loadUser():
    """
    Load specific user information
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id_user
          properties:
            id_user:
              type: string
              example: "1"
              description: "User ID to load information"
    responses:
      200:
        description: User information loaded successfully
        schema:
          type: array
          items:
            type: string
          example: ["1", "John Doe", "user@example.com", "password123", "active", "123456789", "1990-01-01", "male", "Hanoi", "address", "100", "token123", "2023-01-01", "2023-01-01"]
      400:
        description: Failed to load user
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    try:
        data = request.get_json()  # Nhận JSON từ Flutter

        user = exportData(
            sql="SELECT * FROM users WHERE id = %s",
            val=(data["id_user"],),
        )

        return jsonify(user), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@user_bp.route('/loadDataUser', methods=['POST'])
def loadDataUser():
    """
    Load users data (all users or exclude specific user)
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id_user
          properties:
            id_user:
              type: string
              example: "1"
              description: "User ID to exclude from results. Use '0' to get all users"
    responses:
      200:
        description: Users data loaded successfully
        schema:
          type: array
          items:
            type: array
            items:
              type: string
            example: ["1", "John Doe", "user@example.com", "password123", "active", "123456789", "1990-01-01", "male", "Hanoi", "address", "100", "token123", "2023-01-01", "2023-01-01"]
      400:
        description: Failed to load users data
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Database error"
    """
    data = request.get_json()  # Nhận JSON từ Flutter
    idUser = data["id_user"]


    try:
        if idUser == "0":
            user = exportData(
                sql="SELECT * FROM users",
                val=(),
                fetch_all=True
            )
        else:
            user = exportData(
                sql="SELECT * FROM users WHERE id <> %s",
                val=(idUser,),
                fetch_all=True
            )
        print(user)
        return jsonify(user), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400