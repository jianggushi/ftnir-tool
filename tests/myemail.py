import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 邮件服务器配置
smtp_server = "smtp.office365.com"  # 替换为你的SMTP服务器
smtp_port = 587  # 常用端口：587(TLS)或465(SSL)
sender_email = "geodataplatform@geosi.com"  # 发件人邮箱
password = "Geo@1234"  # 邮箱密码或应用专用密码
receiver_email = "jiangxiaojie@skyisz.com"  # 收件人邮箱

# 创建邮件内容
message = MIMEText("hello", "plain", "utf-8")
message["From"] = Header(sender_email)
message["To"] = Header(receiver_email)
message["Subject"] = Header("Test Email", "utf-8")

try:
    # 连接到SMTP服务器
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # 启用TLS加密

    # 登录
    server.login(sender_email, password)

    # 发送邮件
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("邮件发送成功！")

except Exception as e:
    print(f"发送失败: {str(e)}")

finally:
    # 关闭连接
    server.quit()
