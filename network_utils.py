import socket
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import base64
from PIL import Image
import cv2
import io
import pickle


# returns  port
def get_network_info():
    return 5001


# class is used to recieve messages for both the server and client
class MessageReceiver:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def receive_message(self, aes_key):
        if (aes_key == None):
            msg_length = self.client_socket.recv(8)
            if msg_length == b"":
                return
            msg_length = int(msg_length.decode())
            received_message = b''
            while len(received_message) < msg_length:
                chunk = self.client_socket.recv(msg_length - len(received_message))
                if not chunk:
                    break
                received_message += chunk
            return received_message.decode()
        else:
            msg_length_encrypted = self.client_socket.recv(16)
            if msg_length_encrypted == b'':
                return
            msg_length = aes_decrypt(aes_key, msg_length_encrypted)
            msg_length = int(msg_length)
            received_message = b""
            while len(received_message) < msg_length:
                chunk = self.client_socket.recv(msg_length - len(received_message))
                if not chunk:
                    break
                received_message += chunk
            received_message = aes_decrypt(aes_key, received_message)
            return received_message


# class is used to send messages for both the server and client
class MessageSender:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def send_message(self, message, aes_key):

        if (aes_key == None):
            msg_length = len(message)
            msg_length_str = str(msg_length).zfill(8)
            self.client_socket.send(msg_length_str.encode('utf-8'))
            self.client_socket.send(message.encode('utf-8'))
        else:
            msg_encrypted = aes_encrypt(aes_key, message)
            msg_length = len(msg_encrypted)
            msg_length_str = str(msg_length).zfill(8)
            msg_length_str_encrypted = aes_encrypt(aes_key, msg_length_str)
            self.client_socket.send(msg_length_str_encrypted)
            self.client_socket.send(msg_encrypted)


# class is used to send files from the server
class FileSender:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def send_file(self, filename, aes_key):
        with open(filename, "rb") as f:
            file_data = f.read()
        file_data = aes_encrypt(aes_key, file_data)
        file_length = len(file_data)
        file_length_str = str(file_length).zfill(8)
        file_length_str = aes_encrypt(aes_key, file_length_str)
        self.client_socket.sendall(file_length_str)
        self.client_socket.sendall(file_data)
        print("File sent successfully")


# class is used to recieve files for the client
class FileReceiver:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def receive_file(self, file_name, aes_key):
        file_length_str = self.client_socket.recv(16)
        file_length_str = aes_decrypt(aes_key, file_length_str)
        print(file_length_str)
        file_length = int(file_length_str)
        received_data = b''
        while len(received_data) < file_length:
            chunk = self.client_socket.recv(file_length - len(received_data))
            if not chunk:
                break
            received_data += chunk
        received_data = aes_decrypt_file(aes_key, received_data)
        received_data = Image.open(io.BytesIO(received_data))
        new_file_path = f"Unsafe_Files/{file_name}"  # CHANGE LATER TO AN AGREED FILE STORAGE
        received_data.save(new_file_path)
        print("File received successfully")


# generates a random aes key
def generate_aes_key():
    return get_random_bytes(16)


# aes encryption for both files and regular messages
def aes_encrypt(key, message):
    cipher = AES.new(key, AES.MODE_ECB)

    if isinstance(message, bytes):
        padded_message = message + (AES.block_size - len(message) % AES.block_size) * b"\0"
    else:
        padded_message = message.encode('utf-8') + (
                AES.block_size - len(message.encode('utf-8')) % AES.block_size) * b"\0"

    ciphertext = cipher.encrypt(padded_message)
    return ciphertext


# aes decryption for regular messages
def aes_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    print(ciphertext)
    decrypted_message = cipher.decrypt(ciphertext)
    # Remove padding from decrypted message
    print(decrypted_message)

    unpadded_message = decrypted_message.rstrip(b"\0").decode('utf-8')
    print(unpadded_message)
    return unpadded_message


# aes decryption for files
def aes_decrypt_file(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = cipher.decrypt(ciphertext)
    # Remove padding from decrypted message
    print(decrypted_message)

    unpadded_message = decrypted_message.rstrip(b"\0")
    return unpadded_message


# send the rsa key to the client
def send_rsa_key(conn, key):
    key_data = key.exportKey()
    conn.send(key_data)


# recieves the rsa key
def receive_rsa_key(conn):
    key_data = conn.recv(2048)
    key = RSA.importKey(key_data)
    return key


# encrypts via rsa public key
def rsa_encrypt(public_key, message):
    if isinstance(message, str):
        message = message.encode()
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message)
    return encrypted_message


# decrypts via private key
def rsa_decrypt(private_key, encrypted_message):
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(encrypted_message)
    try:
        return decrypted_message.decode('utf-8')  # Attempt to decode as UTF-8
    except UnicodeDecodeError:
        return decrypted_message  # Return bytes if decoding fails
