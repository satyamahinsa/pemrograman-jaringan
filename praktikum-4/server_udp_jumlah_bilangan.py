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
    # Menerima bilangan-bilangan dari klien sebagai string dan memisahkannya menjadi list
    bilangan_list = data.decode().split(' ')
    total = sum(map(int, bilangan_list)) 
    
    # Mengirim balasan ke client
    message = 'Hasil penjumlahan bilangan bulat: ' + str(total)
    server_socket.sendto(message.encode(), address)


