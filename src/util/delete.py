"""
Secure deletion module.

:author: Max Milazzo
"""


import os
import subprocess


def secure_delete(file_path, passes=10):
    """
    Overwrite the file with random data before deleting it.

    :param file_path: the path to the file to be securely deleted
    :param passes: number of times to overwrite the file
    """

    if os.path.exists(file_path):
        try:
            cmd = ["sdelete", "-p", str(passes), file_path]
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"Error during secure delete: {e}")
            
    else:
        print(f"File not found: {file_path}")


def _secure_delete_files_in_directory(directory):
    """Securely delete all files in the specified directory."""
    
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                secure_delete(file_path)
                # print(f"[info] securely deleted file")
            except Exception as e:
                print(f"[error] failed to securely delete file {file_path}: {e}")


def _remove_empty_directories(directory):
    """Remove empty directories in the specified directory."""
    
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.rmdir(dir_path)
                # print(f"[info] removed directory")
            except Exception as e:
                print(f"[error] failed to remove directory {dir_path}: {e}")
                
                
def secure_delete_dir(directory):
    """Secure delete directory."""
    
    print("\nCLEANING UP...\n(do not close program)")
    
    _secure_delete_files_in_directory(directory)
    _remove_empty_directories(directory)
    os.rmdir(directory)
    
    
if __name__ == "__main__":
    directory = input("Enter directory to remove: ")
    secure_delete_dir(directory)