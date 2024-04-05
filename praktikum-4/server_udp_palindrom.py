import socket

# Inisialisasi socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket ke alamat dan port tertentu
server_address = ('localhost', 12345)
server_socket.bind(server_address)

def isPalindrome(s):
    s = s.lower()
    return s == s[::-1]

while True:
    print('Menunggu pesan dari client...')
    data, address = server_socket.recvfrom(4096)

    print('Menerima pesan dari client:', data.decode())
    pesan = data.decode()
    
    if isPalindrome(pesan):
        message = 'Pesan: ' + pesan + ' merupakan Palindrom'
    else:
        message = 'Pesan: ' + pesan + ' bukan merupakan Palindrom'

    # Mengirim balasan ke client
    server_socket.sendto(message.encode(), address)


