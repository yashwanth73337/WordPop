import socket
import sys

SOCKET_PATH = "/tmp/wordpop.sock"


def main():
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)
        client.close()
    except (ConnectionRefusedError, FileNotFoundError):
        print("WordPop isn't running. Start it first with: python3 dictionary_popup_linux.py")
        sys.exit(1)


if __name__ == "__main__":
    main()