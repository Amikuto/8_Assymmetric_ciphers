import socket
import json
import utils


ADDRESS = 'localhost'
PORT = 9090
sock = socket.socket()
sock.connect((ADDRESS, PORT))

json_text = {
    "g": utils.encode_client_certificate_key()[0],
    "p": utils.encode_client_certificate_key()[1],
    "A": utils.encode_client_certificate_key()[2]
}
sock.send(json.dumps(json_text).encode())

data = sock.recv(1024).decode()
server_B = json.loads(data)['B']

K = utils.decode_key_from_server(server_B)
print("Ключ K: ", K)


while True:
    question = input("Введите запрос: ")
    print("Deencrypted question to server:", question)
    question = utils.crypt_func(K, question)
    print("Encrypted question to server:", question)
    sock.send(question.encode())

    answer = sock.recv(1024).decode()
    print("Deencrypted answer from server:", answer)
    answer = utils.crypt_func(K, answer)
    print("Encrypted answer from server:", answer, end="\n\n")

    if answer == "exit":
        break

sock.close()
