import socket
import ipaddress
import re


#UDPServer that serves as the echo server receives messages from the echo client

def valid_port(client_port):
    '''
    prompts user to enter a client port and validates using RegEx
    :param client_port: Server port to check as a string
    :return: server port as an integer
    '''

    regex_port = r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
    valid = False

    #Loop until a valid client port is provided
    while not valid:

        #check if client_port matches the pattern defined in regex_port
        if re.match(regex_port, client_port):
            #sets valid to "True" to exit loop
            valid = True

        else:
            #prompts re-entry for client port until a valid port is recieved
            print ("Invalid client port!")
            client_port = input ("Enter the port number for the server: ")

    #converts client_port to integer and returns
    return int(client_port)

def valid_ip(ip_str):
    '''
    Validates the IP addresses using ipaddress module
    :param ip_str: The IP address as a string
    :return: Validated IP address
    '''

    try:
        ip = ipaddress.ip_address(ip_str)
        # If the IP address is valid, print a message displaying the IP.
        print(f"Using IP address: {ip}")
        return str(ip)

    except ValueError:
        # If a ValueError is raised (invalid IP), print an error message.
        print("Invalid IP address format!")
        # Return None to indicate that the input was not a valid IP address.
        return None

def udp_server():
    '''
    Starts UDP server and binds it to the user-specified IP address and port
    Listens for messages from client, receives messages, processes by converting to uppercase
    then sends it back
    '''

    #prompts the user for the server IP and port

    server_ip = input ('Enter the IP address for the server: ')
    #validates the inputted server ip through valid_ip function
    server_ip = valid_ip(server_ip)

    if not server_ip:
        print("Exiting due to invalid IP address.")
        return


    client_port = input ('Enter the port number for the server: ')
    #validates the inputted port number through valid_port function
    client_port = valid_port(client_port)

    #create and bind a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, client_port))
    print(f"Server started on {server_ip}:{client_port}")

    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)  # buffer size (bytes)
            print(f"Received message: {data.decode().strip()}' from {client_address}")

            #Convert message to Uppercase
            response_message = data.decode().upper()

            #Relay the response back to client in uppercase
            server_socket.sendto(response_message.encode(), client_address)
            print(f"Sent reponse to {client_address}: '{response_message}'")

    #Execeptions for errors
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()
        print("Server socket closed.")

if __name__ == "__main__":
    udp_server()