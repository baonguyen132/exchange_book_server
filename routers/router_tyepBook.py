import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from services.connectDatabase import importData, exportData

# Khởi tạo Blueprint
type_book_bp = Blueprint('typeBook', __name__)

# Đường dẫn thư mục lưu trữ ảnh
PUBLIC_IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public', 'image')

# Tạo thư mục nếu chưa tồn tại
os.makedirs(PUBLIC_IMAGE_FOLDER, exist_ok=True)


@type_book_bp.route('/insertTypeBook', methods=['POST'])
def insertTypeBook():
    """
    Insert new book type
    ---
    tags:
      - Type Book Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name_book
            - type_book
            - price
            - image
            - description
          properties:
            name_book:
              type: string
              example: "Toán học lớp 12"
              description: "Book name/title"
            type_book:
              type: string
              example: "Sách giáo khoa"
              description: "Book category/type"
            price:
              type: number
              example: 50000
              description: "Book price in VND"
            image:
              type: string
              example: "public/image/book_123.jpg"
              description: "Book cover image path"
            description:
              type: string
              example: "Sách toán học chương trình lớp 12"
              description: "Book description"
    responses:
      200:
        description: Book type inserted successfully
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
        data = request.get_json()  # Nhận JSON từ Flutter
        print(data)
        importData(
            sql="""INSERT INTO `type_books`
                    (`name_book`, `type_book`, `price` ,`image`, `description`, `created_at`, `updated_at`)
                    VALUES (%s, %s ,%s, %s, %s, NOW(), NOW())""",
            val=(
                data["name_book"], data["type_book"], data["price"] ,data["image"], data["description"]
            )
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Thêm sách thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@type_book_bp.route('/updateTypeBook', methods=['POST'])
def updateTypeBook():
    """
    Update existing book type
    ---
    tags:
      - Type Book Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id
            - name_book
            - type_book
            - price
            - image
            - description
          properties:
            id:
              type: string
              example: "1"
              description: "Book type ID to update"
            name_book:
              type: string
              example: "Toán học lớp 12 (Updated)"
              description: "Updated book name/title"
            type_book:
              type: string
              example: "Sách giáo khoa"
              description: "Updated book category/type"
            price:
              type: number
              example: 55000
              description: "Updated book price in VND"
            image:
              type: string
              example: "public/image/book_123_new.jpg"
              description: "Updated book cover image path"
            description:
              type: string
              example: "Sách toán học chương trình lớp 12 phiên bản mới"
              description: "Updated book description"
    responses:
      200:
        description: Book type updated successfully
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
        data = request.get_json()  # Nhận JSON từ Flutter
        importData(
            sql="""UPDATE `type_books` SET 
            `name_book`=%s,
            `type_book`=%s,
            `price` = %s ,
            `image`=%s,
            `description`=%s,
            `updated_at`=NOW() 
            WHERE `id`= %s """,
            val=(
                data["name_book"], data["type_book"], data["price"] ,data["image"], data["description"] , data["id"]
            )
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Cập nhật thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@type_book_bp.route('/deleteTypeBook', methods=['POST'])
def deleteTypeBook():
    """
    Delete a book type
    ---
    tags:
      - Type Book Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id
          properties:
            id:
              type: string
              example: "1"
              description: "Book type ID to delete"
    responses:
      200:
        description: Book type deleted successfully
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
        data = request.get_json()  # Nhận JSON từ Flutter
        importData(
            sql="""DELETE FROM `type_books` WHERE `id` = %s """,
            val=(data["id"],)
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Xoá thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@type_book_bp.route("/exportTypeBook", methods=['GET'])
def exportTypeBook():
    """
    Get all book types
    ---
    tags:
      - Type Book Management
    responses:
      200:
        description: List of all book types
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: "1"
                description: "Book type ID"
              name_book:
                type: string
                example: "Toán học lớp 12"
                description: "Book name/title"
              type_book:
                type: string
                example: "Sách giáo khoa"
                description: "Book category/type"
              price:
                type: number
                example: 50000
                description: "Book price in VND"
              image:
                type: string
                example: "public/image/book_123.jpg"
                description: "Book cover image path"
              description:
                type: string
                example: "Sách toán học chương trình lớp 12"
                description: "Book description"
              created_at:
                type: string
                format: date-time
                example: "2023-12-01T10:30:00Z"
                description: "Creation timestamp"
              updated_at:
                type: string
                format: date-time
                example: "2023-12-02T15:45:00Z"
                description: "Last update timestamp"
      400:
        description: Export failed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error details"
    """
    try:
        list = exportData(
            sql="SELECT * FROM `type_books` WHERE 1",
            val=(),
            fetch_all=True
        )

        return jsonify(list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@type_book_bp.route('/upload_type_image_book', methods=['POST'])
def uploadImageBook():
    """
    Upload book cover image
    ---
    tags:
      - Type Book Management
    consumes:
      - multipart/form-data
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: Book cover image to upload
    responses:
      200:
        description: Image uploaded successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Upload successful"
            file_path:
              type: string
              example: "public/image/book_20241010_123456_abc123.jpg"
              description: "Relative path to uploaded image"
      400:
        description: Upload failed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No image file found"
    """
    try:
        # Kiểm tra file ảnh
        if 'image' not in request.files:
            return jsonify({"error": "No image file found"}), 400

        image = request.files['image']

        if image.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Validate file extension
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        ext = os.path.splitext(image.filename)[1].lower()
        
        if ext not in allowed_extensions:
            return jsonify({"error": "Invalid file type. Allowed: jpg, jpeg, png, gif, bmp"}), 400

        # Tạo tên file mới với timestamp và UUID
        new_filename = f"book_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}{ext}"

        # Đảm bảo tên file an toàn
        filename = secure_filename(new_filename)
        image_path = os.path.join(PUBLIC_IMAGE_FOLDER, filename)
        
        # Lưu file ảnh
        image.save(image_path)
        
        # Tạo relative path để trả về (không có dấu / ở đầu)
        relative_path = f"public/image/{filename}"

        return jsonify({
            "message": "Upload successful",
            "file_path": relative_path
        }), 200

    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 400

@type_book_bp.route('/public/image/<path:filename>')
def serve_image(filename):
    """
    Serve book cover images
    ---
    tags:
      - Type Book Management
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: "Image filename to serve"
        example: "book_20231201_143052_abc123.jpg"
    responses:
      200:
        description: Image file served successfully
        schema:
          type: file
      404:
        description: Image file not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "File not found"
    """
    return send_from_directory("public/image", filename)