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
            "4567110c831a884bf32c4bf61cb71762ab83fc9ff19bdd6e0b00d3ae710ce9cd65a647ecef0f1aa7d97109cf39c1c2cdeb617f032eaba2c6c050502968803a4cd044d1319b293b0ddfc12cc3e70a95e9dc3a1314801f39fda03bb3047ebc197fa7393b3d07fb98d40d3feecd4c03a13e5cf16c55f73669afcdd323379dfc5bc33e11b12d61350a6c4e2a88e849baf38f8f9672166432b3468f694800b8efe26eafac96263fecc7d09fd4e4efd614e8dc",
            "cbcb39ec3120f36f31c442281c6051f30b605ffa9f468ac06ee596f52a43357e",
        )
    )
