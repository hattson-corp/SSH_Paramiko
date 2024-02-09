import paramiko
import subprocess
import threading
import argparse
import pwinput
import sys


class sshcmd:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--ip", help="ip of the host to connect ot like 1.1.1.1 .", type=str, required=True)
        parser.add_argument("-u", "--username", help="the username of the ssh  .", type=str, required=True)
        parser.add_argument("-p", "--password", help="the password of the ssh  .", type=str, required=True)
        parser.add_argument("-c", "--command", help="the command to run in the ssh server .", type=str, required=True)
        args = parser.parse_args()
        self.user = args.username
        self.passwd = args.password
        self.ip = args.ip
        self.command = args.command
        self.ssh_command()

    def ssh_command(self):
        client = paramiko.SSHClient()
        # client.load_host_keys("~/.ssh/known_hosts")
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ip, username=self.user, password=self.passwd)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.exec_command(self.command)
            print(ssh_session.recv(4096).decode())
        return

# demo =sshcmd()

class SSH_Manager:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--ip", help="ip of the host to connect ot like 1.1.1.1 .", type=str)
        parser.add_argument("-u", "--username", help="the username of the ssh  .", type=str)
        parser.add_argument("-p", "--password", help="the password of the ssh  .", type=str)
        parser.add_argument("-c", "--command", help="the command to run in the ssh server .", type=str)
        parser.add_argument("-s", "--shell", help="opening active shell session .", action="store_true")
        parser.add_argument("-w", "--wizard", help="start the wizard  .", action="store_true")

        args = parser.parse_args()
        self.user = args.username
        self.passwd = args.password
        self.ip = args.ip
        self.command = args.command
        self.shel = args.shell
        self.name = ""
        if not self.ip or args.wizard:
            self.menu()
        # if args.wizard:
        #     self.menu()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.ip, username=self.user, password=self.passwd)
            print("💀 connected successfully to the ssh server !")
        except:
            print("💀 something has gone wrong , try again \ncauses :\n1. network connection\n2. wrong password")
            sys.exit(0)
        self.ssh_sess = client.get_transport().open_session()
        if self.user == "root":
            self.name = f"root💀{self.ip} ~# "
        else:
            self.name = f"{self.user}💀{self.ip} ~$ "
        if self.shel:
            self.shell()
        else:
            self.ssh_session(self.command)

    def menu(self):
        print('''
                  .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'   SSH    `98v8P'  MANAGER  `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
                               `             '
        ''')
        print("💀 [ starting the ssh session ] ")
        self.ip = input("💀 [ enter ip ] ► ")
        self.user = input("💀 [ enter username ] ► ")
        self.passwd = pwinput.pwinput(prompt="💀 [ enter password ] ► ", mask="💀")
    def ssh_session(self, command):
        if self.ssh_sess.active:
            self.ssh_sess.exec_command(command)
            print(f"[Server] {self.ssh_sess.recv(4096).decode()}")
            return True
        if not ssh_sess.active:
            print("[X] Failed to activate the ssh connection ")
            return False

    def shell(self):
        while True:
            ask = input(f"{self.name}")
            if self.ssh_session(ask):
                continue
            if not self.ssh_session(ask):
                break
        print("[X] Session has been ended .")

demo = SSH_Manager()