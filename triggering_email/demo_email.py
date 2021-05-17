import os
import smtplib

EMAIL_ADDRESS = 'infomationrohit@gmail.com'
EMAIL_PASSWORD = 9419131674

#
# EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
# EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
# print(os.environ['EMAIL_USER'])
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    #elho identifies with the server
    smtp.elho()
    #encrypt our traffic
    smtp.starttls()


    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'Grab dinner this weekend'
    body = 'How about dinner at 6 pm this saturday'

    msg = f'Subject: {subject}\n\n{body}'

    smtp.sendmail(EMAIL_ADDRESS,rohit.ajaygupta@gmail.com, msg)

