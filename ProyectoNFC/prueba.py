#import .AESCipher

"""
def main():


    hola=b'this is local test'
    mensaje=AESCipher.encrypt(hola)
    salida=AESCipher.decrypt(mensaje)
    print(mensaje)
    print(salida)

if __name__ == '__main__':
    main()

#prueba fran Encriptar
from Cryptodome.Cipher import AES
from Cryptodome import Random
key = b'Sixteen byte key'
print(key)
b'Sixteen byte key'
#iv = Random.new().read(AES.block_size)
iv = b'jD[\\;\xe9f@W&\xe1b]\xbav\x9f'
print('jD[\\;\xe9f@W&\xe1b]\xbav\x9f'.encode().hex())
cipher = AES.new(key, AES.MODE_CFB, iv)
msg = cipher.encrypt(b'A la Eva No me gusta la cerveza')
print(msg)

cipher2 = AES.new(key, AES.MODE_CFB, iv)
print(cipher2.decrypt(msg))
"""

from .AESCipher import AESCipher
encrip = AESCipher()


