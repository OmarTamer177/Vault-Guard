import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sys
from vault_file_manager import VaultFileManager
from crypto_manager import CryptoManager
from mfa_client import MFAService

class VaultGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VaultGuard Password Manager")
        self.root.geometry("800x600")
        
        self.file_manager = VaultFileManager()
        self.crypto = CryptoManager()
        self.mfa = MFAService()
        self.credentials = []
        self.master_password = None
        
        self.show_login_screen()
        
    def show_login_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Header
        header = tk.Frame(self.root, bg="#1976D2", height=80)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🔐 VaultGuard", font=("Arial", 24, "bold"), 
                bg="#1976D2", fg="white").pack(pady=20)
        
        # Login frame
        login_frame = tk.Frame(self.root, padx=40, pady=40)
        login_frame.pack(expand=True)
        
        tk.Label(login_frame, text="Master Password:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=10)
        master_pass_entry = tk.Entry(login_frame, show="*", font=("Arial", 12), width=30)
        master_pass_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(login_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=10)
        username_entry = tk.Entry(login_frame, font=("Arial", 12), width=30)
        username_entry.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(login_frame, text="OTP (from Mobile App):", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=10)
        otp_entry = tk.Entry(login_frame, font=("Arial", 12), width=30)
        otp_entry.grid(row=2, column=1, pady=10, padx=10)
        
        def login():
            master_password = master_pass_entry.get()
            username = username_entry.get()
            otp = otp_entry.get()
            
            if not master_password or not username or not otp:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            if len(otp) != 6 or not otp.isdigit():
                messagebox.showerror("Error", "OTP must be 6 digits")
                return
                
            # Verify MFA
            if not self.verify_mfa(username, otp):
                return
                
            # Load vault
            self.master_password = master_password
            if not self.load_vault():
                return
                
            self.show_main_screen()
        
        btn_login = tk.Button(login_frame, text="Login", command=login, 
                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                             padx=30, pady=10)
        btn_login.grid(row=3, column=0, columnspan=2, pady=30)
        
        # Bind Enter key
        master_pass_entry.bind("<Return>", lambda e: username_entry.focus())
        username_entry.bind("<Return>", lambda e: otp_entry.focus())
        otp_entry.bind("<Return>", lambda e: login())
        
        master_pass_entry.focus()
        
    def verify_mfa(self, username, otp):
        try:
            import requests
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            response = requests.post(
                "https://127.0.0.1:5000/login",
                json={"username": username, "otp": otp},
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("authenticated") is True:
                    return True
            
            error_msg = response.json().get('message', 'Authentication failed')
            if response.status_code == 404:
                messagebox.showerror("Access Denied", f"User '{username}' not registered.\nPlease register in the Mobile App first.")
            elif response.status_code == 401:
                messagebox.showerror("Access Denied", f"Invalid or expired OTP.\nOTPs expire after 60 seconds.")
            else:
                messagebox.showerror("Access Denied", error_msg)
            return False
            
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Connection timeout.\nMFA Server took too long to respond.")
            return False
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Could not connect to MFA Server.\nMake sure mfa_server.py is running!")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"MFA verification failed: {str(e)}")
            return False
            
    def load_vault(self):
        encrypted_data = self.file_manager.load_vault()
        
        if encrypted_data is False:
            messagebox.showerror("Security Alert", "File integrity compromised!")
            sys.exit()
        elif encrypted_data is None:
            # New vault
            self.credentials = []
            messagebox.showinfo("New Vault", "Creating a new vault for you!")
            return True
        else:
            try:
                self.credentials = self.crypto.decrypt_data(encrypted_data, self.master_password)
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt vault.\nWrong master password?\n\n{e}")
                return False
                
    def show_main_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Header
        header = tk.Frame(self.root, bg="#1976D2", height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🔐 VaultGuard - Password Vault", font=("Arial", 18, "bold"), 
                bg="#1976D2", fg="white").pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_save_exit = tk.Button(header, text="Save & Exit", command=self.save_and_exit,
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_save_exit.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Main content
        content = tk.Frame(self.root)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Buttons frame
        btn_frame = tk.Frame(content)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(btn_frame, text="➕ Add Credential", command=self.add_credential,
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="✏️ Edit", command=self.edit_credential,
                 bg="#FF9800", fg="white", font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Delete", command=self.delete_credential,
                 bg="#f44336", fg="white", font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📋 Copy Password", command=self.copy_password,
                 bg="#9C27B0", fg="white", font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        # Treeview for credentials
        tree_frame = tk.Frame(content)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Service", "Username", "Password"), 
                                show="headings", yscrollcommand=scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("Service", text="Service")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        
        self.tree.column("Service", width=200)
        self.tree.column("Username", width=200)
        self.tree.column("Password", width=200)
        
        # Style
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        self.refresh_tree()
        
    def refresh_tree(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add credentials
        for i, cred in enumerate(self.credentials):
            self.tree.insert("", tk.END, iid=i, values=(
                cred['service'],
                cred['username'],
                "•" * 10  # Hide password
            ))
            
    def add_credential(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Credential")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Service:", font=("Arial", 10)).pack(pady=(20, 5))
        service_entry = tk.Entry(dialog, font=("Arial", 11), width=35)
        service_entry.pack(pady=5)
        
        tk.Label(dialog, text="Username:", font=("Arial", 10)).pack(pady=5)
        username_entry = tk.Entry(dialog, font=("Arial", 11), width=35)
        username_entry.pack(pady=5)
        
        tk.Label(dialog, text="Password:", font=("Arial", 10)).pack(pady=5)
        password_entry = tk.Entry(dialog, show="*", font=("Arial", 11), width=35)
        password_entry.pack(pady=5)
        
        def save():
            service = service_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not service or not username or not password:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            if len(service) > 50 or len(username) > 100:
                messagebox.showerror("Error", "Service or username too long!")
                return
                
            self.credentials.append({
                "service": service,
                "username": username,
                "password": password
            })
            
            self.refresh_tree()
            dialog.destroy()
            messagebox.showinfo("Success", f"Credential for '{service}' added!")
        
        tk.Button(dialog, text="Save", command=save, bg="#4CAF50", fg="white", 
                 font=("Arial", 11), padx=30, pady=8).pack(pady=20)
                 
        service_entry.focus()
        
    def edit_credential(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a credential to edit")
            return
            
        idx = int(selection[0])
        cred = self.credentials[idx]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Credential")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Service:", font=("Arial", 10)).pack(pady=(20, 5))
        service_entry = tk.Entry(dialog, font=("Arial", 11), width=35)
        service_entry.insert(0, cred['service'])
        service_entry.pack(pady=5)
        
        tk.Label(dialog, text="Username:", font=("Arial", 10)).pack(pady=5)
        username_entry = tk.Entry(dialog, font=("Arial", 11), width=35)
        username_entry.insert(0, cred['username'])
        username_entry.pack(pady=5)
        
        tk.Label(dialog, text="Password (leave blank to keep current):", font=("Arial", 10)).pack(pady=5)
        password_entry = tk.Entry(dialog, show="*", font=("Arial", 11), width=35)
        password_entry.pack(pady=5)
        
        def save():
            service = service_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not service or not username:
                messagebox.showerror("Error", "Service and username are required!")
                return
                
            if not password:
                password = cred['password']
                
            self.credentials[idx] = {
                "service": service,
                "username": username,
                "password": password
            }
            
            self.refresh_tree()
            dialog.destroy()
            messagebox.showinfo("Success", "Credential updated!")
        
        tk.Button(dialog, text="Save", command=save, bg="#FF9800", fg="white",
                 font=("Arial", 11), padx=30, pady=8).pack(pady=20)
                 
    def delete_credential(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a credential to delete")
            return
            
        idx = int(selection[0])
        cred = self.credentials[idx]
        
        if messagebox.askyesno("Confirm Delete", f"Delete credential for {cred['service']}?"):
            del self.credentials[idx]
            self.refresh_tree()
            messagebox.showinfo("Success", "Credential deleted!")
            
    def copy_password(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a credential")
            return
            
        idx = int(selection[0])
        password = self.credentials[idx]['password']
        
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copied", f"Password for '{self.credentials[idx]['service']}' copied to clipboard!")
        
    def save_and_exit(self):
        if messagebox.askyesno("Save & Exit", "Save vault and exit?"):
            try:
                encrypted = self.crypto.encrypt_data(self.credentials, self.master_password)
                self.file_manager.save_vault(encrypted)
                messagebox.showinfo("Success", "Vault saved successfully!")
                self.root.quit()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save vault:\n{str(e)}")
                if messagebox.askyesno("Error", "Save failed. Exit anyway?"):
                    self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VaultGUI(root)
    root.mainloop()
