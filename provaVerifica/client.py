#192.168.1.130
import time
import socket #nativa
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #costruttore --> con questa riga ho istanziato il socket (creazione del socket)
server_address = ('127.0.0.1', 3450) #192.168.0.123 indirizzo IP alphabot
s.connect(server_address)
print("connesso")


def main():
    while True:
        azione = int(input(print("scrivere quale azione si vuole eseguire \n(1 = chiedere al server se un certo nome file è presente; \n 2 = chiedere al server il numero di frammenti di un file a partire dal suo nome file; \n 3 = chiedere al server l’IP dell’host che ospita un frammento a partire nome file e dal numero del frammento; \n 4 = chiedere al server tutti gli IP degli host sui quali sono salvati i frammenti di un file a partire dal nome file.) :")))
        if azione not in [1, 2, 3, 4]:
            print("comando errato")
        else: 
            nomeFile = str(input("inserisci il nome del file: "))
            text = str(azione) + ";" + str(nomeFile) 
            if azione == 3:
                numeroFrammento = int(input("inserisci il numero del frammento: "))
                text += "," + str(numeroFrammento)
            s.sendto(text.encode(), server_address) #mando il messaggio al server
    s.close()


if __name__ == "__main__":
    main()