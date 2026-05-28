# Exchange Book Server 📚

**A comprehensive Flask-based REST API server for peer-to-peer book exchange platform**

**Một máy chủ REST API toàn diện dựa trên Flask cho nền tảng trao đổi sách ngang hàng**

---

## 📋 Table of Contents / Mục Lục

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Features](#features)
- [Database Schema](#database-schema)

---

## 🎯 Project Overview / Tổng Quan Dự Án

Exchange Book Server is a REST API backend for a mobile application that enables users to:
- **Buy and sell used books** peer-to-peer
- **Manage book inventory** with AI-powered image recognition
- **Process payments** through VNPay gateway
- **Transfer points** between users
- **Upload and manage** book cover images

Exchange Book Server là backend REST API cho ứng dụng di động cho phép người dùng:
- **Mua và bán sách cũ** ngang hàng
- **Quản lý kho sách** với nhận dạng hình ảnh được hỗ trợ bởi AI
- **Xử lý thanh toán** thông qua cổng VNPay
- **Chuyển điểm** giữa các người dùng
- **Tải lên và quản lý** hình ảnh bìa sách

---

## 📁 Project Structure / Cấu Trúc Dự Án

```
exchange_book_server/
├── routers/                          # API route handlers / Xử lý routes API
│   ├── router_user.py               # User management endpoints / Endpoints quản lý người dùng
│   ├── router_book.py               # Book listing endpoints / Endpoints liệt kê sách
│   ├── router_tyepBook.py           # Book type management / Quản lý loại sách
│   ├── router_cart.py               # Shopping cart endpoints / Endpoints giỏ hàng
│   ├── router_transaction_handle.py # Transaction & payment / Giao dịch và thanh toán
│   ├── router_image_handle.py       # Image upload & serving / Upload ảnh và cung cấp dịch vụ
│   └── Readme                       # Router documentation / Tài liệu routers
│
├── services/                         # Business logic & utilities / Logic kinh doanh & tiện ích
│   ├── connectDatabase.py           # Database connection manager / Quản lý kết nối cơ sở dữ liệu
│   ├── AI/                          # AI processing modules / Các mô-đun xử lý AI
│   │   ├── scan_image.py            # Text recognition from images / Nhận dạng văn bản từ ảnh
│   │   ├── scan_book.py             # Book classification AI / AI phân loại sách
│   │   ├── scan/                    # AI output folder / Thư mục đầu ra AI
│   │   └── cropped/                 # Cropped image cache / Bộ nhớ đệm ảnh cắt
│   └── Readme                       # Services documentation / Tài liệu dịch vụ
│
├── public/                           # Static files / Các tệp tĩnh
│   ├── image/                       # Book type cover images / Ảnh bìa loại sách
│   └── image_book_client/           # User uploaded book images / Ảnh sách do người dùng tải lên
│
├── serve.py                         # Main Flask application / Ứng dụng Flask chính
├── requirements.txt                 # Python dependencies / Các phụ thuộc Python
├── .env                             # Environment variables / Biến môi trường
├── docker-compose.yml               # Docker configuration / Cấu hình Docker
└── README.md                        # This file / Tệp này
```

---

## 🚀 Installation / Cài Đặt

### Prerequisites / Điều Kiện Tiên Quyết

- Python 3.11+
- MySQL 8.0+ (or use Docker)
- pip or conda

### Step 1: Clone Repository / Bước 1: Clone Repository

```bash
git clone <repository-url>
cd exchange_book_server
```

### Step 2: Create Virtual Environment / Bước 2: Tạo Virtual Environment

```bash
python -m venv venv

# On Windows / Trên Windows
venv\Scripts\activate

# On macOS/Linux / Trên macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies / Bước 3: Cài Đặt Các Phụ Thuộc

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment / Bước 4: Cấu Hình Môi Trường

Create a `.env` file in the root directory / Tạo tệp `.env` trong thư mục gốc:

```env
# MySQL Configuration / Cấu hình MySQL
DB_HOST=localhost
DB_USER=exchange_user
DB_PASSWORD=exchange_pass
DB_NAME=exchange_book

# Flask Configuration / Cấu hình Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# VNPay Configuration / Cấu hình VNPay
VNPAY_TMN_CODE=your-vnpay-code
VNPAY_HASH_SECRET_KEY=your-vnpay-secret
VNPAY_API_URL=https://sandbox.vnpayment.vn

# Email Configuration / Cấu hình Email
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-email-password
```

### Step 5: Setup Database / Bước 5: Thiết Lập Cơ Sở Dữ Liệu

```bash
# Using Docker / Sử dụng Docker
docker-compose up -d

# Or manually import SQL schema / Hoặc nhập sơ đồ SQL thủ công
mysql -u exchange_user -p exchange_book < database.sql
```

### Step 6: Run Server / Bước 6: Chạy Server

```bash
python serve.py
```

Server will start at `http://localhost:5000` / Server sẽ khởi động tại `http://localhost:5000`

---

## ⚙️ Configuration / Cấu Hình

### Environment Variables / Biến Môi Trường

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DB_HOST` | MySQL server host | Yes | localhost |
| `DB_USER` | MySQL username | Yes | exchange_user |
| `DB_PASSWORD` | MySQL password | Yes | exchange_pass |
| `DB_NAME` | Database name | Yes | exchange_book |
| `FLASK_ENV` | Flask environment | No | production |
| `FLASK_DEBUG` | Debug mode | No | False |
| `SECRET_KEY` | Flask secret key | Yes | - |
| `VNPAY_TMN_CODE` | VNPay merchant code | Yes | - |
| `VNPAY_HASH_SECRET_KEY` | VNPay secret key | Yes | - |

### Database Configuration / Cấu Hình Cơ Sở Dữ Liệu

**Using Docker Compose / Sử dụng Docker Compose:**

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: exchange_book
      MYSQL_USER: exchange_user
      MYSQL_PASSWORD: exchange_pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

---

## 📡 API Endpoints / Các Endpoint API

### 🔐 Authentication / Xác Thực (User Management)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sendOtp` | Send OTP to email / Gửi OTP đến email |
| POST | `/login_user` | User login / Đăng nhập người dùng |
| POST | `/register_user` | Register new user / Đăng ký người dùng mới |
| POST | `/loadUser` | Get user profile / Lấy hồ sơ người dùng |

### 📚 Book Management / Quản Lý Sách

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/insertBook` | Create book listing / Tạo danh sách sách |
| POST | `/exportBook` | Get available books / Lấy sách có sẵn |
| POST | `/exportMyBook` | Get user's books / Lấy sách của người dùng |
| POST | `/updateBook` | Update book listing / Cập nhật danh sách sách |
| POST | `/deleteBook` | Delete book listing / Xóa danh sách sách |
| POST | `/upload_image_book` | Upload book image / Tải lên ảnh sách |
| GET | `/public/image_book_client/<filename>` | Serve book image / Phục vụ ảnh sách |

### 📖 Book Type Management / Quản Lý Loại Sách

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/insertTypeBook` | Create book type / Tạo loại sách |
| POST | `/updateTypeBook` | Update book type / Cập nhật loại sách |
| POST | `/deleteTypeBook` | Delete book type / Xóa loại sách |
| GET | `/exportTypeBook/<page>` | Get book types (paginated) / Lấy loại sách (phân trang) |
| POST | `/upload_type_image_book` | Upload book type cover / Tải lên bìa loại sách |

### 🛒 Shopping Cart / Giỏ Hàng

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/insertCart` | Add item to cart / Thêm mục vào giỏ hàng |
| POST | `/export_cart_purchase` | Get purchase cart / Lấy giỏ hàng mua |
| POST | `/export_cart_seller` | Get seller cart / Lấy giỏ hàng bán |
| POST | `/update_state_cart` | Update cart status / Cập nhật trạng thái giỏ hàng |

### 💰 Transaction & Payment / Giao Dịch & Thanh Toán

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/addPoint` | Add points to user / Thêm điểm cho người dùng |
| POST | `/add-transaction` | Create transaction / Tạo giao dịch |
| POST | `/transfer` | Transfer points to multiple users / Chuyển điểm cho nhiều người |
| POST | `/transferOnePerson` | Transfer points to one user / Chuyển điểm cho một người |
| POST | `/create_payment_url` | Create VNPay payment URL / Tạo URL thanh toán VNPay |
| GET | `/payment_return` | VNPay payment callback / Callback thanh toán VNPay |

### 🖼️ Image Management / Quản Lý Ảnh

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload_file` | Upload user avatar / Tải lên ảnh đại diện người dùng |
| POST | `/export_image_avata` | Get user avatar / Lấy ảnh đại diện người dùng |
| GET | `/uploads/<filename>` | Serve user image / Phục vụ ảnh người dùng |

---

## ✨ Features / Các Tính Năng

### 🔐 Security Features / Các Tính Năng Bảo Mật

- ✅ JWT token authentication / Xác thực mã JWT
- ✅ OTP email verification / Xác minh OTP qua email
- ✅ Secure file upload handling / Xử lý tải lên tệp an toàn
- ✅ SQL injection prevention / Ngăn chặn SQL injection
- ✅ CORS enabled / CORS được bật
- ✅ Password hashing / Mã hóa mật khẩu

### 💳 Payment Processing / Xử Lý Thanh Toán

- ✅ VNPay integration / Tích hợp VNPay
- ✅ Transaction history / Lịch sử giao dịch
- ✅ Point system / Hệ thống điểm
- ✅ Multi-user transfers / Chuyển đổi nhiều người dùng

### 🤖 AI Features / Các Tính Năng AI

- ✅ Book type classification / Phân loại loại sách
- ✅ Text recognition from covers / Nhận dạng văn bản từ bìa
- ✅ Grade level detection / Phát hiện mức lớp
- ✅ Subject extraction / Trích xuất môn học

### 📱 API Documentation / Tài Liệu API

- ✅ Swagger UI at `/apidocs/` / Swagger UI tại `/apidocs/`
- ✅ Complete endpoint documentation / Tài liệu endpoint hoàn chỉnh
- ✅ Interactive API testing / Kiểm tra API tương tác
- ✅ Request/response examples / Ví dụ yêu cầu/phản hồi

---

## 🗄️ Database Schema / Sơ Đồ Cơ Sở Dữ Liệu

### Main Tables / Các Bảng Chính

```sql
-- Users table / Bảng người dùng
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  full_name VARCHAR(255),
  phone VARCHAR(20),
  avatar_path VARCHAR(500),
  points INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book types table / Bảng loại sách
CREATE TABLE type_books (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name_book VARCHAR(255),
  type_book VARCHAR(255),
  price DECIMAL(10,2),
  image VARCHAR(500),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Books table / Bảng sách
CREATE TABLE book (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_type_book INT,
  id_user INT,
  date_purchase DATE,
  price DECIMAL(10,2),
  description TEXT,
  image VARCHAR(500),
  status INT DEFAULT 1,
  quantity INT DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_type_book) REFERENCES type_books(id),
  FOREIGN KEY (id_user) REFERENCES users(id)
);

-- Shopping cart table / Bảng giỏ hàng
CREATE TABLE cart (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_user INT,
  id_book INT,
  quantity INT DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_user) REFERENCES users(id),
  FOREIGN KEY (id_book) REFERENCES book(id)
);

-- Transactions table / Bảng giao dịch
CREATE TABLE transactions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_user INT,
  point INT,
  price DECIMAL(10,2),
  state VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_user) REFERENCES users(id)
);
```

---

## 🔧 Technologies / Công Nghệ

### Backend Stack / Stack Backend

- **Framework:** Flask 2.x
- **Database:** MySQL 8.0
- **ORM:** MySQL Connector
- **Authentication:** JWT + OTP
- **Payment:** VNPay API
- **Image Processing:** PIL, OpenCV, YOLO
- **Text Recognition:** EasyOCR
- **API Documentation:** Flasgger (Swagger)
- **Email:** SMTP
- **File Upload:** Werkzeug

### Dependencies / Các Phụ Thuộc

See `requirements.txt` for complete list / Xem `requirements.txt` để biết danh sách đầy đủ

---

## 📝 Usage Examples / Ví Dụ Sử Dụng

### Register User / Đăng Ký Người Dùng

```bash
curl -X POST http://localhost:5000/register_user \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'
```

### Upload Book Image / Tải Lên Ảnh Sách

```bash
curl -X POST http://localhost:5000/upload_image_book \
  -F "image=@book_cover.jpg"
```

### Create Book Listing / Tạo Danh Sách Sách

```bash
curl -X POST http://localhost:5000/insertBook \
  -H "Content-Type: application/json" \
  -d '{
    "id_type_book": 1,
    "id_user": 123,
    "date_purchase": "2024-01-15",
    "price": 45000,
    "description": "Used book in good condition",
    "image": "public/image_book_client/book_123.jpg",
    "status": 1,
    "quantity": 1
  }'
```

---

## 🚨 Troubleshooting / Xử Lý Sự Cố

### Database Connection Error / Lỗi Kết Nối Cơ Sở Dữ Liệu

**Problem:** `Can't connect to MySQL server`

**Solution:** 
- Verify MySQL is running / Xác minh MySQL đang chạy
- Check database credentials in `.env` / Kiểm tra thông tin đăng nhập cơ sở dữ liệu trong `.env`
- Ensure database exists / Đảm bảo cơ sở dữ liệu tồn tại

### File Upload Error / Lỗi Tải Lên Tệp

**Problem:** `Permission denied` when saving files

**Solution:**
- Check folder permissions / Kiểm tra quyền thư mục
- Create `public/` and `uploads/` folders manually / Tạo thư mục `public/` và `uploads/` thủ công
- Run `chmod 777 public/` (on Linux/Mac) / Chạy `chmod 777 public/` (trên Linux/Mac)

### VNPay Integration Error / Lỗi Tích Hợp VNPay

**Problem:** `Invalid VNPay credentials`

**Solution:**
- Verify VNPAY_TMN_CODE and VNPAY_HASH_SECRET_KEY / Xác minh mã và khóa bí mật VNPay
- Use sandbox URL for testing / Sử dụng URL hộp cát để kiểm tra
- Check payment status callback / Kiểm tra callback trạng thái thanh toán

---

## 📞 Support & Contact / Hỗ Trợ & Liên Hệ

For issues, questions, or contributions:
- **Email:** support@exchangebook.com
- **GitHub Issues:** [Create an issue](https://github.com/exchangebook/server/issues)
- **Documentation:** [Full API docs](http://localhost:5000/apidocs)

Để được hỗ trợ, đặt câu hỏi hoặc đóng góp:
- **Email:** support@exchangebook.com
- **GitHub Issues:** [Tạo vấn đề](https://github.com/exchangebook/server/issues)
- **Tài liệu:** [Tài liệu API đầy đủ](http://localhost:5000/apidocs)

---

## 📄 License / Giấy Phép

This project is licensed under the MIT License - see the LICENSE file for details.

Dự án này được cấp phép theo Giấy phép MIT - xem tệp LICENSE để biết chi tiết.

---

**Last Updated:** October 2024 / Cập nhật lần cuối: Tháng 10 năm 2024

**Version:** 1.0.0