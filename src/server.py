import socket
import time

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ip = '127.0.0.1'
    port = 8080

    # Bind the socket to the port
    server_address = (ip, port)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)
    i = 0
    while True:
        print('waiting to receive message')
        data, address = sock.recvfrom(64)
        print('received %s bytes from %s' % (len(data), address))

        if data:
            data = data.decode("utf-8")
            print('received stage', data.split(' ')[0])
            print('received time', data.split(' ')[1])
            data += " " + str(time.time())
            data += " " + str(time.time())  # time sent

            sent = sock.sendto(str.encode(data), address)
            print('sent %s bytes back to %s' % (sent, address) + '\n')
