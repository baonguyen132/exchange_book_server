from flask import Blueprint, request, jsonify
from services.vnpay.vnpay import vnpay
from services.vnpay.settings import *
from datetime import datetime

from services.connectDatabase import importData, exportData

transaction = Blueprint('transaction', __name__)


@transaction.route('/addPoint' , methods=['POST'])
def addPoint():
    """
    Add points for correct answers in quiz/game
    ---
    tags:
      - Transaction Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - idUser
            - countCorrect
          properties:
            idUser:
              type: string
              example: "1"
              description: "User ID to add points"
            countCorrect:
              type: integer
              example: 5
              description: "Number of correct answers (each = 10 points)"
    responses:
      200:
        description: Points added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Đã cộng $50"
            point:
              type: array
              items:
                type: integer
              example: [150]
    """
    data = request.get_json()

    id = data.get('idUser')
    countCorrect = data.get('countCorrect')

    importData(
        sql="UPDATE `users` SET `point` = `point` + %s WHERE `id` = %s",
        val=(countCorrect * 10, id)
    )

    point = exportData(
        sql="SELECT `point` FROM `users` WHERE `id` = %s",
        val=(id,)
    )

    return jsonify({
        "message": f"Đã cộng ${countCorrect * 10}",
        "point": point
    }), 200


@transaction.route('/add-transaction', methods=['POST'])
def add_transaction():
    """
    Add transaction record and update user points
    ---
    tags:
      - Transaction Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - price
            - state
            - id_user
          properties:
            price:
              type: integer
              example: 50000
              description: "Price/amount in VND"
            state:
              type: string
              example: "completed"
              description: "Transaction state"
            id_user:
              type: string
              example: "1"
              description: "User ID for the transaction"
    responses:
      200:
        description: Transaction added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Thêm điểm thành công"
      400:
        description: Transaction failed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error details"
    """
    try:
        data = request.get_json()
        price = int(data.get('price', 0))
        state = data.get('state', '')
        id_user = int(data.get('id_user', 0))
        now = datetime.now()

        if price <= 0 or not state or id_user <= 0:
            return jsonify({"error": "Thiếu hoặc sai dữ liệu đầu vào"}), 400

        # Thêm bản ghi giao dịch
        importData(
            sql="""
                INSERT INTO `transaction`
                (`transaction_date`, `price`, `state`, `id_user`, `created_at`, `updated_at`)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
            """,
            val=(now, price, state, id_user)
        )

        # Cộng điểm cho user
        importData(
            sql="""
                UPDATE `users` 
                SET `point` = `point` + %s 
                WHERE `id` = %s
            """,
            val=(price, id_user)
        )

        return jsonify({"message": "Thêm điểm thành công"}), 200

    except Exception as e:
        print("Lỗi khi thêm giao dịch:", e)
        return jsonify({"error": str(e)}), 400


@transaction.route('/transfer', methods=['POST'])
def transfer():
    """
    Transfer points to multiple users
    ---
    tags:
      - Transaction Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - address
            - point
            - idUser
          properties:
            address:
              type: string
              example: "123 Main St"
              description: "Address of the receivers"
            point:
              type: integer
              example: 100
              description: "Points to give each receiver"
            idUser:
              type: string
              example: "1"
              description: "Sender user ID"
    responses:
      200:
        description: Points transferred successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Chuyển điểm thành công"
            current_points:
              type: integer
              example: 800
              description: "Remaining points of sender"
      400:
        description: Transfer failed
        schema:
          type: object
          properties:
            error:
              type: string
              enum: ["Địa chỉ người nhận không được để trống", "Người gửi không tồn tại", "Danh sách người nhận trống", "Số điểm quá nhỏ để chia", "Không đủ điểm để chuyển"]
              example: "Không đủ điểm để chuyển"
    """
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        point = int(data.get('point', 0))
        id_user_from = data.get('idUser')

        # --- Kiểm tra đầu vào cơ bản ---
        
        if not id_user_from:
            return jsonify({"error": "Thiếu ID người gửi"}), 400
        if point <= 0:
            return jsonify({"error": "Số điểm phải lớn hơn 0"}), 400

        # --- Kiểm tra người gửi có tồn tại không ---
        user_point_data = exportData(
            sql="SELECT `point` FROM `users` WHERE `id` = %s",
            val=(id_user_from,)
        )
        if not user_point_data:
            return jsonify({"error": "Người gửi không tồn tại"}), 400

        current_point = int(user_point_data[0])

        # --- Lấy danh sách người nhận ---
        like_address = f"%{address.lower()}%"
        receivers = exportData(
            sql="""
                SELECT id
                FROM users
                WHERE LOWER(address) LIKE %s
                  AND id <> %s
            """,
            val=(like_address, id_user_from),
            fetch_all=True
        )

        if not receivers:
            return jsonify({"error": "Danh sách người nhận trống"}), 400

        list_id = [receiver[0] for receiver in receivers]

        # --- Kiểm tra đủ điểm để chia ---
        total_transfer = point 
        if current_point < total_transfer:
            return jsonify({"error": "Không đủ điểm để chuyển"}), 400

        # --- Bắt đầu giao dịch ---
        # (Nếu bạn dùng MySQL connector, bạn có thể mở transaction để rollback khi lỗi)
        importData(
            sql="UPDATE `users` SET `point` = `point` - %s WHERE `id` = %s",
            val=(total_transfer, id_user_from)
        )

        for receiver_id in list_id:
            importData(
                sql="UPDATE `users` SET `point` = `point` + %s WHERE `id` = %s",
                val=(int(point / len(list_id)), receiver_id)
            )

        # --- Trả kết quả ---
        return jsonify({
            "message": f"Chuyển điểm thành công đến {len(list_id)} người nhận",
            "current_points": current_point - total_transfer
        }), 200

    except Exception as e:
        print("Error in transfer:", e)
        return jsonify({"error": str(e)}), 400


@transaction.route('/transferOnePerson', methods=['POST'])
def transferOnePerson():
    """
    Transfer points to one specific person
    ---
    tags:
      - Transaction Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - receiverId
            - totalPoint
            - idUser
          properties:
            receiverId:
              type: string
              example: "123-0123456789"
              description: "Receiver ID and CCCD separated by dash (format: id-cccd)"
            totalPoint:
              type: integer
              example: 50
              description: "Points to transfer"
            idUser:
              type: string
              example: "1"
              description: "Sender user ID"
    responses:
      200:
        description: Points transferred successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Chuyển điểm thành công"
            receiverId:
              type: integer
              example: 123
            cccd:
              type: string
              example: "0123456789"
            pointsTransferred:
              type: integer
              example: 50
      400:
        description: Transfer failed
        schema:
          type: object
          properties:
            error:
              type: string
              enum: ["Người nhận không hợp lệ", "Sai định dạng id-cccd", "Số điểm phải > 0", "Người gửi không tồn tại", "Không đủ điểm để chuyển"]
              example: "Không đủ điểm để chuyển"
    """
    try:
        data = request.get_json()
        # ✅ Lấy id người nhận (truyền trực tiếp, không cần list)
        receiver_raw = data.get('receiverId', '')  # ví dụ: "123-0123456789"
        total_point = int(data.get('totalPoint', 0))
        id_user_from = data.get('idUser')

        if not receiver_raw:
            return jsonify({"error": "Người nhận không hợp lệ"}), 400

        # ✅ Tách id và cccd từ receiver_raw
        try:
            receiver_id, cccd = receiver_raw.split('-')
            receiver_id = int(receiver_id)
        except ValueError:
            return jsonify({"error": "Sai định dạng id-cccd"}), 400

        if total_point <= 0:
            return jsonify({"error": "Số điểm phải > 0"}), 400

        # ✅ Kiểm tra điểm hiện tại của người gửi
        user_point_data = exportData(
            sql="SELECT `point` FROM `users` WHERE `id` = %s",
            val=(id_user_from,),
        )

        if not user_point_data:
            return jsonify({"error": "Người gửi không tồn tại"}), 400

        current_point = int(user_point_data[0])

        if current_point < total_point:
            return jsonify({"error": "Không đủ điểm để chuyển"}), 400
        # ✅ Trừ điểm người gửi
        importData(
            sql="UPDATE `users` SET `point` = `point` - %s WHERE `id` = %s",
            val=(total_point, id_user_from)
        )
        # ✅ Cộng điểm cho người nhận
        importData(
            sql="UPDATE `users` SET `point` = `point` + %s WHERE `id` = %s",
            val=(total_point, receiver_id)
        )

        return jsonify({
            "message": "Chuyển điểm thành công",
            "receiverId": receiver_id,
            "cccd": cccd,
            "pointsTransferred": total_point
        }), 200

    except Exception as e:
        print("Lỗi khi chuyển điểm:", e)
        return jsonify({"error": str(e)}), 400
@transaction.route('/create_payment_url', methods=['POST'])
def create_payment_url():
    """
    Create VNPay payment URL
    ---
    tags:
      - Payment Gateway
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: orderId
        in: formData
        type: string
        required: true
        example: "ORDER123456"
        description: "Unique order ID"
      - name: amount
        in: formData
        type: string
        required: true
        example: "100000"
        description: "Payment amount in VND"
    responses:
      200:
        description: Payment URL created successfully
        schema:
          type: string
          example: "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?vnp_Amount=10000000&..."
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
              enum: ["Thiếu orderId hoặc amount", "Amount phải là số"]
              example: "Thiếu orderId hoặc amount"
    """
    order_id = request.form.get('orderId')
    amount = request.form.get('amount')

    if not order_id or not amount:
        return jsonify({'error': 'Thiếu orderId hoặc amount'}), 400

    try:
        amount = int(amount)
    except ValueError:
        return jsonify({'error': 'Amount phải là số'}), 400

    ipaddr = get_client_ip(request)

    vnp = vnpay()
    vnp.requestData['vnp_Version'] = '2.1.0'
    vnp.requestData['vnp_Command'] = 'pay'
    vnp.requestData['vnp_TmnCode'] = VNPAY_TMN_CODE
    vnp.requestData['vnp_Amount'] = amount * 100
    vnp.requestData['vnp_CurrCode'] = 'VND'
    vnp.requestData['vnp_TxnRef'] = order_id
    vnp.requestData['vnp_OrderInfo'] = 'Thanh toan don hang ' + order_id
    vnp.requestData['vnp_OrderType'] = 'other'
    vnp.requestData['vnp_Locale'] = 'vn'
    vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp.requestData['vnp_IpAddr'] = ipaddr
    vnp.requestData['vnp_ReturnUrl'] = VNPAY_RETURN_URL

    payment_url = vnp.get_payment_url(VNPAY_PAYMENT_URL, VNPAY_HASH_SECRET_KEY)

    return payment_url  # trả về plain text URL
@transaction.route('/payment_return')
def payment_return():
    """
    Handle VNPay payment return callback
    ---
    tags:
      - Payment Gateway
    parameters:
      - name: vnp_ResponseCode
        in: query
        type: string
        required: false
        description: "VNPay response code"
      - name: vnp_SecureHash
        in: query
        type: string
        required: false
        description: "VNPay security hash for validation"
      - name: vnp_TxnRef
        in: query
        type: string
        required: false
        description: "Transaction reference (order ID)"
      - name: vnp_Amount
        in: query
        type: string
        required: false
        description: "Transaction amount"
    responses:
      200:
        description: Payment response processed
        schema:
          type: string
          enum: ["00", "invalid", "error"]
          example: "00"
          description: "Response code from VNPay, 'invalid' if validation failed, or 'error' if exception occurred"
    """
    try:
        inputData = request.args.to_dict()
        vnp = vnpay()
        vnp_secure_hash = inputData.pop('vnp_SecureHash', None)

        # Validate response with proper method signature
        vnp.responseData = inputData
        is_valid = vnp.validate_response(VNPAY_HASH_SECRET_KEY)

        if is_valid:
            response_code = inputData.get('vnp_ResponseCode')
            return response_code  # <-- Flutter sẽ bắt response_code này trong WebView
        else:
            return 'invalid'
    except Exception as e:
        print(f"Error in payment_return: {e}")
        return 'error'

def get_client_ip(request):
    if request.headers.getlist("X-Forwarded-For"):
        # Nếu server có reverse proxy (ngrok, nginx, v.v.)
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip