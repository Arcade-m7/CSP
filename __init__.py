requirments = [
    'NetStructer',
    'colored',
]

from socket import socket , gaierror
from sys import stdout , argv
from exceptions import *
from signal import signal ,  SIGINT
from os import kill , getpid , system
from platform import system as syst



try:
    import NetStructer
except ImportError :
    raise ImportError('NetStructer must be installed use pip install NetStructer or install it from github Arcade.m7')

try:
    import colored
except ImportError:
    raise ImportError('colored must be installed use pip install colored')

def stop():
        print('i called stop function')
        kill(getpid())

class Console:

    def __init__(self,ip,port=2000) -> None:
        cmd = 'cls' if syst() == 'Windows' else 'clear'
        addr = (ip,port) ; self.run_ = True
        self.soc = socket() ; ip,port = Console.__gather__()
        if ip :
            self.ip,self.port = ip,port
        else:
            self.ip , self.port = addr
        self.addr = (self.ip,self.port)
        system(cmd) ; self.init() ; self.run()
    
    def __gather__():
        pyload = argv
        if len(pyload) == 2:
            return pyload[1:]
        return '',2000

    def __login__(self,soc):
        login_req = {'PassCode':'Arcade.m7.19682007'} ; soc.SendBuffer(login_req)
        return soc.RecvBuffer()
        
    def init(self):
        try:
            self.soc.connect(self.addr)
            self.soc = NetStructer.Bridge(self.soc) ; answer = self.__login__(self.soc)
            if not answer:
                raise PasswordError
        except ConnectionRefusedError:
            raise ConnectionRefusedError(f"connection refused")
        except gaierror:
            raise CantGetAddressInfo(f"can't find and device with ip {self.ip}")
        except Exception as exc:
            raise exc
        
    def run(self):
        while self.run_:
            try:
                stdout_ = self.soc.RecvBuffer()
                stdout.write(stdout_)
            except (ConnectionAbortedError,ConnectionResetError):
                raise ConnectionError('session ends')
            except KeyboardInterrupt:
                break

class Share:

    def __init__(self,addr=(NetStructer.LocalIP(),2000)):
        self.addr = addr ; self.ip , self.port = addr
        self.soc = NetStructer.Server(addr) ; self.user = None
    
    def __func__(self,soc:socket,_:dict,share):
        while True:
            try:
                user , _ = soc.accept() ; user = NetStructer.Bridge(user) ; user.TimeOut(30) ; resp = user.RecvBuffer(buffer=1024*100,buffer_size=1024*10)
                if resp == {'PassCode':'Arcade.m7.19682007'} :
                    user.SendBuffer(True)
                    user.TimeOut(None) ; share.user = user
                    stdout.write('Console has Connected\n')
                else:
                    user.Close()
            except OSError:
                break
            except Exception as exc:
                raise exc
            
    def stdout_(soc,out):
        try:
            soc.user.SendBuffer(out)
            stdout.write('sending buffer\n')
        except (ConnectionResetError,ConnectionAbortedError,AttributeError):
            stdout.write('writing buffer\n')
            stdout.write(out)

    def print_(*values,sep=' ',end='\n',file=stdout_,soc=None):
        try:
            buffer = f'print function := {sep.join(list(map(lambda x:str(x),values)))}{end}'
            file(soc,buffer)
        except Exception as exc:
            raise exc

    def init(self):
        global print
        print = lambda *values,sep=' ',end='\n',file=Share.stdout_,soc=self:Share.print_(*values,sep=sep,end=end,file=file,soc=soc)
        self.soc.init() ; func = lambda x,y,z=self : self.__func__(soc=x,_=y,share=z)
        self.soc.listen_on(func)

    def release(self):
        self.soc.stop()


        

