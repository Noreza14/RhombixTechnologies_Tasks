from flask import Flask, request, jsonify, render_template, send_from_directory, flash, redirect, url_for
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'your_secret_key'  # Set a secret key for flash messages

# Get email credentials from .env
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))  # Ensure port is an integer

# Route to serve HTML form
@app.route('/pp.html')
def serve_html():
    return render_template('pp.html')  # Ensure the file is located in your templates directory

# Endpoint to handle form submission
@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Check if any field is missing
        if not name or not email or not message:
            flash("All fields are required", "error")
            return redirect(url_for('serve_html'))

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # Send to yourself
        msg['Subject'] = 'New Contact Form Submission'

        # Compose the body
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        msg.attach(MIMEText(body, 'plain'))

        # Set up the server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        flash("Message sent successfully!", "success")
        return redirect(url_for('serve_html'))
    except smtplib.SMTPException as smtp_error:
        flash(f"SMTP error occurred: {str(smtp_error)}", "error")
        return redirect(url_for('serve_html'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('serve_html'))

if __name__ == '__main__':
    app.run(debug=True)

