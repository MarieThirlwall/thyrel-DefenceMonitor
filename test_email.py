#!/usr/bin/env python3
"""
Test Email Configuration
Run this locally to verify your email credentials work before deploying to GitHub
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_email():
    """Test email sending with current configuration"""

    # Get credentials
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')

    print("\n" + "="*60)
    print("Email Configuration Test")
    print("="*60 + "\n")

    print("[CONFIGURATION]")
    print(f"  SMTP Server: {smtp_server}")
    print(f"  SMTP Port: {smtp_port}")
    print(f"  Sender Email: {sender_email if sender_email else 'NOT SET'}")
    print(f"  Sender Password: {'SET' if sender_password else 'NOT SET'}")
    print(f"  Recipient Email: {recipient_email if recipient_email else 'NOT SET'}")
    print()

    # Validate credentials
    if not sender_email:
        print("ERROR: SENDER_EMAIL not set in .env file")
        return False

    if not sender_password:
        print("ERROR: SENDER_PASSWORD not set in .env file")
        print("   Get Gmail App Password from: https://myaccount.google.com/apppasswords")
        return False

    if not recipient_email:
        print("ERROR: RECIPIENT_EMAIL not set in .env file")
        return False

    # Create test message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Test Email - Defence News Monitor - {datetime.now().strftime('%d %b %Y %H:%M')}"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #2c3e50;">✓ Email Test Successful</h2>
        <p>This is a test email from your Defence News Monitor system.</p>
        <p><strong>Configuration verified:</strong></p>
        <ul>
            <li>SMTP connection successful</li>
            <li>Authentication successful</li>
            <li>Email delivery successful</li>
        </ul>
        <p style="color: #7f8c8d; font-size: 12px;">
            Sent: {timestamp}<br>
            From: {sender}<br>
            To: {recipient}
        </p>
    </body>
    </html>
    """.format(
        timestamp=datetime.now().strftime('%d %B %Y %H:%M:%S'),
        sender=sender_email,
        recipient=recipient_email
    )

    msg.attach(MIMEText(html_content, 'html'))

    # Send test email
    try:
        print("[SENDING TEST EMAIL]")
        print(f"  Connecting to {smtp_server}:{smtp_port}...")

        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            print(f"  Connected")
            print(f"  Starting TLS encryption...")
            server.starttls()
            print(f"  TLS started")

            print(f"  Authenticating as {sender_email}...")
            server.login(sender_email, sender_password)
            print(f"  Authentication successful")

            print(f"  Sending test message to {recipient_email}...")
            server.send_message(msg)
            print(f"  Message sent")

        print("\n" + "="*60)
        print("SUCCESS! Email sent successfully")
        print("="*60)
        print(f"\nCheck your inbox: {recipient_email}")
        print("(Also check spam folder if you don't see it)")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"\nAUTHENTICATION FAILED")
        print(f"   Error: {e}")
        print("\n   Troubleshooting:")
        print("   1. Verify 2-Step Verification is enabled in your Google Account")
        print("   2. Go to: https://myaccount.google.com/apppasswords")
        print("   3. Create a new App Password (select 'Mail' and 'Other')")
        print("   4. Use the 16-character password (remove spaces)")
        print("   5. Update SENDER_PASSWORD in .env file")
        return False

    except smtplib.SMTPException as e:
        print(f"\nSMTP ERROR")
        print(f"   Error: {e}")
        print(f"   Server: {smtp_server}:{smtp_port}")
        return False

    except Exception as e:
        print(f"\nUNEXPECTED ERROR")
        print(f"   Type: {type(e).__name__}")
        print(f"   Error: {e}")
        return False

if __name__ == "__main__":
    success = test_email()
    exit(0 if success else 1)
