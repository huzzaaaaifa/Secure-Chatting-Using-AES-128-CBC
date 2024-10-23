import hashlib
import random
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

PRIME = 999331 # any long long prime number
a = random.randint(1, PRIME-1)
if ((a ** (PRIME-1) % PRIME)) == 1:
    is_prime = True
else:
    is_prime = False

if (not (is_prime)):
    print("NUMBER IS NOT PRIME")
    exit()

ALPHA = 4971


def generate_public_private_key():
    private_key = random.randint(2, PRIME - 2)
    public_key = (ALPHA ** private_key) % PRIME
    return private_key, public_key


def calculate_shared_secret(others_public_key, my_private_key):
    shared_secret = (others_public_key ** my_private_key) % PRIME
    return shared_secret


class AES128:
    def __init__(self, shared_key, username = ""):
        shared_key = username + str(shared_key)
        self.key = hashlib.sha256(str(shared_key).encode('utf-8')).digest()[:16] 
    
    def encrypt(self, data):
        IV = get_random_bytes(AES.block_size)
        encryption_cipher = AES.new(self.key, AES.MODE_CBC, IV)
        return IV + encryption_cipher.encrypt(pad(data, AES.block_size))


    def decrypt(self, data):
        IV = data[:AES.block_size]
        decryption_cipher = AES.new(self.key, AES.MODE_CBC, IV)
        return unpad(decryption_cipher.decrypt(data[AES.block_size:]), AES.block_size)

