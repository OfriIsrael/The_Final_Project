import select
from threading import Thread
from network_utils import *
import socket
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from server_cmds import *
from Data import check_credentials


# manages the messages sent by the client and returns how to deal with them
def client_manager(client_socket: socket.socket):
    send = MessageSender(client_socket).send_message
    recv = MessageReceiver(client_socket).receive_message
    send_file = FileSender(client_socket).send_file
    aes_key = None
    while True:
        if (aes_key == None):
            data = recv(None)
        else:
            data = recv(aes_key)
        if data == "leave":
            break
        if data == "confirm_login":
            username = recv(aes_key)
            password = recv(aes_key)
            if (check_credentials(username, password)):
                send("Correct", aes_key)
            else:
                send("Incorrect", aes_key)
        if data == "recieve_file":
            print(get_first_file_name())
            send(get_first_file_name(), aes_key)
            if (get_first_file_name() != "The folder is empty."):
                send_file(get_first_file_in_folder(), aes_key)
        if data == "startconvo":
            server_key = RSA.generate(2048)
            send_rsa_key(client_socket, server_key.publickey())
            encrypted_aes_key = client_socket.recv(2048)
            aes_key = rsa_decrypt(server_key, pickle.loads(encrypted_aes_key))
            print(aes_key)
        if (data == "IsSafe"):
            File_location = get_first_file_name()
            transfer_file(f"{os.getcwd()}/Unsafe_Files_Server/{File_location}", f"{os.getcwd()}/static/{File_location}")
        if (data == "IsntSafe"):
            File = get_first_file_in_folder()
            delete_file(File)
    client_socket.close()


# fucntion to check credntials


# runs socket server which listens to clients, and then directs them to a threaded client manager
def server_run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', get_network_info()))
        print("listening")
        server_socket.listen()
        while True:
            client_socket, client_address = server_socket.accept()

            Thread(target=client_manager, args=(client_socket,)).start()


server_run()
