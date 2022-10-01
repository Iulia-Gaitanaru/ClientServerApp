import socket
import threading
import time

nickname = input("Chose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the client to the server
client.connect(("127.0.0.1", 7000))


# Method for receiving messages from the client through the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


# Method for writing messages
def write():
    while True:
        message = input()
        if message != "":
            try:
                message = '{}: {}'.format(nickname, message)
                client.sendall(message.encode('ascii'))
            except:
                print("Error sending...")
        time.sleep(1)

# Running two threads for receiving and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
