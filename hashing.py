import hashlib
import os
import random

CREDENTIALS_FILE = 'creds.txt'

def hash_password(password,salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def register_user(email,username, password):
    if username_exists(username):
        return False
    i=0
    x = ""
    while i<4:
        x = x + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        i=i+1
    salt = x
    hashed_password = hash_password(password, salt)
    
    with open(CREDENTIALS_FILE, 'a') as file:
        file.write(f"{email},{username},{hashed_password},{salt}\n")
    return True
    
def username_exists(username):
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    with open(CREDENTIALS_FILE, 'r') as file:
        for line in file:
            if line.split(',')[1] == username:
                return True
    return False

def verify_user(username, password):
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    with open(CREDENTIALS_FILE, 'r') as file:
        for line in file:
            stored_email, stored_username, stored_hash, stored_salt = line.strip().split(',')
            if stored_username == username:
                if stored_hash == hash_password(password, stored_salt):
                    return True
    return False


