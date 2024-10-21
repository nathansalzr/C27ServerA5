import re
import ipaddress
import socket

def valid_port(client_port):
    '''
    Prompts user to enter a client port and validates using RegEx.
    :param client_port: Server port to check as a string.
    :return: server port as an integer.
    '''
    regex_port = r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
    valid = False

    # Loop until a valid client port is provided.
    while not valid:
        # Check if client_port matches the pattern defined in regex_port.
        if re.match(regex_port, client_port):
            # Sets valid to True to exit the loop.
            valid = True
        else:
            # Prompts re-entry for client port until a valid port is received.
            print("Invalid client port!")
            client_port = input("Enter the port number for the server: ")

    # Converts client_port to integer and returns.
    return int(client_port)

def valid_ip(ip_str):
    '''
    Validates the IP addresses using ipaddress module.
    :param ip_str: The IP address as a string.
    :return: Validated IP address.
    '''
    try:
        # This will automatically validate IPv4 and IPv6 addresses.
        ip = ipaddress.ip_address(ip_str)
        # If the IP address is valid, print a message displaying the IP.
        print(f"Using IP address: {ip}")
        return str(ip)
    except ValueError:
        # If a ValueError is raised (invalid IP), print an error message.
        print("Invalid IP address format!")
        # Return None to indicate that the input was not a valid IP address.
        return None

def tcp_client():
    '''
    Runs the TCP client that sends the message to the server.
    '''
    # Prompt the user for the server IP and port.
    server_ip = input('Enter the IP address for the server: ')
    # Validates the inputted server IP through valid_ip function.
    server_ip = valid_ip(server_ip)

    if not server_ip:
        print("Exiting due to invalid IP address.")
        return

    client_port = input('Enter the port number for the server: ')
    # Validates the inputted port number through valid_port function.
    client_port = valid_port(client_port)

    # Create the server address tuple.
    server_address = (server_ip, client_port)

    # Creates a TCP Socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # Connect to the server.
            print(f"Connecting to {server_ip}:{client_port}...")
            sock.connect(server_address)
            print("Connected to server.")

            while True:
                # User input.
                message = input("Enter message to send to server (or 'exit' to quit): ")

                # If user inputs exit -> client will end.
                if message.lower() == 'exit':
                    print("Exiting client...")
                    break

                # Sends data to the server.
                print(f"Sending message: {message}")
                sock.sendall(message.encode())

                # Server response.
                data = sock.recv(1024)  # Buffer size (bytes).
                print(f"Received reply from server: {data.decode()}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    tcp_client()
