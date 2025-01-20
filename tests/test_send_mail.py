import smtplib
from email.mime.text import MIMEText

# Email details
sender_email = "baraiyavivek04@gmail.com"
receiver_email = "baraiyavivek04@gmail.com"
subject = "Test Email"
body = "This is a test email sent from Python!"

# Create the email
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

# Connect to Gmail's SMTP server
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender_email, "16-digit-app-password")  # Use your App Password here
    server.sendmail(sender_email, receiver_email, msg.as_string())

print("Email sent successfully!")
