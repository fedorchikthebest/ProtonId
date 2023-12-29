import gostcrypto
import base64


def b64encrypt(data: str, key: str) -> str:

    key = bytearray(key.encode('utf-8'))

    plain_text = bytearray(str(data).encode('utf-8'))

    cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                           key,
                                           gostcrypto.gostcipher.MODE_ECB,
                                           pad_mode=gostcrypto.gostcipher.PAD_MODE_1)

    cipher_text = cipher_obj.encrypt(plain_text)

    return base64.b64encode(cipher_text).decode('utf-8')


def b64decrypt(data: str, key: str) -> str:

    key = bytearray(key.encode('utf-8'))

    plain_text = bytearray(base64.b64decode(data))

    cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                           key,
                                           gostcrypto.gostcipher.MODE_ECB,
                                           pad_mode=gostcrypto.gostcipher.PAD_MODE_1)

    decrypt_text = cipher_obj.decrypt(plain_text)

    return decrypt_text.decode('utf-8').replace(b'\x00'.decode('utf-8'), '')