import os
def print_to_new_file(file_path: str, file_name: str, content) :
    ensure_directory(file_path)
    with open(f'{file_path}/{file_name}', 'w') as f:
        f.write(content)

def print_to_new_file_bytes(file_path: str, file_name: str, content) :
    ensure_directory(file_path)
    with open(f'{file_path}/{file_name}', 'wb') as f:
        f.write(content)

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)