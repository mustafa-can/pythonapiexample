from Crypto.Cipher import AES
#from Crypto.Util.Padding import unpad, pad
import base64, hashlib

class SecureToken:
    secret_key = b'thisismysecretkey' 
    secret_iv = b'www.mysite.com'     
    encrypt_method = "AES-256-CBC"

    @staticmethod
    def tokenencrypt(data):
        key = hashlib.sha256(SecureToken.secret_key).digest()
        iv = hashlib.sha256(SecureToken.secret_iv).digest()[:16]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)  # PKCS7 padding
        encrypted_data = cipher.encrypt(padded_data.encode())
        
        return base64.b64encode(encrypted_data).decode("utf-8")

    @staticmethod
    def tokendecrypt(data):
        key = hashlib.sha256(SecureToken.secret_key).digest()
        iv = hashlib.sha256(SecureToken.secret_iv).digest()[0:16]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt( base64.b64decode(data) )
        padding_length = decrypted_data[-1]
        unpadded_data = decrypted_data[:-padding_length]
               
        return unpadded_data.decode()