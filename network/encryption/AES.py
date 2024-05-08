import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class AES:
    @staticmethod
    def encrypt(message: str, key: str) -> str:
        # Pad the message to be a multiple of 16 bytes (AES block size)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode())
        padded_data += padder.finalize()

        # Generate a random IV (Initialization Vector)
        iv = b"\x00" * 16  # You should generate a random IV in real-world scenarios

        # Create an AES cipher object
        cipher = Cipher(
            algorithms.AES(bytes(bytearray.fromhex(key))),
            modes.ECB(),
            backend=default_backend(),
        )

        # Encrypt the message
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return ciphertext.hex()

    @staticmethod
    def decrypt(ciphertext: str, key: str) -> str:
        # Create an AES cipher object
        cipher = Cipher(
            algorithms.AES(bytes(bytearray.fromhex(key))),
            modes.ECB(),
            backend=default_backend(),
        )

        # Decrypt the ciphertext
        decryptor = cipher.decryptor()
        padded_data = (
            decryptor.update(bytes(bytearray.fromhex(ciphertext)))
            + decryptor.finalize()
        )

        # Unpad the decrypted data
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data)
        data += unpadder.finalize()

        return data.decode("utf-8")


print(
    AES.decrypt(
        "7afab9c2d6be776f47e7e9203c1bfda1d1fba9d276065e44bfb2fe653510f9c67331057ef285ad99d7cc23c571885f0c083ca657eedd372e8de4861e81bc7ead7ad0c23ea52b11d5b41264f8920a785160c6986f04134905c69cd5430b366d5a",
        "b0d762c3548c039a30c3069e50503a5cddb2aed561dc2005d0b26399a299d48d",
    )
)
