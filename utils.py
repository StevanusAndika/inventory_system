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
    smtp_username = "your_email@gmail.com"  # Ganti dengan email Anda
    smtp_password = "your_app_password"     # Ganti dengan password aplikasi
    
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
            for row in data:
                writer.writerow(row)
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

    def add_item(self, name, category, stock, unit, created_date, expiry_date, min_stock=10):
        items = self.load_data(self.items_file)
    
    new_item = {
        "id": self.get_next_id(items),
        "name": name,
        "category": category,
        "stock": stock,
        "unit": unit,
        "created_date": created_date,
        "expiry_date": expiry_date,
        "min_stock": min_stock
    }
    
    items.append(new_item)
    self.save_data(self.items_file, items)
    return True

def update_item(self, item_id, name, category, stock, unit, created_date, expiry_date, min_stock=10):
    items = self.load_data(self.items_file)
    
    for item in items:
        if item["id"] == item_id:
            item["name"] = name
            item["category"] = category
            item["stock"] = stock
            item["unit"] = unit
            item["created_date"] = created_date
            item["expiry_date"] = expiry_date
            item["min_stock"] = min_stock
            
            self.save_data(self.items_file, items)
            return True
            
    return False