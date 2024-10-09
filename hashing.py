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
 # Store in file (username, hashed_password, salt)      ````    
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

def change_username(new_username,username):
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    with open(CREDENTIALS_FILE, 'r') as file:
        lines = file.readlines()
    with open(CREDENTIALS_FILE, 'w') as file:
        for line in lines:
            if line.split(',')[1] == username:
                line.split(',')[1] = new_username
                file.write(line)
            else:
                file.write(line)
    return True

def change_password(username,email,new_password):
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    salt = ""
    i=0
    x = ""
    while i<7:
        x = x + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        i=i+1
    salt = x
    hashed_password = hash_password(new_password, salt)
    with open(CREDENTIALS_FILE, 'r') as file:
        lines = file.readlines()
    with open(CREDENTIALS_FILE, 'w') as file:
        for line in lines:
            if line.split(',')[0] == email and line.split(',')[1] == username:
                file.write(f"{email},{username},{hashed_password},{salt}\n")
            else:
                print("Username or email not found")
                file.write(lines)
    return True
