import socket
import ssl

# Membuat dan mengonfigurasi socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
print("Server mendengarkan di localhost:12345")

# Mengamankan socket dengan SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
secure_server_socket = context.wrap_socket(server_socket, server_side=True)

def handle_client(secure_conn):
    try:
        while True:
            data = secure_conn.recv(1024)
            if not data:
                break
            print(f"Client: {data.decode()}")
            
            # Server siap untuk mengirim pesan balik
            reply = input("Server: ")
            secure_conn.send(reply.encode())
    finally:
        secure_conn.close()

# Menerima koneksi dari klien
while True:
    client_socket, addr = secure_server_socket.accept()
    print(f"Koneksi dari {addr}")
    handle_client(client_socket)
