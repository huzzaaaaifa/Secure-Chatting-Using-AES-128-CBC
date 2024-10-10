# Secure-Chatting-Using-AES-128-CBC


A secure real-time chat system using **AES-128-CBC** encryption to protect the confidentiality of messages.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Encryption Details](#encryption-details)
- [Limitations](#limitations)

## Features

- **AES-128-CBC Encryption:** Encrypts messages to ensure data confidentiality.
- **Random IV Generation:** A unique Initialization Vector (IV) is generated for each message.
- **End-to-End Encryption:** Only the intended recipient can decrypt the message.
- **Real-Time Chatting:** Secure communication between clients in real time.
- **User Authentication:** Basic user authentication for secure access.

## Technologies Used

- **Python** for socket programming and encryption implementation.
- **AES-128-CBC** for secure encryption.
- **Sockets** for real-time communication between clients and the server.
- **Hashing** for securily storing passwords.
- **Deffie-Helmen Key Exchange Mechanism** for securily exchanging the client and server's public keys.

## How It Works

1. **Encryption:** The system uses **AES-128-CBC** to encrypt the plaintext message using a shared key and a randomly generated Initialization Vector (IV) before sending it. For the chatting part key is changed and appened with each user's username to increase security.
2. **Decryption:** The recipient decrypts the received message using the shared key and IV to retrieve the original message.
3. **Transmission:** Encrypted messages are transmitted over the network using socket programming.
4. **IV Handling:** Each message is sent with its corresponding IV, which is used by the recipient for decryption.

## Installation

### Prerequisites
- **Python 3.x**
- Required Python libraries (listed in `requirements.txt`)

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/huzzaaaaifa/Secure-Chatting-Using-AES-128-CBC.git
   cd Secure-Chatting-Using-AES-128-CBC
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

In one terminal, start the server:
```bash
python server.py
```

### Running the Client

In another terminal, start the client:
```bash
python client.py
```

The client will prompt you to input messages, which will be encrypted and sent to the server, then forwarded to the recipient.

## Encryption Details

- **AES-128-CBC**: We use AES with a 128-bit key in CBC mode for encryption.
- **IV Generation**: A new, random Initialization Vector (IV) is generated for each message, ensuring that even identical messages appear different in ciphertext.
- **Decryption**: The recipient uses the AES key and IV to decrypt the message and retrieve the original plaintext.


## Limitations

- No Rate Limiting for Login Attempts: Multiple login attempts can be made without restriction, making it susceptible to brute-force attacks.
- Insecure Email Validation: The email validation is done simply by checking the presence of "@isb.nu.edu.pk", which is weak and could allow bypassing with similar addresses.
- No Logging: Important events, like login failures or registration errors, are only printed to the console and not logged for future analysis or monitoring.
- Unprotected Password Storage: The server doesn't check or limit the number of failed login attempts, which makes it vulnerable to brute-force attacks.
- Weak Diffie-Hellman Implementation: The prime number PRIME and generator ALPHA are hardcoded and relatively small. This weakens the security of the Diffie-Hellman key exchange.
- File-Based Storage: Credentials are stored in a text file (creds.txt), which is not secure for sensitive data like passwords. A database with proper access control should be used instead.

-----------------------------------------------------------------------
