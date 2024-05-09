from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import hashlib


class AES:
    @staticmethod
    def encrypt(message: str, key: str) -> str:
        # Pad the message to be a multiple of 16 bytes (AES block size)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode())
        padded_data += padder.finalize()

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

        try:
            # Unpad the decrypted data
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data)
            data += unpadder.finalize()
        except:
            return data.decode("utf-8")

        return data.decode("utf-8")

    @staticmethod
    def diffie_hellman_key_to_aes_key(diffie_hellman_key: int) -> str:
        return hashlib.sha256(str(diffie_hellman_key).encode()).hexdigest()


if __name__ == "__main__":
    print(
        AES.decrypt(
            "6be324dc043e75eed2e43c9aad23e8d15eede7571ebc81dfb5445447b879db49a81afb0814c73f4ad8913ee6cc21c4ec9e31b6610955c0ccae4fde9306cfde96cf9066df5f9ecb1760e3eb4efbd4d991",
            "916a889f901e2463c409c09b7766525dd0d8b6d0d26fecdb03d217b17638d6b4",
        )
    )
