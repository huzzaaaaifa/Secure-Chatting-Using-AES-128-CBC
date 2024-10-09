import socket
from encryption import generate_public_private_key, calculate_shared_secret, AES128
import datetime
import getpass
import re

def validate_username(username):

    if not re.search(r"[0-9]", username):  
        return False, "Username must contain at least one digit"

    if not re.match(r"^[a-zA-Z0-9]+$", username):  
        return False, "Username can only contain alphanumeric characters (no special characters)"

    return True, ""


def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*]", password):
        return False
    return True

def create_socket():
    # create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # setup an address
    server_address = ('localhost', 8082)
    sock.connect(server_address)

    return sock


def main():
    print("\n\t>>>>>>>>>> FAST University Chat Client <<<<<<<<<<\n\n")

    # Create socket and connect to the server
    sock = create_socket()

    loggedIN = False
    
    rules = sock.recv(1024).decode('utf-8')
    
    print(rules)

    while True:
        action = input("Enter 'register' or 'login': ").strip()

        if action == "register":

            sock.send(action.encode('utf-8'))
            client_private_key, client_public_key = generate_public_private_key()

            server_public_key = int(sock.recv(256).decode('utf8'))

            sock.send(str(client_public_key).encode('utf8'))

            shared_registration_key = calculate_shared_secret(
                server_public_key, client_private_key)

            username_prompt = sock.recv(256).decode('utf-8')
            print(username_prompt)
            username = input().strip()
            
            while True:
                is_valid, error_message = validate_username(username)

                if not is_valid:
                    print(error_message)
                else:
                    break  
        
                username = input("Enter a valid username: ").strip()

            
            msg = username.encode('utf-8')

            aes_cipher = AES128(shared_registration_key)

            encrypted_message = aes_cipher.encrypt(msg)

            sock.send(encrypted_message)

            email_prompt = sock.recv(256).decode('utf-8')
            print(email_prompt)
            while True:
                email = input().strip()
                if '@' in email:
                    at_position = email.index('@')
                    result = email[at_position:]
                    if result == "@isb.nu.edu.pk":
                        break
                else:
                    print("Not Valid Email\nEnter Again\n")
                    print(email_prompt)

            msg = email.encode('utf-8')

            aes_cipher = AES128(shared_registration_key)

            encrypted_message = aes_cipher.encrypt(msg)

            sock.send(encrypted_message)

            password_prompt = sock.recv(256).decode('utf-8')
            
            password = getpass.getpass()
            
            while not validate_password(password):
                print("Password is not according to Rules\n Enter Again\n")
                password = getpass.getpass()
            
            msg = password.encode('utf-8')

            aes_cipher = AES128(shared_registration_key)

            encrypted_message = aes_cipher.encrypt(msg)

            sock.send(encrypted_message)

            response = sock.recv(256).decode('utf-8')
            print(response)

            if "successful" in response:
                print("Now you can log in")
                continue

        elif action == "login":
            sock.send(action.encode('utf-8'))
            client_private_key, client_public_key = generate_public_private_key()

            server_public_key = int(sock.recv(256).decode('utf8'))

            sock.send(str(client_public_key).encode('utf8'))

            shared_login_key = calculate_shared_secret(
                server_public_key, client_private_key)

            response = sock.recv(256).decode('utf-8')
            print(response)
            username = input().strip()
            
            while True:
                is_valid, error_message = validate_username(username)

                if not is_valid:
                    print(error_message)
                else:
                    break 
        
                username = input("Enter a valid username: ").strip()
            
            
            msg = username.encode('utf-8')

            aes_cipher = AES128(shared_login_key)

            encrypted_message = aes_cipher.encrypt(msg)

            sock.send(encrypted_message)

            response = sock.recv(256).decode('utf-8')
            
            password = getpass.getpass()

            msg = password.encode('utf-8')

            aes_cipher = AES128(shared_login_key)

            encrypted_message = aes_cipher.encrypt(msg)

            sock.send(encrypted_message)

            response = sock.recv(256).decode('utf-8')

            if "successful" in response:
                print("Login successful! You can now start chatting")
                loggedIN = True
                break

        else:
            print("Invalid input!!! Please enter 'register' or 'login'")
            continue
    print("\n\n\n")

    if (loggedIN):

        client_private_key, client_public_key = generate_public_private_key()

        server_public_key = int(sock.recv(256).decode('utf8'))

        sock.send(str(client_public_key).encode('utf8'))

        shared_secret_key = calculate_shared_secret(
            server_public_key, client_private_key)

        while True:
            # Get user input and send it to the server
            message = input(f"You {username} : ").strip()
            
            msg = message.encode('utf-8')

            aes_cipher = AES128(shared_secret_key,username)

            encrypted_message = aes_cipher.encrypt(msg)

            sock.send(encrypted_message)
            # Send the message to the server

            # If the client sends "exit", terminate the chat
            if message == "exit":
                print("You disconnected from the chat...")
                break

            # receive response from server
            response = sock.recv(256)
                   
            aes_cipher = AES128(shared_secret_key,username)
            
            decrypted = aes_cipher.decrypt(response)
            
            decrypted_message = decrypted.decode('utf-8')
            
            now = datetime.datetime.now()
            
            print("Server: ", decrypted_message,"\t",now.strftime("%Y-%m-%d %H:%M:%S"))

    # Close the socket after communication
        sock.close()
    else:
        print("Failed to login!! Please try again")
        sock.close()


if __name__ == "__main__":
    main()
