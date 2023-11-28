import datetime
import time
import sqlite3

'''time.sleep(15)
print(datetime.datetime.now())
'''
import socket #nativa
import threading
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #costruttore --> con questa riga ho istanziato il socket (creazione del socket)
server_address = ('127.0.0.1', 3450) #192.168.0.123 indirizzo IP alphabot
fiume = ""
localita = ""
livello = 0

sirena = False

def controllaSePresente(id):
    global fiume
    global localita
    global livello
    continua = True
    con=sqlite3.connect("fiumi.db")
    res0 = con.execute(f"Select id_stazione FROM livelli")
    lista_id = res0.fetchall()
    for i, l in enumerate(lista_id):
        lista_id[i]=l[0]
    print(lista_id)
    if id in lista_id:
        res1 = con.execute(f"Select fiume, localita FROM livelli WHERE id_stazione = {id}")
        tuplaFiumeLocalita = res1.fetchall()[0]
        fiume = tuplaFiumeLocalita[0]
        localita = tuplaFiumeLocalita[1]
        res2 = con.execute(f"Select livello FROM livelli WHERE id_stazione = {id}")
        livello = res2.fetchall()[0][0]
        continua = False
    con.close()
    return continua


def main():
    global livello
    global sirena
    id = int(input(print("inserire l'id corrispondente al fiume e località in cui ti trovi:")))
    while(controllaSePresente(id)):
       id = int(input(print("inserire l'id corrispondente al fiume e località in cui ti trovi:"))) 
    s.connect(server_address)
    print("connesso")
    mex = fiume + "," + localita
    print(mex)
    s.sendto(mex.encode(), server_address) #mando il messaggio al server
    while True:
        c = livello
        time.sleep(2)
        data_ora = datetime.datetime.now()
        livello += float(random.randint(-livello, +livello))
        mex2 = f"{livello}" + "," + str(data_ora)
        s.sendto(mex2.encode(), server_address) #mando il messaggio al server
        livello = c
        text_received, address = s.recvfrom(4096)
        if text_received.decode() == "sirena": 
            sirena = True
        if sirena:
            print("sirena ALLARME")
            sirena = False
    s.close()


if __name__ == "__main__":
    main()

