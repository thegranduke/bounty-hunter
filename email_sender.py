# Sending email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from dotenv import load_dotenv
import os
load_dotenv()

# Email configuration
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECIPIENT_EMAIL")
password = os.getenv("SENDER_PASSWORD")

# Email content
subject = "Test Email from Python"
body = "This is another test email sent from a Python script."

# Set up the MIME
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

try:
    # Set up the SMTP server with extended timeout
    server = smtplib.SMTP("smtp.mail.yahoo.com", 587, timeout=30)
    
    # Enable debug output
    # server.set_debuglevel(1)
    
    # Identify ourselves to SMTP server
    server.ehlo()
    
    # Secure the connection
    server.starttls()
    
    # Re-identify ourselves over TLS connection
    server.ehlo()
    
    # Login
    server.login(sender_email, password)
    
    # Send email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
    
    # Close the connection
    server.quit()

except smtplib.SMTPServerDisconnected as e:
    print(f"Server disconnected unexpectedly: {e}")
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication failed: {e}")
except smtplib.SMTPException as e:
    print(f"SMTP error occurred: {e}")
except Exception as e:
    print(f"Other error occurred: {e}")