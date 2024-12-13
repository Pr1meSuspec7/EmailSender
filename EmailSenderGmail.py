import smtplib
import os
import sys
from dotenv import dotenv_values
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr


################### Fill these fields ###################

From = "Sender Name"
Recipients = "mail1@example.com, mail2@example.com"
Subject = "Test Mail"
Message = "Mail message"
Attachments = ["attachment1.txt", "attachment2.txt"]

#########################################################


def load_dotenv(file):
    if os.path.exists(file) == True:
        credentials = dotenv_values(file)
        return credentials
    else:
        print(f"File {file} not found!")
        sys.exit()

credentials = load_dotenv(".env")
Account = credentials.get('Account')
Password = credentials.get('Password')

class EmailSender:
    def __init__(self, account, password):
        self.client = smtplib.SMTP(host='smtp.gmail.com', port=587)
        self.client.starttls()
        self.client.login(account, password)

    def send_email(self, from_email, recipients, subject, message, attachments = []):
        msg = MIMEMultipart()
        msg['From'] = formataddr((str(Header(from_email, 'utf-8')), 'no_reply@gmail.com'))
        msg['To'] = recipients
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        if attachments:
            for attachment in attachments:
                part = MIMEApplication(open(attachment, 'rb').read())
                part.add_header('Content-Disposition', 'attachment', filename = os.path.basename(attachment))
                msg.attach(part)

        self.client.send_message(msg)
        self.client.quit()


sender = EmailSender(Account, Password)
sender.send_email(From, Recipients, Subject, Message, Attachments)
