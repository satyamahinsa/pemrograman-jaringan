import socket

# Inisialisasi socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket ke alamat dan port tertentu
server_address = ('localhost', 12345)
server_socket.bind(server_address)

while True:
    print('Menunggu pesan dari client...')
    data, address = server_socket.recvfrom(4096)

    print('Menerima pesan dari client:', data.decode())
    
    # Mengirim balasan ke client
    message = 'Pesan diterima oleh server!'
    server_socket.sendto(message.encode(), address)