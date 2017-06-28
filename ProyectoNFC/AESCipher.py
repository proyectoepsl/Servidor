import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome import Random


class AESCipher:

    def __init__(self):
        key = b'this is my key'
        self.bs = int(16)
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, message):
        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(message)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        print(len(s))
        print(self.bs)
        print(s)
        print(type(s))
        return s + ((self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)).encode()

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
'''
key = b'this is my key'
mensaje = b'this is local test'

mensajeEncriptado=AESCipher(key).encrypt(mensaje)
print(mensajeEncriptado)

mensajeEncriptado=b'X9G5cBZ5/Hvcqez9fjsIM6RARpYUnoTOb5cdCW9FzJFhKcA+2EEsl0pEpBVNBSMr'

mensajeDesencriptado=AESCipher(key).decrypt(mensajeEncriptado)
print(mensajeDesencriptado)
'''