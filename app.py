import os
import random
import string
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Generate a random OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Generate QR code from OTP
def generate_qr_code(otp):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(otp)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Store the generated OTP and QR code
otp_data = {}

def send_image_email(recipient_email, image_path):
    # Email configuration
    smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
    smtp_port = 588 #your port number
    sender_email = 'your mail'  
    sender_password = 'your passoword' 

    # Create a message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Image Attachment Example'

    # Attach image file
    with open(image_path, 'rb') as image_file:
        image = MIMEImage(image_file.read(), name='image.jpg')
    msg.attach(image)

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending error: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-otp', methods=['POST'])
def generate_otp_page():
    phone_number = request.form.get('phone_number')
    otp = generate_otp()
    qr_code = generate_qr_code(otp)
    otp_data[phone_number] = otp
    qr_code.save(f'static/generated_qr/{phone_number}.png')
    send_image_email(phone_number,f'static/generated_qr/{phone_number}.png')
    return render_template('generate_qr.html', phone_number=phone_number)

@app.route('/verify', methods=['GET', 'POST'])
def verify_qr():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        phone_number = request.form.get('phone_number')
        
        if phone_number in otp_data:
            expected_otp = otp_data[phone_number]

            # Open the uploaded image using PIL
            uploaded_image = Image.open(uploaded_file)

            # Decode the QR code from the image
            decoded_objects = decode(uploaded_image)
            
            if decoded_objects:
                extracted_otp = decoded_objects[0].data.decode('utf-8')
                if expected_otp == extracted_otp:
                    return render_template('otpmatch.html', phone_number=phone_number)
        
        return "QR code mismatch! OTP Verification Failed."

    return render_template('verify_qr.html')







if __name__ == '__main__':
    app.run(debug=True)
