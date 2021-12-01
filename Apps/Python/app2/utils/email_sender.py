import smtplib
import ssl
import sys
import imghdr
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

EMAIL_ADDRESS = 'support@sinlessgames.com'
EMAIL_PASSWORD = 'Shellshocker93!'
context = ssl.create_default_context()

with SMTP('mail.sinlessgames.com') as smtp:
    try:
        def verify(email):

            msg = MIMEMultipart()
            msg['From'] = f'{EMAIL_ADDRESS}\n\n'
            msg['To'] = email + '\n\n'
            msg['Subject'] = 'test verify' + '\n\n'
            body = """ Someone sent a Helix verification email to this address! Here is the link: 
            www.xxxx.co/verify/
            Not you? Ignore this email.\n
            Thank You for choosing Helix Ai Your virtual assistant.
            """.format(email)
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('mail.sinlessgames.com', 587)
            server.starttls(context=context)
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print(msg.as_string())
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
            server.close()

            print("Successfully sent email message")

    except:
        sys.exit("mail failed; %s" % "CUSTOM_ERROR")  # give an error message

