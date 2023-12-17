import os

def directory_exists(file_path):
    """
    Ensure that the directory for the given file path exists.
    If the directory does not exist, it is created.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
