import mysql.connector
import warnings
warnings.filterwarnings("ignore")

db = mysql.connector.connect(
    host="192.168.1.216",
    user="root",
    passwd="",
    database="dacn1"
)
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
