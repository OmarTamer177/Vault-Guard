from flask import Flask, request, jsonify
import pyotp
import time
import os
import json

app = Flask(__name__)

DB_FILE = "mfa_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

users_db = load_db()

@app.route('/')
def index():
    return "VaultGuard MFA Server is Running (Secure)"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username required"}), 400
        
    if username in users_db:
        return jsonify({"error": "User already exists"}), 409
        
    # Generate TOTP Secret
    secret = pyotp.random_base32()
    users_db[username] = {"secret": secret}
    save_db(users_db)
    
    # In a real app, we'd return a QR code URI
    # otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="VaultGuard")
    
    print(f"[Server] Registered user '{username}' with secret: {secret}")
    
    return jsonify({
        "message": "Registration successful", 
        "secret": secret,
        "info": "Enter this secret into the Mobile Auth App"
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    otp_code = data.get('otp')
    
    if not username or not otp_code:
        return jsonify({"error": "Missing credentials"}), 400
        
    user = users_db.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    secret = user['secret']
    totp = pyotp.TOTP(secret)
    
    # Verify (window=1 means allow +/- 30 seconds for clock drift, creating a validity window)
    if totp.verify(otp_code, valid_window=1):
        return jsonify({"message": "Access Granted", "authenticated": True})
    else:
        return jsonify({"message": "Invalid OTP", "authenticated": False}), 401

@app.route('/get-otp-simulation', methods=['GET'])
def get_otp_simulation():
    """
    DEBUG ONLY: Helper to get the current valid OTP for a user because we are simulating.
    Simulates the 'Server generating the OTP' aspect for the Mobile App to fetch.
    """
    username = request.args.get('username')
    user = users_db.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    secret = user['secret']
    totp = pyotp.TOTP(secret)
    current_otp = totp.now()
    time_remaining = totp.interval - (time.time() % totp.interval)
    
    return jsonify({
        "otp": current_otp,
        "time_remaining": time_remaining
    })

if __name__ == '__main__':
    # SSL Context 'adhoc' generates a self-signed cert on the fly
    print("Starting MFA Server on port 5000 (HTTPS)...")
    try:
        app.run(host='0.0.0.0', port=5000, ssl_context='adhoc', debug=True)
    except Exception as e:
        print(f"Failed to start with SSL: {e}. Fallback to HTTP for debugging (NOT SECURE).")
        app.run(host='0.0.0.0', port=5000, debug=True)
