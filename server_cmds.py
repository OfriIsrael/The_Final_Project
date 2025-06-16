from Data import *
import os
import shutil

#gets the first filename of the designated folder
def get_first_file_name():
    folder_path = f"{os.getcwd()}//Unsafe_Files_Server"

    # List all files in the folder
    files = os.listdir(folder_path)

    if files:  # Check if there are any files in the folder
        first_file = files[0]  # Get the first file
        return first_file
    else:
        return("The folder is empty.")

#deletes first file in the designated folder
def delete_file(file_path):
    try:
        print (file_path)
        if (file_path != None):
            os.remove(file_path)
    except OSError as e:
        print(f"Error deleting file '{file_path}': {e}")

#transfers file from one folder to another
def transfer_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        print(f"File transferred successfully from '{source_path}' to '{destination_path}'.")
    except Exception as e:
        print(f"Error transferring file: {e}")

#gets the first file in the unsafe_files_server folder
def get_first_file_in_folder():
    # Get a list of all files in the folder
    # folder_path = 'C:/The_Final_Project (2)/The_Final_Project/Unsafe_Files'
    folder_path = f"{os.getcwd()}/Unsafe_Files_Server"
    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):
            # Open the file and return the file object
            # return open(file_path, 'rb').read()  # 'rb' opens the file in binary mode
            return file_path

    return None
