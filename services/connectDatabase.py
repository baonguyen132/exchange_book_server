import mysql.connector
from mysql.connector import Error
import warnings
import os
import time
import dotenv

warnings.filterwarnings("ignore")

dotenv.load_dotenv()

# Các biến môi trường
DB_HOST = os.getenv("DB_HOST", "mysql-db")
DB_USER = os.getenv("DB_USER", "exchange_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "exchange_pass")
DB_NAME = os.getenv("DB_NAME", "exchange_book")
print(f"🔧 DB Config - HOST: {DB_HOST}, USER: {DB_USER}, DB: {DB_NAME}")
# Thử kết nối nhiều lần để chờ MySQL khởi động
db = None
for i in range(10):
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=3306
        )
        if db.is_connected():
            print(f"✅ Connected to MySQL database at {DB_HOST}")
            break
    except Error as e:
        print(f"⏳ Waiting for MySQL... attempt {i+1}/10 | {e}")
        time.sleep(5)

if not db or not db.is_connected():
    raise Exception("❌ Could not connect to MySQL after 10 attempts.")

mycursor = db.cursor()

def importData(sql,val):

    mycursor.execute(sql, val)
    db.commit()

# Hàm import và lấy lại ID vừa tạo
def importDataGetId(sql, val):
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    last_id = cursor.lastrowid
    cursor.close()
    return last_id

def exportData(sql, val, fetch_all=False):
    mycursor.execute(sql, val)
    return mycursor.fetchall() if fetch_all else mycursor.fetchone()
