import json
from datetime import datetime

from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from services.connectDatabase import importData, exportData, importDataGetId

cart_bp = Blueprint('cart', __name__)

@cart_bp.route("/export_cart_purchase", methods=['POST'])
def export_cart_purchase():
    """
    Get purchase cart history for user
    ---
    tags:
      - Cart Management
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
              description: "User ID to get purchase history"
    responses:
      200:
        description: Purchase cart history retrieved successfully
        schema:
          type: array
          items:
            type: array
            items:
              type: string
            example: ["1", "Xác nhận đơn", "123 Main Street", "50000", "Seller Name"]
    """
    data = request.get_json()

    list = exportData(
        sql="""
        SELECT 
            cart.id, 
            cart.status, 
            cart.address, 
            cart.total, 
            users.name 
        FROM `cart` JOIN users 
        ON cart.id_seller = users.id 
        WHERE cart.id_user = %s """,
        val=(data["id_user"],),
        fetch_all=True
    )
    return jsonify(list), 200

@cart_bp.route("/export_cart_seller", methods=['POST'])
def export_cart_seller():
    """
    Get seller cart history
    ---
    tags:
      - Cart Management
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
              description: "Seller ID to get cart history"
    responses:
      200:
        description: Seller cart history retrieved successfully
        schema:
          type: array
          items:
            type: array
            items:
              type: string
            example: ["1", "Xác nhận đơn", "123 Main Street", "50000", "Buyer Name"]
    """
    data = request.get_json()

    list = exportData(
        sql="""
        SELECT 
            cart.id, 
            cart.status, 
            cart.address, 
            cart.total, 
            users.name 
        FROM `cart` JOIN users 
        ON cart.id_user = users.id 
        WHERE cart.id_seller = %s """,
        val=(data["id_user"],),
        fetch_all=True
    )

    return jsonify(list), 200


@cart_bp.route("/update_state_cart", methods=['POST'])
def update_state_cart():
    """
    Update cart status
    ---
    tags:
      - Cart Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - state
            - total
            - id_user
            - id_cart
          properties:
            state:
              type: string
              enum: ["Xác nhận đơn", "Đang giao", "Đã chuyển", "Đã hủy"]
              example: "Đã chuyển"
              description: "New cart status"
            total:
              type: string
              example: "50000"
              description: "Cart total amount"
            id_user:
              type: string
              example: "1"
              description: "User ID"
            id_cart:
              type: string
              example: "1"
              description: "Cart ID to update"
    responses:
      200:
        description: Cart status updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Cập nhật trạng thái giỏ hàng thành công"
            result:
              type: string
              example: "Update result"
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Thiếu trường dữ liệu cần thiết."
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Lỗi xử lý: error message"
    """
    try:
        data = request.get_json()
        now = datetime.now()
        print(data)

        # Kiểm tra trường dữ liệu bắt buộc
        required_fields = ["state", "total", "id_user", "id_cart"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Thiếu trường dữ liệu cần thiết."}), 400

        # Cộng điểm nếu đơn hàng đã chuyển
        if data["state"] == "Đã chuyển":
            importData(
                sql="""UPDATE `users` SET `point` = `point` + %s WHERE id = %s""",
                val=(int(data["total"]), data["id_user"]),
            )

        # Cập nhật trạng thái đơn hàng
        result = importData(
            sql="""
            UPDATE `cart` 
            SET `status` = %s,
                `updated_at` = %s
            WHERE `id` = %s
            """,
            val=(data["state"], now, data["id_cart"])
        )

        return jsonify({"message": "Cập nhật trạng thái giỏ hàng thành công", "result": result})

    except Exception as e:
        return jsonify({"error": f"Lỗi xử lý: {str(e)}"}), 500

@cart_bp.route("/export_item_cart", methods=['POST'])
def export_item_cart():
    """
    Get cart items details
    ---
    tags:
      - Cart Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id_cart
          properties:
            id_cart:
              type: string
              example: "1"
              description: "Cart ID to get items"
    responses:
      200:
        description: Cart items retrieved successfully
        schema:
          type: array
          items:
            type: array
            items:
              type: string
            example: ["1", "2", "5", "2023-01-01", "25000", "Book description", "image.jpg", "Book Title"]
    """
    data = request.get_json()

    list = exportData(
        sql=""
            "SELECT detail_cart.id, detail_cart.quantity, detail_cart.id_book,book.date_purchase, book.price,book.description, book.image,type_books.name_book  FROM `detail_cart` JOIN book ON detail_cart.id_book = book.id JOIN type_books ON book.id_type_book = type_books.id WHERE detail_cart.id_cart = %s ",
        val=(int(data["id_cart"]),),
        fetch_all=True,
    )

    print(list)

    return jsonify(list), 200


@cart_bp.route('/insert_cart', methods=['POST'])
def insertCart():
    """
    Create new cart with items
    ---
    tags:
      - Cart Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - address
            - total
            - data
            - id_user
          properties:
            address:
              type: string
              example: "123 Main Street, Hanoi"
              description: "Delivery address"
            total:
              type: string
              example: "50000-30000"
              description: "Total amounts separated by dash for multiple sellers"
            data:
              type: object
              description: "Cart data with seller IDs and their books (JSON structure)"
              example:
                "1":
                  "book1": '{"quantity": 2, "bookModal": {"id": 5}}'
                "2":
                  "book2": '{"quantity": 1, "bookModal": {"id": 3}}'
            id_user:
              type: string
              example: "1"
              description: "Buyer user ID"
    responses:
      200:
        description: Cart created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Insert successful"
      500:
        description: Cart creation failed
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Insert failed"
            error:
              type: string
              example: "Error details"
    """
    data = request.get_json()
    address = data.get("address", "")
    total_raw = data.get("total", "0")
    all_items = data.get("data", {})
    id_user = int(data.get("id_user", 0))

    total_list = [int(t.strip()) for t in total_raw.split('-') if t.strip().isdigit()]
    now = datetime.now()



    try:
        for index, (seller_id, books_json) in enumerate(all_items.items()):
            if not books_json:
                continue

            books = json.loads(books_json)
            total = total_list[index] if index < len(total_list) else 0

            cart_id = importDataGetId(
                sql="""
                    INSERT INTO cart (
                        status, address, total, id_user, id_seller, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                val=("Xác nhận đơn", address, total, id_user, int(seller_id), now, now)
            )

            importData(
                sql="""UPDATE `users` SET `point` = `point` - %s WHERE id = %s""",
                val=(int(total), id_user)
            )

            for book_detail_json in books.values():
                book_detail = json.loads(book_detail_json)
                quantity = book_detail.get("quantity", 0)
                book_info = book_detail.get("bookModal", {})
                id_book = int(book_info.get("id", 0))

                importData(
                    sql="""
                        INSERT INTO detail_cart (quantity, id_book, id_cart)
                        VALUES (%s, %s, %s)
                    """,
                    val=(quantity, id_book, cart_id)
                )

        return {"message": "Insert successful"}, 200

    except Exception as e:
        print("Error inserting cart:", e)
        return {"message": "Insert failed", "error": str(e)}, 500


