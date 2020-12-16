import smtplib
from email.mime.text import MIMEText

sender = 'admin@example.com'
receivers = ['info@example.com']


port = 1025
msg = MIMEText('This is test mail')

msg['Subject'] = 'Test mail'
msg['From'] = 'admin@example.com'
msg['To'] = 'info@example.com'

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login('duiculaurentiu50', 'alphaomega')
    sender = 'duiculaurentiu50@gmail.com'
    receivers = ['duicul@yahoo.com']
    server.sendmail(sender, receivers, msg.as_string())
    print("Successfully sent email")


