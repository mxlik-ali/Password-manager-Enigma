from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto import Random
import base64

def encrypt(key, source, encode=True, keyType='hex'):
    '''
    Parameters:
    key - The key used for encryption (hex representation or ASCII string).
    source - The message or data to encrypt.
    encode - Whether to encode the output in base64. Default is True.
    keyType - Specify the type of key passed.

    Returns:
    Base64 encoded cipher.
    '''
    source = source.encode()  # Convert source to bytes
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC,iv)
    encrypted_cipher = cipher.encrypt(pad(source, AES.block_size))
    return base64.b64encode(encrypted_cipher).decode() if encode else encrypted_cipher

def decrypt(key, encrypt_pass, decode=True, keyType='hex'):
    encrypt_pass = encrypt_pass.encode()
    if decode:
        encrypt_pass = base64.b64decode(encrypt_pass)
    
    
    # Convert the key to bytes if it's provided as a hex string
    if keyType == "hex":
        key = bytes.fromhex(key)
    iv = encrypt_pass[:AES.block_size]
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(encrypt_pass[AES.block_size:]), AES.block_size)
        return decrypted_data  # Decode the decrypted bytes to a string
    except ValueError as e:
        print(f"Decryption error: {e}")
        return None  # Return None or handle the decryption failure accordingly

