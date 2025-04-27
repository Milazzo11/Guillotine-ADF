import subprocess
import sys


def cls():
    """
    """
    
    subprocess.run("cls", shell=True)


def shutdown():
    #subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=False)
    print("[SHUTDOWN] (test placeholder) -- Python\n")
    sys.exit()