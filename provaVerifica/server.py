import threading
import socket 
import time
import sqlite3

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#server_address=config1.server_address
s.bind(('0.0.0.0', 3450))       #bind del server tcp
s.listen()
c, a=s.accept()
print("connesso")


def eseguiComando(comando, nomeFile):
    lista_risultati = []
    con=sqlite3.connect("file.db")
    res0 = con.execute(f"SELECT files.nome from files")
    lista_film = res0.fetchall()
    for i, l in enumerate(lista_film):
        lista_film[i]=l[0]
    #print(lista_film)
    if comando not in [1, 2, 3, 4]:
        print("comando non in lista comandi")
    else:
        if comando == 1:
            if(nomeFile not in lista_film):
                print(f"film {nomeFile} non presente")
            else:
                res1 = con.execute(f"SELECT * from files where UPPER(files.nome) = UPPER('{nomeFile}')")
                lista_risultati=str(res1.fetchall())#ritorna lista con tutti i risultati
        elif comando == 2:
            if(nomeFile not in lista_film):
                print(f"film {nomeFile} non presente")
            else:
                res2 = con.execute(f"SELECT files.tot_frammenti from files where UPPER(files.nome) = UPPER('{nomeFile}')")
                lista_risultati=str(res2.fetchall()[0][0])#ritorna lista con tutti i risultati
        elif comando == 4:
            if(nomeFile not in lista_film):
                print(f"film {nomeFile} non presente")
            else:
                res4 = con.execute(f"SELECT frammenti.host from frammenti, files where UPPER(files.nome) = UPPER('{nomeFile}') and frammenti.id_file = files.id_file")
                lista_risultati=res4.fetchall()#ritorna lista con tutti i risultati
                for i, l in enumerate(lista_risultati):
                    lista_risultati[i]=l[0]
        elif comando == 3:
            nome_frammento = nomeFile.split(",")
            if(nome_frammento[0] not in lista_film):
                print(f"film {nome_frammento[0]} non presente")
            else:
                res3 = con.execute(f"SELECT frammenti.host from frammenti, files where UPPER(files.nome) = UPPER('{nome_frammento[0]}') and frammenti.id_file = files.id_file and frammenti.n_frammento = {int(nome_frammento[1])}")
                lista_risultati=str(res3.fetchall()[0][0])#ritorna lista con tutti i risultati
        #print(lista_risultati)
    con.close()
    return lista_risultati
        

class receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection=c
    
    def run(self):
        while True:
            text_received = self.connection.recv(4096)
            #print(text_received.decode())
            t=text_received.decode()
            lis = t.split(";")
            risultati = eseguiComando(int(lis[0]), lis[1])
            print(risultati)



def main():
    r = receiver()
    r.start()   
    s.close()


if __name__ == "__main__":
    main()