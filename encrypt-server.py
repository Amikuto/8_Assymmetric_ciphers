import socket
import json

from utils import check_certificate, crypt_func, bind_socket, encode_server_certificate_key, decode_key


sock = socket.socket()
bind_socket(sock)
sock.listen()

conn, addr = sock.accept()

json_text = conn.recv(1024).decode()
text = json.loads(json_text)
# print(text)

g_client = text['g']
A_client = text['A']
p_client = text['p']
text = {
    'B': encode_server_certificate_key(g=g_client, p=p_client)
}
# print(text)
conn.send(json.dumps(text).encode())

K = decode_key(key=A_client, p=p_client)
print("Ключ K: ", K)

if check_certificate(K):
    while True:
        text = conn.recv(1024).decode()
        print("Text from client encrypted:", text)
        text = crypt_func(K, text)
        print("Text from client deencrypted:", text)

        if text == "exit":
            conn.send(crypt_func(K, "exit").encode())
            break

        answer = "OK"
        print("Deencrypted answer:", answer)
        answer = crypt_func(K, answer)
        print("Encrypted answer:", answer, end="\n\n")
        conn.send(answer.encode())

sock.close()
