import os
import getpass
import py7zr
import shutil
from util.delete import secure_delete, secure_delete_dir


BACKUP_DIRNAME = ".backup"


## note - 7z enc iv auto generated (nice)
# should work with files
def encrypt(path):
    password = getpass.getpass("Password: ")
    password_conf = getpass.getpass("Confirm Password: ")

    if password != password_conf:
        print("[error] passwords do not match")
        return

    if not os.path.exists(path):
        print(f"[error] {path} does not exist.")
        return
        
    if os.path.isfile(path):
        is_file = True
    elif os.path.isdir(path):
        is_file = False
    else:
        print("[error] unsupported path type.")
        return
        

    # Determine output .7z file path
    base_name = os.path.basename(path.rstrip(os.sep))
    output_filename = base_name + ".7z"
    output_file_path = os.path.join(os.path.dirname(path), output_filename)

    try:
        with py7zr.SevenZipFile(output_file_path, mode='w', password=password) as archive:
            archive.set_encrypted_header(True)
            
            if is_file:
                archive.write(path, arcname=base_name)
            else:
                archive.writeall(path, arcname=base_name)

        print(f"Successfully compressed {path} into {output_file_path}.")

    except Exception as e:
        print(f"[error] {e}")
        return

    # Securely delete the original file or directory
    if is_file:
        secure_delete(path)
    else:
        secure_delete_dir(path)
    
 

#### file (not dir) deleted
def decrypt(target):
    password = getpass.getpass("Password: ")
    # get the directory name and user password

    file_path = target + ".7z"
    backup_dir = os.path.join(os.path.dirname(file_path), BACKUP_DIRNAME)

    if not os.path.isfile(file_path):
        print(f"[error] {file_path} does not exist.")
        return

    try:
        with py7zr.SevenZipFile(file_path, mode="r", password=password) as archive:
            archive.extractall(path=os.path.dirname(file_path))
            # decrypt and extract the .7z file
              
        print(f"Successfully extracted {file_path}.")

        # Copy the decrypted 7z file to the backup folder, replacing the file if it exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)  # create the .backup folder if it does not exist

        backup_file_path = os.path.join(backup_dir, os.path.basename(file_path))
        shutil.copy(file_path, backup_file_path)
        print(f"Backup of {file_path} created in {backup_dir}.")

    except Exception as e:
        print(f"[error] {e}")
        return
 
    secure_delete(file_path)
    # securely delete the .7z file