import socket

# Inisialisasi socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket ke alamat dan port tertentu
server_address = ('localhost', 5000)
sock.bind(server_address)

# Menunggu koneksi masuk
sock.listen(1)
print('Menunggu koneksi dari klien...')

while True:
    # Menerima koneksi dari klien
    client_socket, client_address = sock.accept()
    print('Terhubung dengan klien:', client_address)

    while True:
        # Menerima pesan dari klien
        data = client_socket.recv(1024).decode()
        if not data:
            break

        print('Pesan diterima dari klien:', data)
        
        # Memisahkan operator dan operand
        operand1, operator, operand2 = data.split()
        
        # Melakukan perhitungan matematika
        result = None
        if operator == '+':
            result = int(operand1) + int(operand2)
        elif operator == '-':
            result = int(operand1) - int(operand2)
        elif operator == '*':
            result = int(operand1) * int(operand2)
        elif operator == '/':
            if operand2 != 0:
                result = int(operand1) / int(operand2)
            else:
                result = "Error: Pembagian dengan nol"
        else:
            result = "Operator tidak dikenali. Gunakan salah satu dari: +, -, *, /"

        # Mengirim pesan balasan berisi hasil perhitungan ke klien
        response = str(result)
        client_socket.send(response.encode())

    # Menutup koneksi dengan klien
    client_socket.close()
