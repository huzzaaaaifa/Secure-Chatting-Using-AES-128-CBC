import socket
import os
import datetime
from encryption import generate_public_private_key, calculate_shared_secret, AES128
from hashing import register_user, verify_user, username_exists, change_username, change_password

def print_rules(client_socket):
    rules = """
    
    Please review the following rules before you register or log in:

    1. Username Policy:
        Must be between 3 and 20 characters
        No spaces allowed

    2. Password Policy:
       Minimum of 8 characters
       Must include at least:
          1 uppercase letter
          1 lowercase letter
          1 number
          1 special character (!@#$%^&*)

    3. Data Security:
        All communications are encrypted for security


    4. Session Timeout:
        If you're inactive for 15 minutes, you will be logged out automatically

    5. Behavior:
        Please refrain from using inappropriate language
        Any inappropriate messages will result in a ban

    6. Privacy:
        Your credentials and messages are encrypted and secure

    """
    client_socket.send(rules.encode('utf-8'))


def main():
    print("\n\t>>>>>>>>>> FAST University Chat Server <<<<<<<<<<\n\n")

    # create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # define the server address
    server_address = ('', 8082)

    # bind the socket to the specified IP and port
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("Server started and waiting for clients to connect...")

    while True:
        # accept incoming connections
        client_socket, client_address = server_socket.accept()
        print(f"Client connected from {client_address}")

        # create a new process to handle the client
        pid = os.fork()
        if pid == -1:
            print("Error! Unable to fork process.")
        elif pid == 0:
            # child process handles the client
            handle_client(client_socket)
            os._exit(0)
        else:
            # parent process continues accepting clients
            client_socket.close()

def handle_client(client_socket):

    loggedIn = False
    print("Waiting for client to choose login or registration...")
    
    print_rules(client_socket)

    while True:
        method = client_socket.recv(256).decode('utf-8')
        print(f"Client selected method: {method}")

        if method == "register":
            print("Client selected registration process...")
            server_private_key, server_public_key = generate_public_private_key()

            client_socket.send(str(server_public_key).encode('utf-8'))

            client_public_key = int(client_socket.recv(256).decode('utf-8'))

            shared_registration_key = calculate_shared_secret(client_public_key, server_private_key)

            client_socket.send("Username: ".encode('utf-8'))
            username = client_socket.recv(256)

            aes_cipher = AES128(shared_registration_key)
            decrypted = aes_cipher.decrypt(username)
            username = decrypted.decode('utf-8')

            print(f"Client provided username: {username}")

            client_socket.send("Email: ".encode('utf-8'))
            email = client_socket.recv(256)

            aes_cipher = AES128(shared_registration_key)
            decrypted = aes_cipher.decrypt(email)
            email = decrypted.decode('utf-8')

            print(f"Client provided email: {email}")

            client_socket.send("Password: ".encode('utf-8'))
            password = client_socket.recv(256)

            aes_cipher = AES128(shared_registration_key)
            decrypted = aes_cipher.decrypt(password)
            password = decrypted.decode('utf-8')

            print(f"Client provided password (encrypted): {password}")

            if register_user(email, username, password):
                client_socket.send("Registration successful You can now login\n".encode('utf-8'))
                print("Registration successful")
            else:
                client_socket.send("Username already exists Please try again\n".encode('utf-8'))
                print("Username already exists Registration failed")

        elif method == "login":
            print("Client selected login process...")
            server_private_key, server_public_key = generate_public_private_key()

            client_socket.send(str(server_public_key).encode('utf-8'))
            client_public_key = int(client_socket.recv(256).decode('utf-8'))

            shared_login_key = calculate_shared_secret(client_public_key, server_private_key)

            client_socket.send("Username: ".encode('utf-8'))
            username = client_socket.recv(256)

            aes_cipher = AES128(shared_login_key)
            decrypted = aes_cipher.decrypt(username)
            username = decrypted.decode('utf-8')

            client_socket.send("Password: ".encode('utf-8'))
            password = client_socket.recv(256)

            aes_cipher = AES128(shared_login_key)
            decrypted = aes_cipher.decrypt(password)
            password = decrypted.decode('utf-8')

            print(f"Client attempting to log in with username: {username}")

            if verify_user(username, password):
                client_socket.send("Login successful\n".encode('utf-8'))
                loggedIn = True
                print(f"Login successful for user: {username}")
                break
            else:
                client_socket.send("Invalid credentials Please try again\n".encode('utf-8'))
                print("Invalid credentials. Login attempt failed")

        else:
            client_socket.send("INVALID INPUT".encode('utf-8'))
            print("Invalid method selected by client")
            
    print("\n\n\n")

    if loggedIn:
        server_private_key, server_public_key = generate_public_private_key()

        client_socket.send(str(server_public_key).encode('utf-8'))

        client_public_key = int(client_socket.recv(256).decode('utf-8'))

        shared_secret_key = calculate_shared_secret(client_public_key, server_private_key)

        while True:
            # receive message from the client
            message = client_socket.recv(256)

            aes_cipher = AES128(shared_secret_key, username)
            decrypted = aes_cipher.decrypt(message)
            decrypted_message = decrypted.decode('utf-8')

            # if client sends "exit", close the connection
            if decrypted_message == "exit":
                print(f"Client {username} disconnected.")
                break

            now = datetime.datetime.now()
            print(f"{username}: {decrypted_message} \t {now.strftime('%Y-%m-%d %H:%M:%S')}")

            # send a response back to the client
            response = input("You (Server): ").strip()

            msg = response.encode('utf-8')

            aes_cipher = AES128(shared_secret_key, username)
            encrypted_message = aes_cipher.encrypt(msg)

            client_socket.send(encrypted_message)

        client_socket.close()
    else:
        client_socket.close()
        print("Client not logged in. Connection closed.")

if __name__ == "__main__":
    main()
