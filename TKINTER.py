import tkinter as tk
from tkinter import messagebox
import threading
from Client import *
from network_utils import *
from tkinter import ttk
import os
from PIL import Image, ImageTk

# checks with the server whether the login credentials are correct
def login():
    username = username_entry.get()
    password = password_entry.get()

    send("confirm_login", aes_key)
    send(username, aes_key)
    send(password, aes_key)
    IsLoginCorrect = recv(aes_key)
    if (IsLoginCorrect == "Correct"):
        login_window.destroy()
        gui_thread = threading.Thread(target=run_gui)
        gui_thread.start()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

#opens the main tkinter page
def run_gui():
    import tkinter as tk
    from tkinter import filedialog
    import shutil
    import webbrowser
    import os


    #opens link in a browser
    def open_link(event):
        webbrowser.open("https://www.virustotal.com/gui/home/upload")

    #clears unsafe_files folder form all files
    def clear_folder():
        folder_path = f"{os.getcwd()}/Unsafe_Files"
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    #send the server a message indicating the file is safe and then deletes it
    def IsSafe():
        send("IsSafe", aes_key)
        clear_folder()

    # send the server a message indicating the file is not safe and then deletes it
    def IsntSafe():
        send("IsntSafe", aes_key)
        clear_folder()

    #requests a file from the server
    def Get_File():
        MessageSender(client_socket).send_message("recieve_file", aes_key)
        file_name = MessageReceiver(client_socket).receive_message(aes_key)
        if (file_name != "The folder is empty."):
            FileReceiver(client_socket).receive_file(file_name, aes_key)
            return file_name
        else:
            messagebox.showerror("Error", "No more pending files")
        return None

    #presents to the admin the visual presentation of the map file
    def show_image():
        folder_path = f"{os.getcwd()}//Unsafe_Files"
        files = os.listdir(folder_path)
        if files:
            first_file = files[0]
            img = Image.open(f"{os.getcwd()}//Unsafe_Files/{first_file}")
            img = img.resize((125, 125))
            img_tk = ImageTk.PhotoImage(img)

            img_label = tk.Label(root, image=img_tk)
            img_label.image = img_tk
            img_label.pack(pady=20)






    #further lines are all for managing the user interface for after he logs in
    root = tk.Tk()
    root.title("Validate Maps")

    title_label = ttk.Label(root, text="Step 1: Press the 'download' button")
    title_label.pack(pady=10)

    copy_button = ttk.Button(root, text="Download", command=Get_File)
    copy_button.pack(pady=10)

    title_label = ttk.Label(root,
                            text="Step 2: Check in the website 'virustotal.com' whether the file has malicious content")
    title_label.pack(pady=10)

    text_widget = tk.Text(root, wrap="word", height=1, borderwidth=0, highlightthickness=0)
    text_widget.pack()
    text_widget.insert("1.0", "Click here to enter virustotal.com")
    text_widget.tag_configure("hyperlink", foreground="blue", underline=True)
    text_widget.tag_bind("hyperlink", "<Button-1>", open_link)
    text_widget.tag_add("hyperlink", "1.0", "1.end")

    title_label = ttk.Label(root,
                            text="Step 3: Check that the image has no malicious visual content")
    title_label.pack(pady=10)

    image_button = ttk.Button(root, text="Show Image", command=show_image)
    image_button.pack(pady=20)


    title_label = ttk.Label(root, text="Step 4.1: if file is indeed secure, press 'secure'")
    title_label.pack(pady=10)

    secure_button = ttk.Button(root, text="Secure", command=IsSafe)
    secure_button.pack(pady=10)

    message_label = tk.Label(root, text="")
    message_label.pack(pady=5)

    title_label = ttk.Label(root, text="Step 4.2: if file is not secure, press 'not secure' ")
    title_label.pack(pady=10)

    not_secure_button = ttk.Button(root, text="Not Secure", command=IsntSafe)
    not_secure_button.pack()

    status_label = tk.Label(root, text="", fg="black")
    status_label.pack()

    root.mainloop()

#connects to the server
client_socket, aes_key = connect_to_server()

send = MessageSender(client_socket).send_message
recv = MessageReceiver(client_socket).receive_message
recv_file = FileReceiver(client_socket).receive_file

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

style = ttk.Style()

style.theme_use("clam")

username_label = ttk.Label(login_window, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_entry = ttk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = ttk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_entry = ttk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = ttk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, columnspan=2, padx=5, pady=5)

login_window.mainloop()
