import socket

# Inisialisasi socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)

while True:
    message = input('Masukkan bilangan: ')

    # Mengirim pesan ke server
    client_socket.sendto(message.encode(), server_address)

    # Menerima balasan dari server
    data, _ = client_socket.recvfrom(4096)
    print('Menerima balasan dari server:', data.decode())


