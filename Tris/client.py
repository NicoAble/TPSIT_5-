import time
import socket #nativa
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #costruttore --> con questa riga ho istanziato il socket (creazione del socket)
server_address = ('127.0.0.1', 3450) #192.168.0.123 indirizzo IP alphabot
s.connect(server_address)
print("connesso")

def stampaGriglia(t):
    t = t.split(',')
    print(f"\n{t[0]}\t{t[1]}\t{t[2]}\n{t[3]}\t{t[4]}\t{t[5]}\n{t[6]}\t{t[7]}\t{t[8]}")

def main():
    while True:
        text_received, address = s.recvfrom(4096)
        if text_received == "exit": 
            print("partita conclusa")
            break
        else: stampaGriglia(text_received.decode())
        mossa = input("inserire la cella: ")
        if(int(mossa)>=1 and int(mossa)<=9):
            s.sendto(mossa.encode(), server_address) #mando il messaggio al server
    s.close()


if __name__ == "__main__":
    main()