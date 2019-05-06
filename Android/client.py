import paramiko

def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('localhost',usurname='root',password='toor')
    chan = client.get_transport().open_session()
    chan.send("Connected Successfully :)) ")
    print chan.recv(1024)

connect()
