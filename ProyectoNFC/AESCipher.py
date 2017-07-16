import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome import Random


class AESCipher:
    #Encriptacion de la clave
    def __init__(self):
        key = b'this is my key'
        self.bs = int(16)
        self.key = hashlib.sha256(key).digest()
    #Encriptacion de los datos
    def encrypt(self, message):
        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(message)).decode('utf-8')
    #Desencritar los datos
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
    #Formateo de los datos
    def _pad(self, s):
        print(len(s))
        print(self.bs)
        print(s)
        print(type(s))
        return s + ((self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)).encode()

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
