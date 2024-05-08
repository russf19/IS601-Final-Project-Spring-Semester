import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class SMTPClient:
    def __init__(self, server: str, port: int, username: str, password: str):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, subject: str, content: str, recipient: str, content_type='html'):
        try:
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = self.username
            message['To'] = recipient
            # Set the body of the email
            message.attach(MIMEText(content, content_type))

            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()  # Ensure using TLS
                server.login(self.username, self.password)
                server.send_message(message)  # Use send_message to handle MIME objects
            logging.info(f"Email sent to {recipient}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            raise
        