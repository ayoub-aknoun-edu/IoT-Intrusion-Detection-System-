from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, settings):
        super().__init__()
        self.email_sender = settings['email_alerts']['email_sender']
        self.email_receiver = settings['email_alerts']['email_recipient']
        self.password = settings['email_alerts']['email_password']
        self.enabled = settings['email_alerts']['enabled']

    def send_email(self, subject, message):
        # em = EmailMessage()
        em = MIMEMultipart('alternative')
        em['From'] = self.email_sender
        em['To'] = self.email_receiver
        em['Subject'] = subject

        html = f"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>IDS Alert Notification</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 20px;
                    padding: 0;
                    color: #333;
                }}
                .header {{
                    background-color: #990000; /* Darker red */
                    padding: 20px;
                    text-align: center;
                    color: #ffffff;
                }}
                .content {{
                    margin: 20px 0;
                }}
                .attack-details {{
                    background-color: #ffe5e5; /* Light red/pink */
                    border-left: 5px solid #cc0000; /* Bright red */
                    padding: 20px;
                    margin: 10px 0;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    font-size: 0.9em;
                    color: #777;
                }}
                p {{
                    line-height: 1.5;
                }}
                strong {{
                    color: #cc0000;
                }}
            </style>
            </head>
            <body>
            <div class="header">
                <h2>IDS Alert Notification</h2>
            </div>
            <div class="content">
                <p>An intrusion attempt has been detected by the IDS. Here are the details:</p>
                <div class="attack-details">
                    <p><strong>Type of Attack:</strong> {message['attack_type']}</p>
                    <p><strong>Time of Detection:</strong> {message['timestamp']}</p>
                </div>
                <p>Please take the necessary actions to secure your systems. For safety reasons, the network has been shutdown to prevent further damages.</p>
            </div>
            <div class="footer">
                <p>This is an automated message. Please do not reply directly to this email.</p>
            </div>
            </body>
            </html>

        """
        part = MIMEText(html, 'html')
        em.attach(part)

        # em.set_content(message)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.password)
            smtp.sendmail(self.email_sender, self.email_receiver, em.as_string())

    def send_alert(self, timestamp, attack_type, ):
        if not self.enabled:
            return

        subject = "Network Attack Detected"
        message = {'attack_type': attack_type, 'timestamp': timestamp}

        self.send_email(subject, message)
