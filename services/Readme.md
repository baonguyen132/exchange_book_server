# Services / Các Dịch Vụ 🔧

**Business logic, utilities, and service modules for Exchange Book Server**

**Logic kinh doanh, tiện ích và các mô-đun dịch vụ cho Exchange Book Server**

---

## 📋 Overview / Tổng Quan

This directory contains core business logic and utility services that support the API routers. Each service module handles a specific domain of functionality.

Thư mục này chứa logic kinh doanh cốt lõi và các dịch vụ tiện ích hỗ trợ các router API. Mỗi mô-đun dịch vụ xử lý một lĩnh vực chức năng cụ thể.

---

## 📁 Service Files / Các Tệp Dịch Vụ

### 1. `connectDatabase.py` - Database Connection Manager / Quản Lý Kết Nối Cơ Sở Dữ Liệu

**Purpose:** Handle all database connections and queries

**Mục đích:** Xử lý tất cả các kết nối và truy vấn cơ sở dữ liệu

#### Key Functions / Các Hàm Chính:

```python
def importData(sql, val):
    """
    Execute INSERT, UPDATE, DELETE operations
    
    Thực thi các hoạt động INSERT, UPDATE, DELETE
    
    Args:
        sql (str): SQL query / Truy vấn SQL
        val (tuple): Parameter values / Giá trị tham số
        
    Returns:
        bool: True if successful / True nếu thành công
    """
    pass

def exportData(sql, val, fetch_all=False):
    """
    Execute SELECT operations (read-only)
    
    Thực thi các hoạt động SELECT (chỉ đọc)
    
    Args:
        sql (str): SQL query / Truy vấn SQL
        val (tuple): Parameter values / Giá trị tham số
        fetch_all (bool): Get all rows or single row / Lấy tất cả hàng hoặc hàng duy nhất
        
    Returns:
        dict/list: Query results / Kết quả truy vấn
    """
    pass
```

#### Database Configuration / Cấu Hình Cơ Sở Dữ Liệu

```python
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "exchange_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "exchange_pass")
DB_NAME = os.getenv("DB_NAME", "exchange_book")
```

#### Connection Retry Logic / Logic Thử Lại Kết Nối

- Attempts connection 10 times / Cố gắng kết nối 10 lần
- Waits 5 seconds between attempts / Chờ 5 giây giữa các lần thử
- Useful for Docker startup / Hữu ích cho khởi động Docker

#### Error Handling / Xử Lý Lỗi

- ✅ Connection errors / Lỗi kết nối
- ✅ Query syntax errors / Lỗi cú pháp truy vấn
- ✅ Data constraint violations / Vi phạm ràng buộc dữ liệu
- ✅ Transaction rollback / Hoàn tác giao dịch

---

### 2. `AI/` - Artificial Intelligence Modules / Các Mô-đun Trí Tuệ Nhân Tạo

**Purpose:** AI-powered image analysis and text recognition

**Mục đích:** Phân tích ảnh và nhận dạng văn bản được hỗ trợ bởi AI

#### Directory Structure / Cấu Trúc Thư Mục

```
AI/
├── scan_image.py          # Text recognition from book covers / Nhận dạng văn bản từ bìa sách
├── scan_book.py           # Book classification / Phân loại sách
├── model_label_number.pt  # YOLO model for labels/grades / Mô hình YOLO cho nhãn/lớp
├── model_book.pt          # YOLO model for book types / Mô hình YOLO cho loại sách
├── scan/                  # Output folder for predicted images / Thư mục đầu ra cho ảnh được dự đoán
└── cropped/               # Folder for cropped label images / Thư mục cho ảnh nhãn cắt
    └── label/            # Label crops / Cắt nhãn
```

#### 2.1 `scan_image.py` - Text Recognition / Nhận Dạng Văn Bản

**Purpose:** Extract text from book cover images using AI

**Mục đích:** Trích xuất văn bản từ ảnh bìa sách bằng AI

##### Key Functions / Các Hàm Chính:

```python
def recognize_text_easyocr(image, resize_factor=3):
    """
    Recognize text from image using EasyOCR
    
    Nhận dạng văn bản từ ảnh bằng EasyOCR
    
    Process:
    1. Convert to grayscale / Chuyển đổi sang tỷ độ xám
    2. Apply Gaussian blur / Áp dụng mờ Gaussian
    3. Binary thresholding (Otsu) / Ngưỡng nhị phân (Otsu)
    4. Invert colors if needed / Đảo ngược màu nếu cần
    5. Resize 3-4x for better recognition / Thay đổi kích thước 3-4x để nhận dạng tốt hơn
    6. EasyOCR recognition / Nhận dạng EasyOCR
    
    Args:
        image (PIL.Image): Input image / Ảnh đầu vào
        resize_factor (int): Resize multiplier (default 3) / Hệ số thay đổi kích thước (mặc định 3)
        
    Returns:
        str: Recognized text / Văn bản được nhận dạng
    """
    pass

def scans(file_path):
    """
    Analyze book cover and extract information
    
    Phân tích bìa sách và trích xuất thông tin
    
    Returns:
        dict: {
            'label': str (detected subject / môn học được phát hiện),
            'number': str (detected grade / lớp được phát hiện)
        }
    """
    pass
```

##### Technologies Used / Công Nghệ Được Sử Dụng:

- **YOLO v8:** Object detection for book labels / Phát hiện đối tượng cho nhãn sách
- **EasyOCR:** Text recognition in multiple languages / Nhận dạng văn bản bằng nhiều ngôn ngữ
- **OpenCV:** Image processing / Xử lý ảnh
- **PIL (Pillow):** Image manipulation / Thao tác ảnh

##### Output / Đầu Ra:

```python
{
    'label': 'Toán học',           # Book subject / Môn học
    'number': '12'                 # Grade level / Cấp lớp
}
```

---

#### 2.2 `scan_book.py` - Book Classification / Phân Loại Sách

**Purpose:** Classify book types from cover images

**Mục đích:** Phân loại loại sách từ ảnh bìa

##### Key Functions / Các Hàm Chính:

```python
def scan_book(file_path):
    """
    Classify book type from image using YOLO
    
    Phân loại loại sách từ ảnh bằng YOLO
    
    Args:
        file_path (str): Path to book image / Đường dẫn đến ảnh sách
        
    Returns:
        str: Detected book type / Loại sách được phát hiện
             (e.g., 'textbook', 'fiction', 'reference')
             (ví dụ: 'sách giáo khoa', 'tiểu thuyết', 'sách tham khảo')
    """
    pass
```

##### Process / Quy Trình:

1. Load YOLO model / Tải mô hình YOLO
2. Run inference on image / Chạy suy luận trên ảnh
3. Get prediction with highest confidence / Lấy dự đoán có độ tin cậy cao nhất
4. Save predicted image / Lưu ảnh được dự đoán
5. Return classification / Trả về phân loại

##### Output Folder / Thư Mục Đầu Ra:

```
AI/scan_book/
├── book_image_1.jpg (predicted)
├── book_image_2.jpg (predicted)
└── ...
```

---

#### 2.3 Model Files / Các Tệp Mô Hình

##### `model_label_number.pt` - Label & Grade Detection

- **Training Data:** Book covers with label/grade annotations / Bìa sách với chú thích nhãn/lớp
- **Classes:** Subject names (Toán, Văn, Anh, ...) and grades (1-12) / Tên môn học và lớp (1-12)
- **Input Size:** 640x640 / 640x640
- **Confidence Threshold:** 0.5 / 0.5

##### `model_book.pt` - Book Type Classification

- **Training Data:** Various book types / Các loại sách khác nhau
- **Classes:** Textbook, Fiction, Reference, etc. / Sách giáo khoa, Tiểu thuyết, Tham khảo, v.v.
- **Input Size:** 640x640 / 640x640
- **Confidence Threshold:** 0.5 / 0.5

---

## 🔧 Configuration / Cấu Hình

### Environment Variables / Biến Môi Trường

```env
# Database / Cơ Sở Dữ Liệu
DB_HOST=localhost
DB_USER=exchange_user
DB_PASSWORD=exchange_pass
DB_NAME=exchange_book

# AI Models / Mô Hình AI
AI_MODEL_PATH=./services/AI/
AI_CONFIDENCE_THRESHOLD=0.5

# Email Configuration / Cấu Hình Email
EMAIL_ADDRESS=noreply@exchangebook.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

---

## 💾 Database Schema / Sơ Đồ Cơ Sở Dữ Liệu

### Key Tables / Các Bảng Chính:

#### `users` - User Accounts / Tài Khoản Người Dùng

```sql
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  phone VARCHAR(20),
  avatar_path VARCHAR(500),
  points INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `type_books` - Book Categories / Danh Mục Sách

```sql
CREATE TABLE type_books (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name_book VARCHAR(255) UNIQUE,
  type_book VARCHAR(255),
  price DECIMAL(10,2),
  image VARCHAR(500),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `book` - Book Listings / Danh Sách Sách

```sql
CREATE TABLE book (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_type_book INT NOT NULL,
  id_user INT NOT NULL,
  date_purchase DATE,
  price DECIMAL(10,2),
  description TEXT,
  image VARCHAR(500),
  status INT DEFAULT 1 (1=available, 0=sold),
  quantity INT DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (id_type_book) REFERENCES type_books(id),
  FOREIGN KEY (id_user) REFERENCES users(id)
);
```

#### `cart` - Shopping Cart / Giỏ Hàng

```sql
CREATE TABLE cart (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_user INT NOT NULL,
  id_book INT NOT NULL,
  quantity INT DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_user) REFERENCES users(id),
  FOREIGN KEY (id_book) REFERENCES book(id)
);
```

#### `transactions` - Transaction Records / Bản Ghi Giao Dịch

```sql
CREATE TABLE transactions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_user INT NOT NULL,
  point INT,
  price DECIMAL(10,2),
  state VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_user) REFERENCES users(id)
);
```

---

## 🔐 Security Practices / Thực Tiễn Bảo Mật

### Database Security / Bảo Mật Cơ Sở Dữ Liệu

- ✅ **Prepared Statements:** Prevent SQL injection / Ngăn chặn SQL injection
- ✅ **Connection Pooling:** Reuse connections / Tái sử dụng kết nối
- ✅ **Timeout Management:** Prevent hanging connections / Ngăn chặn kết nối bị treo
- ✅ **Error Logging:** Log but don't expose sensitive info / Ghi nhật ký nhưng không tiếp lộ thông tin nhạy cảm

### File Upload Security / Bảo Mật Tải Lên Tệp

- ✅ **Secure Filenames:** Remove path traversal characters / Loại bỏ ký tự traversal đường dẫn
- ✅ **Type Validation:** Whitelist allowed extensions / Danh sách cho phép các phần mở rộng
- ✅ **Size Limits:** Restrict file sizes / Giới hạn kích thước tệp
- ✅ **Virus Scanning:** Optional antivirus integration / Tích hợp antivirus tùy chọn

### AI Security / Bảo Mật AI

- ✅ **Model Validation:** Verify model integrity / Xác minh tính toàn vẹn của mô hình
- ✅ **Rate Limiting:** Limit AI processing requests / Giới hạn yêu cầu xử lý AI
- ✅ **Timeout Protection:** Prevent long-running processes / Ngăn chặn các quy trình chạy lâu dài
- ✅ **Resource Cleanup:** Remove temporary files / Xóa tệp tạm thời

---

## 🧪 Testing / Thử Nghiệm

### Database Connection Test / Kiểm Tra Kết Nối Cơ Sở Dữ Liệu

```python
from services.connectDatabase import exportData

# Test query / Truy vấn kiểm tra
result = exportData(
    sql="SELECT * FROM users LIMIT 1",
    val=(),
    fetch_all=False
)
print(f"Connection successful: {result}")
```

### AI Module Test / Kiểm Tra Mô-đun AI

```python
from services.AI.scan_image import scans

# Test with image / Kiểm tra bằng ảnh
result = scans("path/to/test/image.jpg")
print(f"AI Result: {result}")
```

---

## 📊 Performance Optimization / Tối Ưu Hóa Hiệu Suất

### Database Optimization / Tối Ưu Hóa Cơ Sở Dữ Liệu

- ✅ **Indexes:** Create indexes on frequently queried columns / Tạo chỉ mục trên các cột được truy vấn thường xuyên
- ✅ **Query Caching:** Cache common queries / Bộ nhớ đệm các truy vấn phổ biến
- ✅ **Batch Operations:** Use bulk insert/update / Sử dụng chèn/cập nhật hàng loạt
- ✅ **Connection Pooling:** Reuse connections / Tái sử dụng kết nối

### AI Performance / Hiệu Suất AI

- ✅ **Model Caching:** Load model once / Tải mô hình một lần
- ✅ **Batch Processing:** Process multiple images / Xử lý nhiều ảnh
- ✅ **GPU Acceleration:** Use GPU if available / Sử dụng GPU nếu có
- ✅ **Image Resizing:** Downscale before processing / Giảm quy mô trước khi xử lý

---

## 📝 Error Handling / Xử Lý Lỗi

### Common Errors / Lỗi Phổ Biến

| Error | Cause | Solution |
|-------|-------|----------|
| `mysql.connector.Error` | Database connection failed | Check DB credentials / Kiểm tra thông tin đăng nhập DB |
| `FileNotFoundError` | Model file not found | Verify model path / Xác minh đường dẫn mô hình |
| `OCR Error` | EasyOCR failed | Check image quality / Kiểm tra chất lượng ảnh |
| `YOLO Error` | Model inference failed | Retry with different image / Thử lại bằng ảnh khác |

---

## 🚀 Future Enhancements / Những Nâng Cao Trong Tương Lai

- [ ] Database migration tool / Công cụ di chuyển cơ sở dữ liệu
- [ ] Advanced caching layer / Lớp bộ nhớ đệm nâng cao
- [ ] Multi-language support / Hỗ trợ đa ngôn ngữ
- [ ] Real-time notifications / Thông báo thực tế
- [ ] Analytics dashboard / Bảng điều khiển phân tích
- [ ] Improved AI models / Mô hình AI cải tiến

---

**Last Updated:** October 2024 / Cập nhật lần cuối: Tháng 10 năm 2024

**Version:** 1.0.0