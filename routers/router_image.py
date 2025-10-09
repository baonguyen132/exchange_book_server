import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from services.connectDatabase import importData, exportData

image_bp = Blueprint('image', __name__)

# Đường dẫn uploads cùng cấp với thư mục routers
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

@image_bp.route('/upload_image', methods=['POST'])
def upload_file():
    """
    Upload image file for user
    ---
    tags:
      - Image Management
    consumes:
      - multipart/form-data
    parameters:
      - name: number
        in: formData
        type: string
        required: true
        example: "123"
        description: "Folder number/identifier for organizing images"
      - name: status
        in: formData
        type: string
        required: true
        example: "active"
        description: "Image status"
      - name: id
        in: formData
        type: string
        required: true
        example: "1"
        description: "User ID"
      - name: image
        in: formData
        type: file
        required: true
        description: "Image file to upload"
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
              example: "uploads/123/image.jpg"
      400:
        description: Upload failed
        schema:
          type: object
          properties:
            error:
              type: string
              enum: ["Missing number", "No image file found", "No selected file"]
              example: "Missing number"
    """
    # Kiểm tra số có được gửi lên không
    number = request.form.get('number')
    status = request.form.get('status')
    id = request.form.get('id')

    if not number:
        return jsonify({"error": "Missing number"}), 400

    # Tạo thư mục theo số
    folder_path = os.path.join(UPLOAD_FOLDER, number)
    os.makedirs(folder_path, exist_ok=True)

    # Kiểm tra file ảnh
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Bảo mật filename
    filename = secure_filename(image.filename)
    
    # Lưu ảnh vào thư mục tương ứng
    image_path = os.path.join(folder_path, filename)
    image.save(image_path)

    # Lưu đường dẫn tương đối vào database
    relative_path = os.path.join('uploads', number, filename).replace('\\', '/')
    
    importData(
        sql="""INSERT INTO `images`(`path`, `status`, `id_user`) VALUES (%s,%s,%s)""",
        val=(relative_path, status, id)
    )

    return jsonify({"message": "Upload successful", "file_path": relative_path})
@image_bp.route('/export_image_avata', methods=['POST'])
def export_image_avata():
    """
    Get user's latest avatar image
    ---
    tags:
      - Image Management
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
              description: "User ID to get avatar image"
    responses:
      200:
        description: Avatar image path retrieved successfully
        schema:
          type: object
          properties:
            path:
              type: string
              example: "uploads/123/avatar.jpg"
              description: "Relative path to the avatar image"
      400:
        description: Missing required parameter
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Thiếu tham số 'id'"
      404:
        description: No image found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Không tìm thấy ảnh"
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Server error message"
    """
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        user_id = data.get('id')

        if not user_id:
            return jsonify({"error": "Thiếu tham số 'id'"}), 400

        # Truy vấn ảnh mới nhất (ID lớn nhất)
        path_result = exportData(
            sql="SELECT `path` FROM `images` WHERE `id_user` = %s ORDER BY `id` DESC LIMIT 1",
            val=(user_id,),
        )

        if not path_result:
            return jsonify({"error": "Không tìm thấy ảnh"}), 404

        # Nếu kết quả là danh sách, lấy phần tử đầu tiên
        image_path = path_result[0] if isinstance(path_result, list) else path_result

        print(f"Ảnh mới nhất: {image_path}")
        return jsonify({"path": image_path}), 200

    except Exception as e:
        print(f"Lỗi server: {e}")
        return jsonify({"error": str(e)}), 500

@image_bp.route('/uploads/<path:filename>')
def serve_image(filename):
    """
    Serve uploaded image files
    ---
    tags:
      - Image Management
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        example: "123/avatar.jpg"
        description: "Path to the image file relative to uploads folder"
    responses:
      200:
        description: Image file served successfully
        content:
          image/jpeg:
            schema:
              type: string
              format: binary
          image/png:
            schema:
              type: string
              format: binary
          image/gif:
            schema:
              type: string
              format: binary
      404:
        description: Image file not found
    """
    return send_from_directory(UPLOAD_FOLDER, filename)