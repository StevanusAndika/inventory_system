import hashlib
import smtplib
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_email_notification(to_email, subject, message):
    # Konfigurasi email server
    # Catatan: Ini adalah contoh, Anda perlu mengonfigurasi dengan pengaturan email Anda sendiri
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "stevanusstudent@gmail.com"  # Ganti dengan email Anda
    smtp_password = "bzhd yijo kccq nmve" 
    
    try:
        # Buat message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Tambahkan body pesan
        msg.attach(MIMEText(message, 'plain'))
        
        # Kirim email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, to_email, text)
        server.quit()
        
        print(f"Email berhasil dikirim ke {to_email}")
        return True
    except Exception as e:
        print(f"Gagal mengirim email: {e}")
        return False

def export_to_csv(data, filename, fieldnames):
    """Export data to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def validate_date(date_string):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_current_date():
    """Get current date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")

def format_currency(amount):
    """Format number as currency"""
    return "Rp {:,.2f}".format(amount).replace(",", "X").replace(".", ",").replace("X", ".")