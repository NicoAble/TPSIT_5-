import threading
import socket 
import time
import sqlite3

tris = '1,2,3,4,5,6,7,8,9'
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#server_address=config1.server_address
s.bind(('0.0.0.0', 3450))       #bind del server tcp
Fine = True # aspetto che finisca la partita


def ricomponiTris(t):
    r = t[0]+","+t[1]+","+t[2]+","+t[3]+","+t[4]+","+t[5]+","+t[6]+","+t[7]+","+t[8]
    return r

def controllaFine(t):
    global Fine
    print(t)
    if '1' not in t and '2' not in t and '3' not in t and '4' not in t and '5' not in t and '6' not in t and '7' not in t and '8' not in t and '9' not in t:
        Fine = False

class Server(threading.Thread):
    def __init__(self, conn, num):
        threading.Thread.__init__(self)
        self.conn = conn
        self.numClient = num
    def run(self):
        global tris
        if self.numClient == 1 or self.numClient == 2:
            if self.numClient == 1: carta = "O"
            elif self.numClient == 2: carta = "X"
            self.conn.sendall(str(tris).encode())# invio stringa
            '''while Fine:
                mess =  self.conn.recv(4096).decode()#leggo il messaggio in entrata e lo decodifico
                tris = tris.split(',')
                if tris[int(mess)-1] == 'X' or tris[int(mess)-1]=='O':
                    print("non possibile inserire")
                else: tris[int(mess)-1] = carta
                tris = ricomponiTris(tris)
                self.conn.sendall(str(tris).encode())# invio stringa
                controllaFine(tris)'''
                


def main():
    global Fine
    lista_thread = []
    i=1
    while Fine:#ciclo per accettare le connessioni
        s.listen()
        conn, address = s.accept()
        #print("connesso")
        server = Server(conn, i)#dichiaro il nuovo oggeto thread
        lista_thread.append(server)#aggiungo l'oggetto alla lista che utilizzerò per chiudere tutti i thread
        server.start()#faccio partire il thread
        print(f"start client {i}")
        i+=1
    
    print("fuori ciclo")

    if (Fine == False):
            conn.sendall(str("exit").encode())# invio stringa
    
    for i in lista_thread:#ciclo per chiudere tutti i thread
        i.join()
    s.close()#chiudo il socket

if __name__ == "__main__":
    main()