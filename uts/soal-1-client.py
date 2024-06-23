import socket
import ssl

# Membuat dan mengonfigurasi socket klien
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Mengamankan socket dengan SSL
context = ssl.create_default_context()
context.load_verify_locations('cert.pem')
secure_client_socket = context.wrap_socket(client_socket, server_hostname='satya')
secure_client_socket.connect(('localhost', 12345))

# Mengirim dan menerima pesan
try:
    while True:
        # Mengirim pesan ke server
        message = input("Client: ")
        secure_client_socket.send(message.encode())

        # Menerima respon dari server
        response = secure_client_socket.recv(1024)
        print(f"Server: {response.decode()}")
except KeyboardInterrupt:
    print("\nChat client ditutup.")
finally:
    secure_client_socket.close()
