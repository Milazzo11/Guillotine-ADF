## ADF setup file


from util import system
import service

import subprocess



def service_setup():
    """
    """

    print("Service Menu (ensure service is stopped, then select an option):")
    print("1 - clear saved devices")
    print("2 - save connected devices")
    print("x - quit")
    
    op = input("\n> ")
    
    match op:
        case "1":
            service.clear_devices()
        case "2":
            service.add_devices()
        case "x":
            pass
        case _:
            print("Error: incorrect command")
    


def requirements_check():
    """
    """
    
    print("CHECK RESULTS")
    print("-------------")
    
    try:
        subprocess.run(["exiftool", "-ver"], timeout=3)
        print(":) EXIFTOOLS -- INSTALLED")
        
    except:
        print(":( EXIFTOOLS -- NOT INSTALLED")
        
    input()
    
    
def fde_setup():
    """
    """
    
    subprocess.run(["control" ,"/name", "Microsoft.BitLockerDriveEncryption"])



def main():
    """
    """
    
    print("Maximum-Security Anti-Digital Forensics Windows Toolkit")
    print("-------------------------------------------------------")
    
    while True:
        
        print("Main Menu (select an option):")
        print("1 - device monitor service setup")
        print("2 - requirements check")
        print("3 - configure BitLocker FDE")
        print("x - quit")
        
        op = input("\n> ")
        system.cls()
        
        match op:
            case "1":
                service_setup()
            case "2":
                requirements_check()
            case "3":
                fde_setup()
            case "x":
                system.cls()
                return
            case _:
                print("Error: incorrect command")
                
        system.cls()


if __name__ == "__main__":
    main()