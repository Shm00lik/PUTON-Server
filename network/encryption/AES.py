from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib


class AES:
    """
    A class providing AES encryption and decryption functionalities.
    """

    @staticmethod
    def encrypt(message: str, key: str) -> str:
        """
        Encrypts a message using AES encryption.

        Args:
        - message (str): The message to encrypt.
        - key (str): The encryption key.

        Returns:
        - str: The hexadecimal representation of the encrypted ciphertext.
        """

        # Pad the message to be a multiple of 16 bytes (AES block size)
        padded_data = AES.pad(message.encode())

        # Create an AES cipher object
        cipher = Cipher(
            algorithms.AES(bytes.fromhex(key)),
            modes.ECB(),
            backend=default_backend(),
        )

        # Encrypt the message
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return ciphertext.hex()

    @staticmethod
    def decrypt(ciphertext: str, key: str) -> str:
        """
        Decrypts a ciphertext using AES decryption.

        Args:
        - ciphertext (str): The hexadecimal representation of the ciphertext.
        - key (str): The decryption key.

        Returns:
        - str: The decrypted message.
        """

        # Create an AES cipher object
        cipher = Cipher(
            algorithms.AES(bytes.fromhex(key)),
            modes.ECB(),
            backend=default_backend(),
        )

        # Decrypt the ciphertext
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(bytes.fromhex(ciphertext)) + decryptor.finalize()

        try:
            # Unpad the decrypted data
            data = AES.unpad(padded_data)
        except:
            # If unpadding fails, return the unpadded data directly
            return padded_data.decode("utf-8")

        return data.decode("utf-8")

    @staticmethod
    def pad(message: bytes) -> bytes:
        """
        Pads a message to be a multiple of 16 bytes (AES block size).

        Args:
        - message (bytes): The message to pad.

        Returns:
        - bytes: The padded message.
        """
        length_to_pad = 16 - (len(message) % 16)
        return message + bytes([length_to_pad] * length_to_pad)

    @staticmethod
    def unpad(message: bytes) -> bytes:
        """
        Unpads a padded message.

        Args:
        - message (bytes): The padded message.

        Returns:
        - bytes: The unpadded message.
        """
        return message[: -message[-1]]

    @staticmethod
    def diffie_hellman_key_to_aes_key(diffie_hellman_key: int) -> str:
        """
        Converts a Diffie-Hellman key to an AES key using SHA-256 hashing.

        Args:
        - diffie_hellman_key (int): The Diffie-Hellman key.

        Returns:
        - str: The AES key obtained from the Diffie-Hellman key.
        """
        return hashlib.sha256(str(diffie_hellman_key).encode()).hexdigest()


if __name__ == "__main__":
    # Example usage
    print(
        AES.decrypt(
            "4567110c831a884bf32c4bf61cb71762ab83fc9ff19bdd6e0b00d3ae710ce9cd65a647ecef0f1aa7d97109cf39c1c2cdeb617f032eaba2c6c050502968803a4cd044d1319b293b0ddfc12cc3e70a95e9dc3a1314801f39fda03bb3047ebc197fa7393b3d07fb98d40d3feecd4c03a13e5cf16c55f73669afcdd323379dfc5bc33e11b12d61350a6c4e2a88e849baf38f8f9672166432b3468f694800b8efe26eafac96263fecc7d09fd4e4efd614e8dc",
            "cbcb39ec3120f36f31c442281c6051f30b605ffa9f468ac06ee596f52a43357e",
        )
    )
