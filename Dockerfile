FROM python:3.11-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy file requirements trước để tận dụng cache layer
COPY requirements.txt .

# Cài đặt thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code dự án vào container
COPY . .

# Expose port cho Flask (mặc định 5000)
EXPOSE 5000

# Chạy app
CMD ["python", "serve.py"] 