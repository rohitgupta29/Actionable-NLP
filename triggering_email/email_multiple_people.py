import smtplib
#to get multiple images
import imghdr
from email.message import EmailMessage


EMAIL_ADDRESS = 'infomatxxxrxxxx@gmail.com'
EMAIL_PASSWORD = "9xxxxxxxxx4"

contacts = ["xxxx.xxxxxxpta@gmail.com", "infomatxxxxxxxt@gmail.com"]

msg = EmailMessage()
msg['Subject'] = "Check out this Book"
msg['From'] = EMAIL_ADDRESS
msg['To'] = ', '.join(contacts)
msg.set_content('This is a plain text email')


msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
    </body>
</html>""", subtype = 'html')

def sendmail(msg):
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # smtp = smtplib.SMTP("localhost", 1025)
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    # message_body = f"Subject:{subject}\n\n{body}"
    smtp.send_message(msg)
    # smtp.sendmail(EMAIL_ADDRESS,"xxxxt.xxxxpta@gmail.com", message_body)
    smtp.quit()

sendmail(msg)
