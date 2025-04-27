import os
import subprocess



def exiftool(path):
    """
    """
    
    try:
        subprocess.run(["exiftool", "-all=", "-overwrite_original", path], check=True)
    except Exception as e:
       print(f"[error] ensure exiftool is installed: {e}")


def metawipe(path):
    """
    Removes all metadata from the given file or all files in a directory (recursively),
    using the exiftool command-line tool. This operation is destructive—metadata is permanently deleted.
    
    Requirements:
    - exiftool must be installed and available in the system's PATH.

    Parameters:
    - path (str): Path to a file or directory.
    """
    
    if not os.path.exists(path):
        print(f"Error: {path} does not exist.")
        return

    if os.path.isfile(path):
        # Remove metadata from a single file, overwrite original
        exiftool(path)
    elif os.path.isdir(path):
        # Recursively process all files in the directory
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                exiftool(full_path)
    else:
        print("[error] unsupported path type")
