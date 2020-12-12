import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

def sendMail(mailBody, mailSubject):
    """ Send a mail via gmail with credentials from .env file """
    user = os.getenv("GMAIL_USER")
    pw = os.getenv("GMAIL_PW")
    sent_to = os.getenv("SEND_TO")
    email_text = """\
From: %s
To: %s
Subject: %s


%s
""" % (user, sent_to, mailSubject, mailBody)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(user, pw)
        server.sendmail(user, sent_to, email_text.encode('utf-8'))
        server.close()
        print('E-Mail sent!')

    except Exception as e:
        print('Error: '+ str(e))


if __name__ == "__main__":
    sendMail( mailBody = 'Eine E-Mail von Python3!', mailSubject = 'PythonMail' )
