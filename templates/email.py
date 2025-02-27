import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os

# Email configuration
sender_email = "your mail"
sender_password = "your password"  # Use an App Password if 2FA is enabled
recipient_email = "recieptent mail"
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Gmail's SMTP port

# Create the email message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = recipient_email
message['Subject'] = "Email with Image Attachment"

# Email body
body = "This email contains an image attachment."
message.attach(MIMEText(body, 'plain'))

# Attach an image file
image_path = "templates\dharunkuamr.jpg"  # Replace with the path to your image file
with open(image_path, 'rb') as image_file:
    image = MIMEImage(image_file.read(), name="templates\dharunkumar.jpg")
message.attach(image)

# Connect to the SMTP server
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, message.as_string())
    server.quit()
    print("Email with image attachment sent successfully")
except Exception as e:
    print("An error occurred while sending the email:", str(e))