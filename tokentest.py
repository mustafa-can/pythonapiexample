from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import hashlib
import base64

class SecureToken:
    @staticmethod
    def tokenencrypt(data, secret_key, secret_iv):
        key = hashlib.sha256(secret_key.encode('utf-8')).digest()
        iv = hashlib.sha256(secret_iv.encode()).digest()[:16]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)  # PKCS7 padding
        encrypted_data = cipher.encrypt(padded_data.encode())
        
        return base64.b64encode(encrypted_data).decode("utf-8")
    
    @staticmethod
    def tokendecrypt(data, secret_key, secret_iv):
        # Hash the secret key and IV using SHA-256
        key = hashlib.sha256(secret_key.encode()).digest()
        iv = hashlib.sha256(secret_iv.encode()).digest()[0:16]
        
        # Decrypt the data using AES-256-CBC decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt( base64.b64decode(data) )
        padding_length = decrypted_data[-1]
        unpadded_data = decrypted_data[:-padding_length]
        
        return unpadded_data.decode()

# Example usage:
encrypted_data = "I4ITBFHFL5FrFxCUOpRXLA=="  # Replace with your encrypted data
secret_key = "thisismysecretkey"
secret_iv = "www.mysite.com"

decrypted_data = SecureToken.tokendecrypt(encrypted_data, secret_key, secret_iv)
print("ecrypted data:", SecureToken.tokenencrypt('test:testuserps', secret_key, secret_iv))
print("Decrypted data:", decrypted_data)
