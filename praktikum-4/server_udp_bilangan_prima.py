import socket

# Inisialisasi socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket ke alamat dan port tertentu
server_address = ('localhost', 12345)
server_socket.bind(server_address)

def isPrima(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

while True:
    print('Menunggu pesan dari client...')
    data, address = server_socket.recvfrom(4096)

    print('Menerima pesan dari client:', data.decode())
    bilangan = int(data.decode())
    
    if isPrima(bilangan):
        message = 'Bilangan: ' + str(bilangan) + ' adalah bilangan prima'
    else:
        message = 'Bilangan: ' + str(bilangan) + ' bukan bilangan prima'

    # Mengirim balasan ke client
    server_socket.sendto(message.encode(), address)


