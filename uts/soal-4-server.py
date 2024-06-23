import socket

# Membuat socket IPv6 TCP
server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# Mengikat socket ke alamat lokal dan port
server_socket.bind(("::1", 12345)) # "::1" adalah alamat loopback IPv6
server_socket.listen(1)
print("Server mendengarkan di port 12345")

# Menerima koneksi dari client
connection, addr = server_socket.accept()
print(f"Terhubung dengan {addr}")

try:
    # Menerima data dari client
    data = connection.recv(1024)
    print("Data diterima:", data.decode())

    # Mengirim balasan ke client
    message = "Pesan ini adalah balasan dari server!"
    connection.sendall(message.encode())

finally:
    # Menutup koneksi
    connection.close()
    server_socket.close()
    print("Server menutup koneksi")
