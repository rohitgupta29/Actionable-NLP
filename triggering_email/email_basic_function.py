
import smtplib

EMAIL_ADDRESS = 'infomationxxxit@gmail.com'
EMAIL_PASSWORD = "xxxxxxxx74"

subject = 'Grab dinner this weekend'
body = 'How about dinner at 6 pm this saturday'

def sendmail(subject, body):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    # smtp = smtplib.SMTP("localhost", 1025)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    message_body = f"Subject:{subject}\n\n{body}"
    smtp.sendmail(EMAIL_ADDRESS,"rohit.ajaygupta@gmail.com", message_body)
    smtp.quit()

sendmail(subject, body)
