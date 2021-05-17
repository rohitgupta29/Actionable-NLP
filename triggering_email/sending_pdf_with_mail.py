import smtplib
#to get multiple images
import imghdr
from email.message import EmailMessage


EMAIL_ADDRESS = 'infomationxxxxx@gmail.com'
EMAIL_PASSWORD = "xxxxxxxxxxx"

msg = EmailMessage()
msg['Subject'] = "Check out this Book"
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'xxxxx.ajaygupta@gmail.com'
msg.set_content('Image Attached')

files = ['book.pdf']
for file in files:
    with open(file,'rb') as f:
        file_data = f.read()
        # file_type = imghdr.what(f.name)
        file_name = f.name

    msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file_name)

def sendmail(msg):
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # smtp = smtplib.SMTP("localhost", 1025)
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    # message_body = f"Subject:{subject}\n\n{body}"
    smtp.send_message(msg)
    # smtp.sendmail(EMAIL_ADDRESS,"rohit.ajaygupta@gmail.com", message_body)
    smtp.quit()

sendmail(msg)
