import threading
import socket

host = '127.0.0.1'  # localhost
port = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


# Method for server to send a broadcast message to all the clients
def broadcast(message):
    for client in clients:
        client.sendall(message)


# Method for receiving a message from a client and broadcast that message
def handle(client):
    client.settimeout(0.00001)
    while True:
        try:
            message = client.recv(1024)
        except socket.timeout as e:
            # index = clients.index(client)
            # clients.remove(client)
            # client.close()
            # nickname = nicknames[index]
            # broadcast('{} left!'.format(nickname).encode('ascii'))
            # nicknames.remove(nickname)
            # break
            pass
        else:
            print(message.decode("ascii"))
            broadcast(message)

# Method for connection and start the communication
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# Main method
print("Server is listening...")
receive()
