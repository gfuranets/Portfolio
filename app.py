from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message_body = request.form.get('message')

    if name and email and message_body:
        # Send the email
        msg = Message(subject = f"New message from {name}",
                      sender = app.config['MAIL_USERNAME'],
                      recipients = [app.config['MAIL_USERNAME']],  
                      body = f"Name: {name}\nEmail: {email}\n\n{message_body}")
        mail.send(msg)
        flash('Message sent successfully!', 'success')
    else:
        flash('Failed to send message. Please fill all fields.', 'error')

    return redirect('/#contact')

if __name__ == '__main__':
    app.run(debug = True)
