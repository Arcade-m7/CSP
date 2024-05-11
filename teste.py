'''
import sys

def init():
    global print    
    def print(*values,sep=' ',end='\n',file=sys.stdout.write):
        data = f'function called : {str(sep.join(list(map(lambda x:str(x),values))))}'+end
        file(data)

class x:

    def z(yy):
        pass

init()

print(list(range(100)),list(range(20)),x)

from NetStructer import Bridge , LocalIP
from socket import socket
from sys import stdout

server = socket()
server.bind((LocalIP(),2000))
server.listen()

bridge , addr = server.accept() ; bridge = Bridge(bridge)

print('client accepted !')

while True:
    print(bridge.RecvBuffer())'''

from __init__ import Console

console = Console()
console.init()
console.run()