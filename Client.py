from network_utils import *
import socket


# client command for conencting with the server
def connect_to_server():  # Connects to the server and exchanges keys on the way
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', get_network_info()))  # CHANGE IP ACCORDING TO CURRENT SERVER IP
    MessageSender(client_socket).send_message("startconvo", None)
    server_key = receive_rsa_key(client_socket)
    aes_key = generate_aes_key()
    encrypted_aes_key = rsa_encrypt(server_key, aes_key)
    client_socket.send(pickle.dumps(encrypted_aes_key))
    return [client_socket, aes_key]
