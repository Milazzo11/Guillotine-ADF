"""
"""


import argparse
from tools.delete import delete
from tools.encrypt import encrypt, decrypt
from tools.metawipe import metawipe


def main():
    """
    """

    parser = argparse.ArgumentParser(description="ADF arguments.")
    parser.add_argument("tool", choices=["delete", "encrypt", "decrypt", "metawipe"], help="Selected tool")
    parser.add_argument("target", help="Target file/directory")
    args = parser.parse_args()

    match args.tool:
        case "delete":
            delete(args.target)
        case "encrypt":
            encrypt(args.target)
        case "decrypt":
            decrypt(args.target)
        case "metawipe":
            metawipe(args.target)
        case _:
            print("Error: incorrect command")


if __name__ == "__main__":
    main()