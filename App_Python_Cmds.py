import os


# gets all file names in a certain folder (including extentions)
def get_all_file_names(folder_path):
    file_names = []

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            file_names.append(item)

    return file_names


# Check if the uploaded file has an allowed extension
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jfif', 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
