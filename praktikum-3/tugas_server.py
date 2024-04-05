import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Waiting...")
client_socket, client_address = server_socket.accept()
print(f"Terhubung dengan {client_address}")

while True:
    pesan = client_socket.recv(1024).decode()
    if not pesan:
        break
    
    jumlah_karakter = str(len(pesan))
    client_socket.send(jumlah_karakter.encode())

client_socket.close()
server_socket.close()

