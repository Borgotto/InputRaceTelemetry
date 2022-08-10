#!python3
import socket
import sys
import irsdk



if len(sys.argv) == 1:
    # Get "IP address of Server" and also the "port number" from argument 1 and argument 2
    #hostname = socket.gethostname()   
    #ip = socket.gethostbyname(hostname)
    #ip = sys.argv[1]
    ip = "127.0.0.1"
    port = int(20778)
else:
    print("Run like : python3 client.py <arg1 server ip 192.168.1.102> <arg2 server port 4444 >")
    exit(1)

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))
print("Do Ctrl+c to exit the program !!")



# Let's send data through UDP protocol
while True:
    data, address = s.recvfrom(1024)
    print("\n\n 2. Client received : ", data.decode('UTF-8'), "\n\n")
# close the socket
s.close()