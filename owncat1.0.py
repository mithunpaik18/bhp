#shell proxy
import socket
import threading
import subprocess
import sys
import os

mode = sys.argv[1] #server for acting as server and client for acting as a client
ip = sys.argv[2]
port = sys.argv[3]

print(mode, ip, port)


bind_ip = ip
bind_port = int(port)


def handle_client(client_socket):
    #print out what the client sends
    request = client_socket.recv(1024)
    
    print("[*] recieved: {}".format(request))
    
    result = run_command(request)
    
    # formatted_output = ''
    # for line in result:
        # formatted_output = formatted_output + line + '\n'
    
    #send back a packet
    client_socket.sendall(bytes(result, 'ascii'))
    
    client_socket.close()
    
def run_command(command):
    os.system(command.decode('ascii') + ' > tmp')
    with open('tmp', 'r') as f:
        out = f.read()
        print(out)
    return out


if mode == 'server':
    print('server loop')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    print("[*] listening on {}:{}".format(bind_ip, bind_port))
    
    while True:
        client, addr = server.accept()
        print("[*] Accepted connection from {}:{}".format(addr[0], addr[1]))
        
        #spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
        
elif mode == 'client':
    target_host = ip
    target_port = int(port)
    while True:
        command = input('$$$:')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host, target_port))
        client.sendall(bytes(command.strip(), 'ascii'))
        response = client.recv(4096)
        print(response.decode('ascii'))

#client handling thread starts here

