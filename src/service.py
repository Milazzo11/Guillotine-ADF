import os
import time
import ctypes
import atexit
from pywinusb import hid
import tkinter as tk
import time
import wmi

import pickle
import subprocess

from util import system




### note, for non-demo, this would be pyw

DEVICE_DATA_PATH = os.path.join("data", "devices.pkl")

NUM_WATCHDOGS = 64



def clear_devies():
    """
    """
    
    open(DEVICE_DATA_PATH, "wb").close()
    
   
def read_devices():
    """
    """
    
    try:
        with open(DEVICE_DATA_PATH, "rb") as f:
            devices = pickle.load(f)
    except:
        devices = []
        
    return devices
    
    
def add_devices():
    """
    """
    
    devices = read_devices()  # Should return a tuple: (disk_serials, hid_serials)

    # Extend storage device serials
    c = wmi.WMI()
    disk_serials = {
        (disk.SerialNumber or "").strip()
        for disk in c.Win32_DiskDrive()
    }
    devices.extend(disk_serials)
    

    # Remove duplicates by converting to list(set(...))
    devices = list(set(devices))
    
    print(devices)

    with open(DEVICE_DATA_PATH, "wb") as f:
        pickle.dump(devices, f)
        
    return devices
    

## TODO - FETCH AND PICKLE ONLY THE SERIALS -- FOR INPUT DEVICES, IGNORE "" SERIAL, AND DISK DEVICES, "" SERIAL = SHUTDOWN
    

#BASELINE_DEVICES, BASELINE_DISKS = read_devices()

#with open(os.path.join("data", "devices.pkl"), "rb") as f:
#    BASELINE_DEVICES = read_devices()





def shutdown_computer():###unused
    """
    Shut down the computer.
    """

    # os.system("shutdown /s /f /t 0")
    print("SHUTDOWN TRIGGERED")
 
 

def check_bad_device():
    """
    Check for storage device changes.
    Baseline is a list of serial numbers (strings).
    """
    c = wmi.WMI()
    current_serials = {
        (disk.SerialNumber or "").strip()
        for disk in c.Win32_DiskDrive()
    }

    # BASELINE_DISKS is a list of serial strings
    baseline_serials = set(baseline_devices)

    # Immediately return True if any current STORAGE DEVICE has no serial
    if "" in current_serials:
        return True

    return not current_serials.issubset(baseline_serials)



def main():
    """
    Program entry point.
    """
    
    global baseline_devices
    
    ##shield.secure()
    
    service_pid = str(os.getpid())
    num_watchdogs = str(NUM_WATCHDOGS)
    exe_path = os.path.join("shield", "watchdog.exe")
    subprocess.call([exe_path, service_pid, num_watchdogs])
    
    baseline_devices = add_devices()
    
    try:
        while True:
            if check_bad_device():
                system.shutdown()
                # shutdown on change
                
            time.sleep(0.001)
            
    except:
        system.shutdown()
        # shutdown if error occurs


if __name__ == "__main__":
    main()