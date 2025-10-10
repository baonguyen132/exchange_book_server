import json
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# from AI.scan_book import scan_book
from services.connectDatabase import importData, exportData

book_bp = Blueprint('book', __name__)

# Đường dẫn thư mục lưu trữ ảnh sách của client (cùng cấp với routers)
PUBLIC_IMAGE_BOOK_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public', 'image_book_client')

# Tạo thư mục nếu chưa tồn tại
os.makedirs(PUBLIC_IMAGE_BOOK_FOLDER, exist_ok=True)

# @book_bp.route('/upload_image_book', methods=['POST'])
# def upload_book():
#     """
#     Upload book image and analyze with AI
#     ---
#     tags:
#       - Book Management
#     consumes:
#       - multipart/form-data
#     parameters:
#       - name: image
#         in: formData
#         type: file
#         required: true
#         description: Book cover image to upload and analyze
#     responses:
#       200:
#         description: Image uploaded and analyzed successfully
#         schema:
#           type: object
#           properties:
#             message:
#               type: string
#               example: "Upload successful"
#             data:
#               type: object
#               description: Book data from AI analysis
#             path:
#               type: string
#               example: "public/image_book_client/book_cover.jpg"
#       400:
#         description: Upload failed
#         schema:
#           type: object
#           properties:
#             error:
#               type: string
#               example: "No image file found"
#     """
#     # Kiểm tra file ảnh
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file found"}), 400

#     image = request.files['image']

#     if image.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     # Tạo tên file unique với timestamp và uuid
#     ext = os.path.splitext(image.filename)[1]
#     new_filename = f"book_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}{ext}"
    
#     # Đổi tên file an toàn
#     filename = secure_filename(new_filename)
#     image_path = os.path.join(PUBLIC_IMAGE_BOOK_FOLDER, filename)
#     image.save(image_path)

#     # AI analysis (commented out until AI module is available)
#     # text_output = scan_book(image_path)
#     # book = exportData(
#     #     sql="SELECT * FROM `type_books` WHERE `id` = %s",
#     #     val=(text_output,)
#     # )
    
#     # Temporary response without AI
#     book = {"message": "AI analysis disabled temporarily"}

#     # Trả về đường dẫn ảnh hợp lệ với relative path
#     relative_path = f"public/image_book_client/{filename}"
    
#     return jsonify({
#         "message": "Upload successful",
#         "data": book,
#         "path": relative_path
#     }), 200


# @book_bp.route('/scan_books', methods=['POST'])
# def scan_books():
#     """
#     Scan book image and find matching books
#     ---
#     tags:
#       - Book Management
#     consumes:
#       - multipart/form-data
#     parameters:
#       - name: image
#         in: formData
#         type: file
#         required: true
#         description: Book image to scan and match
#       - name: id
#         in: formData
#         type: string
#         required: true
#         description: User ID to exclude from results
#         example: "123"
#     responses:
#       200:
#         description: Books found matching the scanned image
#         schema:
#           type: array
#           items:
#             type: object
#             properties:
#               id:
#                 type: integer
#                 example: 1
#               name_book:
#                 type: string
#                 example: "Toán học lớp 12"
#               type_book:
#                 type: string
#                 example: "Sách giáo khoa"
#               date_purchase:
#                 type: string
#                 example: "2024-01-15"
#               price:
#                 type: number
#                 example: 45000
#               description:
#                 type: string
#                 example: "Sách toán cũ, tình trạng tốt"
#               image:
#                 type: string
#                 example: "public/image_book_client/book_123.jpg"
#               id_user:
#                 type: integer
#                 example: 456
#               id_type_book:
#                 type: integer
#                 example: 5
#               status:
#                 type: integer
#                 example: 1
#               quantity:
#                 type: integer
#                 example: 2
#       400:
#         description: Scan failed
#         schema:
#           type: object
#           properties:
#             error:
#               type: string
#               example: "No image file found"
#     """
#     # Kiểm tra file ảnh
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file found"}), 400

#     image = request.files['image']

#     if image.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     # Tạo tên file unique
#     ext = os.path.splitext(image.filename)[1]
#     new_filename = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}{ext}"
    
#     # Đổi tên file an toàn và lưu tạm ảnh
#     filename = secure_filename(new_filename)
#     image_path = os.path.join(PUBLIC_IMAGE_BOOK_FOLDER, filename)
#     image.save(image_path)

#     # Lấy thêm trường id từ form-data
#     user_id = request.form.get('id')

#     if not user_id:
#         return jsonify({"error": "Missing user id"}), 400

#     # AI analysis (commented out until AI module is available)
#     # text_output = scan_book(image_path)
#     # books = exportData(...)
    
#     # Temporary: return all available books except user's own
#     books = exportData(
#         sql="""
#             SELECT  
#                 book.id, 
#                 type_books.name_book, 
#                 type_books.type_book, 
#                 book.date_purchase, 
#                 book.price, 
#                 book.description, 
#                 book.image,
#                 book.id_user,
#                 book.id_type_book,
#                 book.status,
#                 book.quantity
#             FROM book 
#             JOIN type_books ON book.id_type_book = type_books.id
#             WHERE book.status = 1 AND book.quantity > 0 AND book.id_user != %s
#             LIMIT 10
#         """,
#         val=(user_id,),
#         fetch_all=True
#     )

#     return jsonify(books), 200


@book_bp.route('/insertBook', methods=['POST'])
def insertBook():
    """
    Insert new book listing
    ---
    tags:
      - Book Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - date_purchase
            - price
            - description
            - status
            - quantity
            - image
            - id_user
            - id_type_book
          properties:
            date_purchase:
              type: string
              format: date
              example: "2024-01-15"
              description: "Date when book was purchased"
            price:
              type: number
              example: 45000
              description: "Book selling price in VND"
            description:
              type: string
              example: "Sách toán cũ, tình trạng tốt, không viết vẽ"
              description: "Book condition description"
            status:
              type: integer
              example: 1
              description: "Book status (1=available, 0=sold)"
            quantity:
              type: integer
              example: 2
              description: "Number of books available"
            image:
              type: string
              example: "public/image_book_client/book_123.jpg"
              description: "Book image path"
            id_user:
              type: integer
              example: 123
              description: "Owner user ID"
            id_type_book:
              type: integer
              example: 5
              description: "Book type ID from type_books table"
    responses:
      200:
        description: Book inserted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Thêm sách thành công!"
      400:
        description: Insert failed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error details"
    """
    try:
        data = request.get_json()
        importData(
            sql="""
            INSERT INTO `book`(`date_purchase`, `price`, `description`, `status`, `quantity` ,`image`, `id_user`, `id_type_book`, `created_at`, `updated_at`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
            val=(
                data["date_purchase"],
                data["price"],
                data["description"],
                data["status"],
                data["quantity"],
                data["image"],
                data["id_user"],
                data["id_type_book"]
            )
        )

        return jsonify({"message": "Thêm sách thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@book_bp.route("/exportMyBook", methods=['POST'])
def exportMyBook():
    """
    Get user's own book listings
    ---
    tags:
      - Book Management
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
              type: integer
              example: 123
              description: "User ID to get books for"
    responses:
      200:
        description: User's books retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name_book:
                type: string
                example: "Toán học lớp 12"
              type_book:
                type: string
                example: "Sách giáo khoa"
              date_purchase:
                type: string
                example: "2024-01-15"
              price:
                type: number
                example: 45000
              description:
                type: string
                example: "Sách toán cũ, tình trạng tốt"
              image:
                type: string
                example: "public/image_book_client/book_123.jpg"
              id_user:
                type: integer
                example: 123
              id_type_book:
                type: integer
                example: 5
              status:
                type: integer
                example: 1
              quantity:
                type: integer
                example: 2
    """
    data = request.get_json()

    list = exportData(
        sql="""SELECT  
        book.id, 
        type_books.name_book, 
        type_books.type_book, 
        book.date_purchase, 
        book.price, 
        book.description, 
        book.image ,
        book.id_user,
        book.id_type_book,
        book.status,
        book.quantity
        FROM book JOIN type_books ON book.id_type_book = type_books.id 
        WHERE book.id_user = %s""",
        val=(data["id_user"],),
        fetch_all=True
    )

    return jsonify(list), 200

@book_bp.route("/exportBook", methods=['POST'])
def exportBook():
    """
    Get available books from other users
    ---
    tags:
      - Book Management
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
              type: integer
              example: 123
              description: "Current user ID (to exclude from results)"
    responses:
      200:
        description: Available books from other users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name_book:
                type: string
                example: "Toán học lớp 12"
              type_book:
                type: string
                example: "Sách giáo khoa"
              date_purchase:
                type: string
                example: "2024-01-15"
              price:
                type: number
                example: 45000
              description:
                type: string
                example: "Sách toán cũ, tình trạng tốt"
              image:
                type: string
                example: "public/image_book_client/book_123.jpg"
              id_user:
                type: integer
                example: 456
              id_type_book:
                type: integer
                example: 5
              status:
                type: integer
                example: 1
              quantity:
                type: integer
                example: 2
    """
    data = request.get_json()

    books = exportData(
        sql="""
            SELECT  
                book.id, 
                type_books.name_book, 
                type_books.type_book, 
                book.date_purchase, 
                book.price, 
                book.description, 
                book.image,
                book.id_user,
                book.id_type_book,
                book.status,
                book.quantity
            FROM book 
            JOIN type_books ON book.id_type_book = type_books.id
            WHERE book.status = 1 AND book.quantity > 0 AND book.id_user != %s
        """,
        val=(data["id_user"], ),
        fetch_all=True
    )

    return jsonify(books), 200


@book_bp.route('/deleteBook', methods=['POST'])
def deleteBook():
    """
    Delete book listing
    ---
    tags:
      - Book Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id
            - image
          properties:
            id:
              type: integer
              example: 1
              description: "Book ID to delete"
            image:
              type: string
              example: "public/image_book_client/book_123.jpg"
              description: "Image path to delete from filesystem"
    responses:
      200:
        description: Book deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Xoá thành công!"
      400:
        description: Delete failed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error details"
    """
    try:
        data = request.get_json()
        importData(
            sql="""DELETE FROM `book` WHERE `id` = %s """,
            val=(data["id"],)
        )

        # Delete image file if exists
        image_path = data["image"]
        if os.path.exists(image_path):
            os.remove(image_path)
            print("Đã xóa ảnh.")
        else:
            print("Ảnh không tồn tại.")

        return jsonify({"message": "Xoá thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@book_bp.route('/updateBook', methods=['POST'])
def updateBook():
    """
    Update book listing details
    ---
    tags:
      - Book Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id
            - date_purchase
            - price
            - description
            - quantity
          properties:
            id:
              type: integer
              example: 1
              description: "Book ID to update"
            date_purchase:
              type: string
              format: date
              example: "2024-01-15"
              description: "Updated purchase date"
            price:
              type: number
              example: 40000
              description: "Updated selling price in VND"
            description:
              type: string
              example: "Sách toán cũ, giảm giá nhanh"
              description: "Updated book description"
            quantity:
              type: integer
              example: 1
              description: "Updated quantity available"
    responses:
      200:
        description: Book updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Cập nhật thành công!"
      400:
        description: Update failed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error details"
    """
    try:
        data = request.get_json()
        importData(
            sql="""
            UPDATE `book` SET 
            `date_purchase`=%s,
            `price`=%s,
            `description`=%s,
            `quantity`=%s,
            `updated_at`=NOW() 
            WHERE `id`= %s """,
            val=(
                data["date_purchase"], data["price"], data["description"], data["quantity"], data["id"]
            )
        )

        return jsonify({"message": "Cập nhật thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@book_bp.route('/public/image_book_client/<path:filename>')
def serve_image(filename):
    """
    Serve book client images
    ---
    tags:
      - Book Management
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: Image filename to serve
        example: "book_123.jpg"
    produces:
      - image/jpeg
      - image/png
      - image/gif
    responses:
      200:
        description: Image file served successfully
        content:
          image/jpeg:
            schema:
              type: string
              format: binary
      404:
        description: Image not found
    """
    return send_from_directory("public/image_book_client", filename)