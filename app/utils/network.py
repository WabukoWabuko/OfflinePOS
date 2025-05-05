import socket
import time

def is_online(host="8.8.8.8", port=53, timeout=3):
    """
    Check if the internet is available by pinging Google's DNS.
    Returns True if online, False if offline.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def get_status():
    """Return the current online/offline status as a string."""
    return "Online" if is_online() else "Offline"

if __name__ == "__main__":
    # Test the connectivity checker
    while True:
        print(f"Status: {get_status()}")
        time.sleep(5)  # Check every 5 seconds
