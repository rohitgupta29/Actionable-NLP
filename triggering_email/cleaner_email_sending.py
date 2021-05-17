import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = 'infomationxxxxx@gmail.com'
EMAIL_PASSWORD = "94191xxxxxx"

msg = EmailMessage()
msg['Subject'] = "We all your Family.You are Awesome"
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'xxxxx.ajaygupta@gmail.com'
msg.set_content('How about dinner at 6 pm this saturday')


def sendmail(msg):
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # smtp = smtplib.SMTP("localhost", 1025)
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    # message_body = f"Subject:{subject}\n\n{body}"
    smtp.send_message(msg)
    # smtp.sendmail(EMAIL_ADDRESS,"rohit.ajaygupta@gmail.com", message_body)
    smtp.quit()

sendmail(msg)
