import hashlib
import json
import os
import random
import string
from utils import hash_password, send_email_notification

class AuthSystem:
    def __init__(self):
        self.users_file = "data/users.txt"
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            
    def load_users(self):
        if not os.path.exists(self.users_file):
            return []
            
        with open(self.users_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
                
    def save_users(self, users):
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=4)
            
    def register(self, username, password, email):
        users = self.load_users()
        
        # Check if username already exists
        for user in users:
            if user["username"] == username:
                return False
                
        # Create new user
        new_user = {
            "username": username,
            "password": hash_password(password),
            "email": email
        }
        
        users.append(new_user)
        self.save_users(users)
        
        # Send notification email
        send_email_notification(
            email, 
            "Registrasi Berhasil", 
            f"Akun Anda dengan username {username} telah berhasil dibuat."
        )
        
        return True
        
    def login(self, username, password):
        users = self.load_users()
        hashed_password = hash_password(password)
        
        for user in users:
            if user["username"] == username and user["password"] == hashed_password:
                return user
                
        return None
        
    def reset_password(self, email):
        users = self.load_users()
        
        for user in users:
            if user["email"] == email:
                # Generate random password
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                user["password"] = hash_password(new_password)
                
                self.save_users(users)
                
                # Send email with new password
                send_email_notification(
                    email,
                    "Reset Password",
                    f"Password Anda telah direset. Password baru Anda adalah: {new_password}\n\nSilakan login dan ubah password Anda segera."
                )
                
                return True
                
        return False