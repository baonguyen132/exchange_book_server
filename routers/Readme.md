# Routers / Các Routes 📡

**API endpoint definitions and handlers for Exchange Book Server**

**Các định nghĩa endpoint API và trình xử lý cho Exchange Book Server**

---

## 📋 Overview / Tổng Quan

This directory contains all Flask Blueprint route handlers that define the API endpoints for the Exchange Book Server. Each router module handles a specific domain of functionality.

Thư mục này chứa tất cả các trình xử lý tuyến Flask Blueprint xác định các endpoint API cho Exchange Book Server. Mỗi mô-đun router xử lý một lĩnh vực chức năng cụ thể.

---

## 📁 Router Files / Các Tệp Router

### 1. `router_user.py` - User Management / Quản Lý Người Dùng

**Purpose:** Handle user authentication, registration, and profile management

**Mục đích:** Xử lý xác thực người dùng, đăng ký và quản lý hồ sơ

#### Endpoints / Các Endpoint:

| Method | Path | Description | Mô Tả |
|--------|------|-------------|-------|
| POST | `/sendOtp` | Send OTP to user email | Gửi OTP đến email người dùng |
| POST | `/login_user` | Authenticate user with email/password | Xác thực người dùng bằng email/mật khẩu |
| POST | `/register_user` | Register new user account | Đăng ký tài khoản người dùng mới |
| POST | `/loadUser` | Get user profile information | Lấy thông tin hồ sơ người dùng |
| POST | `/loadDataUser` | Get detailed user data | Lấy dữ liệu người dùng chi tiết |

#### Key Functions / Các Hàm Chính:

- `sendOtp()` - Send OTP via email with SMTP / Gửi OTP qua email bằng SMTP
- `login_user()` - Verify credentials and return JWT token / Xác minh thông tin đăng nhập và trả về mã JWT
- `register_user()` - Create new user with password hashing / Tạo người dùng mới bằng mã hóa mật khẩu
- `loadUser()` - Retrieve user by email or ID / Lấy người dùng theo email hoặc ID

---

### 2. `router_book.py` - Book Listings / Danh Sách Sách

**Purpose:** Handle book CRUD operations, search, and image management

**Mục đích:** Xử lý các hoạt động CRUD sách, tìm kiếm và quản lý ảnh

#### Endpoints / Các Endpoint:

| Method | Path | Description | Mô Tả |
|--------|------|-------------|-------|
| POST | `/insertBook` | Create new book listing | Tạo danh sách sách mới |
| POST | `/updateBook` | Update book details | Cập nhật chi tiết sách |
| POST | `/deleteBook` | Delete book listing | Xóa danh sách sách |
| POST | `/exportBook` | Get all available books from other users | Lấy tất cả sách có sẵn từ người dùng khác |
| POST | `/exportMyBook` | Get current user's book listings | Lấy danh sách sách của người dùng hiện tại |
| POST | `/upload_image_book` | Upload book cover image | Tải lên ảnh bìa sách |
| POST | `/scan_books` | Search books by name | Tìm kiếm sách theo tên |
| GET | `/public/image_book_client/<filename>` | Serve book image file | Phục vụ tệp ảnh sách |

#### Key Functions / Các Hàm Chính:

- `insertBook()` - Insert new book with validation / Chèn sách mới với xác thực
- `updateBook()` - Update book price, quantity, description / Cập nhật giá, số lượng, mô tả sách
- `deleteBook()` - Delete book and associated image / Xóa sách và ảnh liên quan
- `exportBook()` - Query books from other users with pagination / Truy vấn sách từ người dùng khác có phân trang
- `exportMyBook()` - Get user's own books / Lấy sách của chính người dùng
- `upload_image_book()` - Handle book image upload with secure filename / Xử lý tải lên ảnh sách bằng tên tệp an toàn
- `scan_books()` - Search books by name or type / Tìm kiếm sách theo tên hoặc loại
- `serve_image()` - Serve static book images / Phục vụ ảnh sách tĩnh

#### Database Tables / Bảng Cơ Sở Dữ Liệu:

- `book` - Main book listings table / Bảng danh sách sách chính
- `type_books` - Book categories / Danh mục sách

---

### 3. `router_tyepBook.py` - Book Type Management / Quản Lý Loại Sách

**Purpose:** Manage book categories/types with images

**Mục đích:** Quản lý danh mục/loại sách bằng ảnh

#### Endpoints / Các Endpoint:

| Method | Path | Description | Mô Tả |
|--------|------|-------------|-------|
| POST | `/insertTypeBook` | Create new book type | Tạo loại sách mới |
| POST | `/updateTypeBook` | Update book type info | Cập nhật thông tin loại sách |
| POST | `/deleteTypeBook` | Delete book type | Xóa loại sách |
| GET | `/exportTypeBook/<page>` | Get all book types (paginated) | Lấy tất cả loại sách (phân trang) |
| POST | `/upload_type_image_book` | Upload book type cover image | Tải lên ảnh bìa loại sách |
| GET | `/public/image/<filename>` | Serve type book images | Phục vụ ảnh loại sách |

#### Key Functions / Các Hàm Chính:

- `insertTypeBook()` - Create new book category / Tạo danh mục sách mới
- `updateTypeBook()` - Update category details / Cập nhật chi tiết danh mục
- `deleteTypeBook()` - Delete category / Xóa danh mục
- `exportTypeBook()` - Get paginated list of categories / Lấy danh sách danh mục có phân trang
- `uploadImageBook()` - Upload cover image for category / Tải lên ảnh bìa cho danh mục
- `serve_image()` - Serve static category images / Phục vụ ảnh danh mục tĩnh

#### Database Tables / Bảng Cơ Sở Dữ Liệu:

- `type_books` - Book types/categories / Loại/danh mục sách

---

### 4. `router_cart.py` - Shopping Cart / Giỏ Hàng

**Purpose:** Handle shopping cart operations and order management

**Mục đích:** Xử lý các hoạt động giỏ hàng và quản lý đơn hàng

#### Endpoints / Các Endpoint:

| Method | Path | Description | Mô Tả |
|--------|------|-------------|-------|
| POST | `/insertCart` | Add item to shopping cart | Thêm mục vào giỏ hàng |
| POST | `/export_cart_purchase` | Get items in purchase cart | Lấy mục trong giỏ hàng mua |
| POST | `/export_cart_seller` | Get items in seller cart | Lấy mục trong giỏ hàng bán |
| POST | `/update_state_cart` | Update cart item status | Cập nhật trạng thái mục giỏ hàng |
| POST | `/export_item_cart` | Get specific cart item details | Lấy chi tiết mục giỏ hàng cụ thể |

#### Key Functions / Các Hàm Chính:

- `insertCart()` - Add book to user's cart / Thêm sách vào giỏ hàng của người dùng
- `export_cart_purchase()` - Get items user is buying / Lấy mục người dùng đang mua
- `export_cart_seller()` - Get items user is selling / Lấy mục người dùng đang bán
- `update_state_cart()` - Update cart status (pending, confirmed, shipped, etc.) / Cập nhật trạng thái giỏ hàng
- `export_item_cart()` - Get specific item details / Lấy chi tiết mục cụ thể

#### Database Tables / Bảng Cơ Sở Dữ Liệu:

- `cart` - Shopping cart items / Các mục giỏ hàng

---

### 5. `router_transaction_handle.py` - Transactions & Payments / Giao Dịch & Thanh Toán

**Purpose:** Handle user points, transactions, and VNPay payment integration

**Mục đích:** Xử lý điểm người dùng, giao dịch và tích hợp thanh toán VNPay

#### Endpoints / Các Endpoint:

| Method | Path | Description | Mô Tả |
|--------|------|-------------|-------|
| POST | `/addPoint` | Add points to user account | Thêm điểm vào tài khoản người dùng |
| POST | `/add-transaction` | Record transaction | Ghi lại giao dịch |
| POST | `/transfer` | Transfer points to multiple users | Chuyển điểm cho nhiều người dùng |
| POST | `/transferOnePerson` | Transfer points to single user | Chuyển điểm cho một người dùng |
| POST | `/create_payment_url` | Create VNPay payment URL | Tạo URL thanh toán VNPay |
| GET | `/payment_return` | Handle VNPay payment callback | Xử lý callback thanh toán VNPay |

#### Key Functions / Các Hàm Chính:

- `addPoint()` - Add points for correct answers / Thêm điểm cho câu trả lời đúng
- `add_transaction()` - Record transaction in database / Ghi lại giao dịch trong cơ sở dữ liệu
- `transfer()` - Distribute points equally to multiple users / Phân phối điểm bằng nhau cho nhiều người dùng
- `transferOnePerson()` - Transfer points to specific user / Chuyển điểm cho người dùng cụ thể
- `create_payment_url()` - Generate VNPay payment link / Tạo liên kết thanh toán VNPay
- `payment_return()` - Verify and process VNPay callback / Xác minh và xử lý callback VNPay

#### Database Tables / Bảng Cơ Sở Dữ Liệu:

- `transactions` - Transaction history / Lịch sử giao dịch
- `users` - User points balance / Số dư điểm người dùng

---

### 6. `router_image_handle.py` - User Images / Ảnh Người Dùng

**Purpose:** Handle user avatar uploads and image management

**Mục đích:** Xử lý tải lên ảnh đại diện người dùng và quản lý ảnh

#### Endpoints / Các Endpoint:

| Method | Path | Description | Mô Tả |
|--------|------|-------------|-------|
| POST | `/upload_file` | Upload user avatar image | Tải lên ảnh đại diện người dùng |
| POST | `/export_image_avata` | Get latest user avatar | Lấy ảnh đại diện người dùng mới nhất |
| GET | `/uploads/<filename>` | Serve user image file | Phục vụ tệp ảnh người dùng |

#### Key Functions / Các Hàm Chính:

- `upload_file()` - Handle avatar upload with security / Xử lý tải lên ảnh đại diện với bảo mật
- `export_image_avata()` - Retrieve latest user avatar path / Lấy đường dẫn ảnh đại diện mới nhất
- `serve_image()` - Serve static user images / Phục vụ ảnh người dùng tĩnh

#### Database Tables / Bảng Cơ Sở Dữ Liệu:

- `users` - User avatar path / Đường dẫn ảnh đại diện người dùng

---

## 🔧 Router Configuration / Cấu Hình Router

### Registering Routers / Đăng Ký Routers

In `serve.py`, all routers are registered with the Flask app / Trong `serve.py`, tất cả các router được đăng ký với ứng dụng Flask:

```python
from routers.router_user import user_bp
from routers.router_book import book_bp
from routers.router_tyepBook import type_book_bp
from routers.router_cart import cart_bp
from routers.router_transaction_handle import transaction_bp
from routers.router_image_handle import image_bp

# Register blueprints / Đăng ký blueprints
app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(type_book_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(image_bp)
```

---

## 🔐 Authentication / Xác Thực

### OTP Email Verification / Xác Minh Email OTP

1. User requests OTP / Người dùng yêu cầu OTP
2. Server generates random OTP / Server tạo OTP ngẫu nhiên
3. OTP sent via SMTP to user email / OTP được gửi qua SMTP đến email người dùng
4. User verifies OTP / Người dùng xác minh OTP
5. User account created / Tài khoản người dùng được tạo

### JWT Token / Mã JWT

- Issued on successful login / Được cấp khi đăng nhập thành công
- Include in `Authorization: Bearer <token>` header / Bao gồm trong tiêu đề `Authorization: Bearer <token>`
- Verify token for protected routes / Xác minh mã token cho các tuyến được bảo vệ

---

## 💾 Database Access / Truy Cập Cơ Sở Dữ Liệu

All routers use the `connectDatabase.py` service for database operations / Tất cả các router sử dụng dịch vụ `connectDatabase.py` để hoạt động cơ sở dữ liệu:

```python
from services.connectDatabase import importData, exportData

# Insert data / Chèn dữ liệu
importData(
    sql="INSERT INTO users (email, password) VALUES (%s, %s)",
    val=("user@email.com", "hashed_password")
)

# Select data / Chọn dữ liệu
users = exportData(
    sql="SELECT * FROM users WHERE email = %s",
    val=("user@email.com",),
    fetch_all=False
)
```

---

## 📤 File Upload Handling / Xử Lý Tải Lên Tệp

### Security Measures / Các Biện Pháp Bảo Mật

- ✅ `secure_filename()` to prevent path traversal / Để ngăn chặn traversal đường dẫn
- ✅ Whitelist allowed file extensions / Danh sách cho phép các phần mở rộng tệp
- ✅ Generate unique filenames with UUID + timestamp / Tạo tên tệp duy nhất bằng UUID + dấu thời gian
- ✅ Store relative paths in database / Lưu trữ đường dẫn tương đối trong cơ sở dữ liệu
- ✅ Validate file size / Xác thực kích thước tệp

### Upload Folders / Các Thư Mục Tải Lên

```
public/
├── image/                  # Book type covers / Bìa loại sách
├── image_book_client/      # User uploaded books / Sách do người dùng tải lên
└── uploads/                # User avatars / Ảnh đại diện người dùng
```

---

## 🧪 Testing / Thử Nghiệm

### Using Postman / Sử dụng Postman

1. Import collection / Nhập bộ sưu tập
2. Set environment variables / Đặt biến môi trường
3. Test each endpoint / Kiểm tra từng endpoint
4. Verify request/response format / Xác minh định dạng yêu cầu/phản hồi

### Using cURL / Sử dụng cURL

```bash
# Register user / Đăng ký người dùng
curl -X POST http://localhost:5000/register_user \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}'

# Add book / Thêm sách
curl -X POST http://localhost:5000/insertBook \
  -H "Content-Type: application/json" \
  -d '{"id_user":1,"id_type_book":1,"price":45000}'
```

---

## 🔗 API Documentation / Tài Liệu API

Complete API documentation available at: / Tài liệu API đầy đủ có sẵn tại:

```
http://localhost:5000/apidocs/
```

Interactive Swagger UI with:
- ✅ All endpoints documented / Tất cả các endpoint được ghi chép
- ✅ Request/response examples / Ví dụ yêu cầu/phản hồi
- ✅ Parameter descriptions / Mô tả tham số
- ✅ Try it out feature / Tính năng thử nó

---

## 📝 Notes / Ghi Chú

- All endpoints require proper error handling / Tất cả các endpoint yêu cầu xử lý lỗi thích hợp
- Return consistent JSON responses / Trả về các phản hồi JSON nhất quán
- Validate all input parameters / Xác thực tất cả các tham số đầu vào
- Use database transactions for complex operations / Sử dụng giao dịch cơ sở dữ liệu cho các hoạt động phức tạp
- Log important operations / Ghi nhật ký các hoạt động quan trọng

---

**Last Updated:** October 2024 / Cập nhật lần cuối: Tháng 10 năm 2024