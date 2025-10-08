import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(to_email, subject, body):
    global server
    EMAIL_SENDER = "hbnguyen132@gmail.com"
    EMAIL_PASSWORD = "dwni qvsx fagy kypn"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))  # Nếu muốn gửi HTML: MIMEText(body, "html")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Bật TLS
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        print(f"✅ Email đã gửi đến {to_email}")
    except smtplib.SMTPAuthenticationError:
        print("❌ Lỗi xác thực! Kiểm tra email/mật khẩu hoặc bật App Password.")
    except smtplib.SMTPException as e:
        print(f"❌ Lỗi SMTP: {e}")
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")
    finally:
        server.quit()  # Đóng kết nối

