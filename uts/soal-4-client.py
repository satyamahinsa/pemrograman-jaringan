import socket

# Mendefinisikan alamat server dan port
server_address = "::1"
server_port = 12345

# Membuat socket IPv6 TCP
client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# Menghubungkan socket ke server
client_socket.connect((server_address, server_port))
print(f"Terkoneksi ke server {server_address} pada port {server_port}")

try:
    # Mengirimkan pesan ke server
    message = "Halo, ini klien!"
    client_socket.sendall(message.encode())
    print("Pesan terkirim:", message)

    # Menerima balasan dari server
    data = client_socket.recv(1024)
    print("Balasan diterima:", data.decode())

finally:
    # Menutup koneksi
    client_socket.close()
    print("Koneksi dengan server ditutup")
