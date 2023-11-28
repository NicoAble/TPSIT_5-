import threading
import socket 
import time
import sqlite3

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#server_address=config1.server_address
s.bind(('0.0.0.0', 3450))       #bind del server tcp


class Server(threading.Thread):
    def __init__(self, conn, num):
        threading.Thread.__init__(self)
        self.conn = conn
        self.numClient = num
        self.fiume = ""
        self.localita = ""
        self.livello = 0
    def run(self):
        
        mess =  self.conn.recv(4096).decode()#leggo il messaggio in entrata e lo decodifico
        m = mess.split(",")
        self.fiume = m[0]
        self.localita = m[1]
        print(self.fiume, self.localita)

        while True:
            con=sqlite3.connect("fiumi.db")
            res2 = con.execute(f"Select livello FROM livelli WHERE UPPER(fiume)=UPPER('{self.fiume}') and UPPER(localita)=UPPER('{self.localita}')")
            livello = res2.fetchall()[0][0]
            con.close()
            mess2 =  self.conn.recv(4096).decode()#leggo il messaggio in entrata e lo decodifico
            mess2 = mess2.split(",")
            self.livello = mess2[0]
            data = mess2[1]
            print(self.livello, data)
            percentuale = (self.livello / livello) *100
            if percentuale < 30:
                mex3 = "avvenuta ricezione"
                self.conn.sendall(str(mex3).encode())# invio stringa
            elif percentuale >= 30 and percentuale <=70:
                mex3 = "avvenuta ricezione"
                self.conn.sendall(str(mex3).encode())# invio stringa
                print("pericolo imminente")
            elif percentuale >= 70:
                mex3 = "sirena"
                self.conn.sendall(str(mex3).encode())# invio stringa
                print("pericolo in corso")
            

                
def main():
    lista_thread = []
    i=1
    while True:#ciclo per accettare le connessioni
        s.listen()
        conn, address = s.accept()
        #print("connesso")
        server = Server(conn, i)#dichiaro il nuovo oggeto thread
        lista_thread.append(server)#aggiungo l'oggetto alla lista che utilizzerò per chiudere tutti i thread
        server.start()#faccio partire il thread
        print(f"start client {i}")
        i+=1
    
    print("fuori ciclo")
    for i in lista_thread:#ciclo per chiudere tutti i thread
        i.join()
    s.close()#chiudo il socket

if __name__ == "__main__":
    main()