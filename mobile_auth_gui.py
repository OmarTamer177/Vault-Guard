import tkinter as tk
from tkinter import messagebox, ttk
import requests
import pyotp
import time
import urllib3
import json
import os

# Suppress warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MobileAuthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VaultGuard Mobile Authenticator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        self.server_url = "https://127.0.0.1:5000"
        self.username = None
        self.secret = None
        self.otp_label = None
        self.timer_label = None
        self.saved_users_file = "mobile_users.json"
        self.saved_users = self.load_saved_users()
        
        self.create_widgets()
        
    def load_saved_users(self):
        """Load previously registered users from file"""
        if os.path.exists(self.saved_users_file):
            try:
                with open(self.saved_users_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self):
        """Save registered users to file"""
        with open(self.saved_users_file, 'w') as f:
            json.dump(self.saved_users, f, indent=4)
    
    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="VaultGuard Mobile Authenticator", 
                         font=("Arial", 16, "bold"), bg="#2196F3", fg="white", pady=15)
        header.pack(fill=tk.X)
        
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.show_login_screen()
        
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def show_login_screen(self):
        self.clear_frame()
        
        tk.Label(self.main_frame, text="Welcome!", font=("Arial", 14, "bold")).pack(pady=10)
        
        # If there are saved users, show them with scrollbar
        if self.saved_users:
            tk.Label(self.main_frame, text="Your Saved Users:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
            
            # Create scrollable frame for users (max height: 150px)
            users_wrapper = tk.Frame(self.main_frame, height=150)
            users_wrapper.pack(fill=tk.X, pady=5)
            users_wrapper.pack_propagate(False)  # Don't auto-expand
            
            scrollbar = tk.Scrollbar(users_wrapper)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            canvas = tk.Canvas(users_wrapper, yscrollcommand=scrollbar.set, highlightthickness=0, bg="#f5f5f5")
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=canvas.yview)
            
            users_frame = tk.Frame(canvas, bg="#f5f5f5")
            canvas.create_window((0, 0), window=users_frame, anchor=tk.NW, width=380)
            
            for username in self.saved_users:
                btn = tk.Button(users_frame, text=f"👤 {username}", 
                               command=lambda u=username: self.login_user(u),
                               bg="#2196F3", fg="white", font=("Arial", 10),
                               padx=15, pady=6, width=40)
                btn.pack(pady=3, fill=tk.X, padx=5)
            
            def on_frameconfig(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            users_frame.bind("<Configure>", on_frameconfig)
            
            # Separator
            tk.Label(self.main_frame, text="─" * 30, fg="#ccc").pack(pady=8)
        
        tk.Label(self.main_frame, text="Register New Device:", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Register button
        btn_register = tk.Button(self.main_frame, text="Register New Device", 
                                command=self.show_register_screen, 
                                bg="#4CAF50", fg="white", font=("Arial", 11),
                                padx=20, pady=10, width=25)
        btn_register.pack(pady=5)
        
        # Exit button
        btn_exit = tk.Button(self.main_frame, text="Exit", 
                            command=self.root.quit,
                            bg="#f44336", fg="white", font=("Arial", 11),
                            padx=20, pady=10, width=25)
        btn_exit.pack(pady=5)
        
    def show_register_screen(self):
        self.clear_frame()
        
        tk.Label(self.main_frame, text="Register New Device", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self.main_frame, text="Username:", font=("Arial", 10)).pack(pady=5)
        username_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=30)
        username_entry.pack(pady=5)
        
        def register():
            username = username_entry.get().strip()
            if not username:
                messagebox.showerror("Error", "Please enter a username")
                return
                
            try:
                response = requests.post(
                    f"{self.server_url}/register",
                    json={"username": username},
                    verify=False
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.secret = data['secret']
                    self.username = username
                    # Save user locally
                    self.saved_users[username] = self.secret
                    self.save_users()
                    messagebox.showinfo("Success", f"Registered!\n\nUser '{username}' saved locally.\nYou can log in anytime!")
                    self.show_otp_screen()
                elif response.status_code == 409:
                    messagebox.showerror("Error", "User already exists")
                else:
                    messagebox.showerror("Error", f"Server error: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Could not connect to MFA Server.\nMake sure mfa_server.py is running!")
        
        btn_register = tk.Button(self.main_frame, text="Register", 
                                command=register, 
                                bg="#4CAF50", fg="white", font=("Arial", 12),
                                padx=20, pady=10)
        btn_register.pack(pady=20)
        
        btn_back = tk.Button(self.main_frame, text="Back", 
                            command=self.show_login_screen,
                            bg="#9E9E9E", fg="white", font=("Arial", 10),
                            padx=15, pady=5)
        btn_back.pack(pady=10)
        
    def login_user(self, username):
        """Log in to an existing saved user"""
        self.username = username
        self.secret = self.saved_users[username]
        self.show_otp_screen()
        
    def show_otp_screen(self):
        self.clear_frame()
        
        tk.Label(self.main_frame, text=f"User: {self.username}", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        # OTP Display
        otp_frame = tk.Frame(self.main_frame, bg="#E3F2FD", relief=tk.RAISED, borderwidth=2)
        otp_frame.pack(pady=20, padx=10, fill=tk.X)
        
        tk.Label(otp_frame, text="Current OTP:", font=("Arial", 10), bg="#E3F2FD").pack(pady=(10, 0))
        
        self.otp_label = tk.Label(otp_frame, text="------", 
                                  font=("Courier", 32, "bold"), 
                                  fg="#2196F3", bg="#E3F2FD")
        self.otp_label.pack(pady=10)
        
        self.timer_label = tk.Label(otp_frame, text="Valid for: 60s", 
                                    font=("Arial", 10), fg="#666", bg="#E3F2FD")
        self.timer_label.pack(pady=(0, 10))
        
        # Info label
        tk.Label(self.main_frame, text="Use this code to login to VaultGuard", 
                font=("Arial", 9), fg="#666").pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(pady=20)
        
        btn_copy = tk.Button(btn_frame, text="Copy OTP", 
                            command=self.copy_otp,
                            bg="#2196F3", fg="white", font=("Arial", 10),
                            padx=15, pady=8)
        btn_copy.pack(side=tk.LEFT, padx=5)
        
        btn_logout = tk.Button(btn_frame, text="Logout", 
                              command=self.logout,
                              bg="#f44336", fg="white", font=("Arial", 10),
                              padx=15, pady=8)
        btn_logout.pack(side=tk.LEFT, padx=5)
        
        btn_delete = tk.Button(btn_frame, text="🗑️ Delete", 
                              command=self.delete_user,
                              bg="#9C27B0", fg="white", font=("Arial", 10),
                              padx=15, pady=8)
        btn_delete.pack(side=tk.LEFT, padx=5)
        
        # Start OTP update loop
        self.update_otp()
        
    def update_otp(self):
        if not self.secret or self.otp_label is None:
            return
            
        try:
            totp = pyotp.TOTP(self.secret, interval=60)  # 60-second interval
            otp = totp.now()
            remaining = int(totp.interval - (time.time() % totp.interval))
            
            self.otp_label.config(text=otp)
            self.timer_label.config(text=f"Valid for: {remaining}s")
            
            # Update every second
            self.root.after(1000, self.update_otp)
        except Exception as e:
            self.otp_label.config(text="ERROR")
            self.timer_label.config(text=str(e))
            
    def copy_otp(self):
        try:
            totp = pyotp.TOTP(self.secret, interval=60)  # 60-second interval
            otp = totp.now()
            self.root.clipboard_clear()
            self.root.clipboard_append(otp)
            messagebox.showinfo("Copied", f"OTP {otp} copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")
            
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.username = None
            self.secret = None
            self.otp_label = None
            self.timer_label = None
            self.show_login_screen()
    
    def delete_user(self):
        """Delete currently logged in user from saved users"""
        if messagebox.askyesno("Delete User", f"Permanently delete '{self.username}' from saved users?\n\nYou can re-register later."):
            if self.username in self.saved_users:
                del self.saved_users[self.username]
                self.save_users()
                messagebox.showinfo("Deleted", f"User '{self.username}' has been deleted.")
            self.logout()

if __name__ == "__main__":
    root = tk.Tk()
    app = MobileAuthGUI(root)
    root.mainloop()