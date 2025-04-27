"""
this will basically just call the util -- but having it in tools too for structure
"""


import os
from util.delete import secure_delete, secure_delete_dir


def delete(path):
    """
    """
    
    if os.path.isfile(path):
        secure_delete(path)
    elif os.path.isdir(path):
        secure_delete_dir(path)
    else:
        print("[error] unsupported path type")