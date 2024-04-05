import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect('localhost', 12345)

pesan = input("Masukkan pesan: ")
client_socket.send(pesan.encode())

jumlah_karakter = client_socket.recv(1024).decode()
print("Jumlah karakter:", jumlah_karakter)

client_socket.close()

