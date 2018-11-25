import socket
import time


if __name__ == '__main__':

    ip = '127.0.0.1'
    server_port = 8080

    file = open("log" + str(time.time()) + ".txt", "a")
    server_address = (ip, server_port)
    stage = 1
    oldOffset = 0
    data = ""
    offset = 0
    while True:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) \
            # If the response from a partner is
        # not received within an expected time frame (i.e. if t4 − t1 > 1000ms) the sample is discarded.
        sock.settimeout(1)

        print("\n" + 'oldOffset ', oldOffset)
        new_time = str(time.time() - oldOffset)
        message = str(stage) + " " + new_time

        try:
            # Send data
            print('send stage ', stage)
            print('send time ', new_time)
            sent = sock.sendto(str.encode(message), server_address)

            # Receive response
            print('response')
            data, server = sock.recvfrom(64)
            data = data.decode("utf-8")
            print('received ', data)
            data += " " + str(time.time())

            # Calculate RTT and Offset
            seq_s, t1, t2, t3, t4 = data.split(" ")
            t1 = float(t1)
            t2 = float(t2)
            t3 = float(t3)
            t4 = float(t4)

            print("t1: %f " % t1)
            print("t2: %f " % t2)
            print("t3: %f " % t3)
            print("t4: %f " % t4)

            rtt = ((t4 - t1) - (t3 - t2))
            offset = (t4 - t3 + t2 - t1) / 2
            oldOffset = offset

            # LOG the information.
            file.write(" SUCCESS: " + ' oldOffset: ' + str(oldOffset) + ' send stage: ' + str(stage) + ' send time: ' +
                       str(new_time) + ' t1: ' + str(t1) + ' t2: ' + str(t2) + ' t3: ' + str(t3) + ' t4: ' + str(t4) +
                       ' rtt: ' + str(rtt) +
                       "\n")

        except socket.timeout:
            print('Timeout')
            file.write("FAILURE;" + message + "\n")

        stage += 1
        time.sleep(1)
