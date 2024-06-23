import socket
import threading
import os

# List untuk menyimpan pesan yang diterima dan dikirim
store_message = []
# Daftar IP tujuan untuk mengirim pesan
list_IP = [
    ("192.168.0.173", 9002),
]


# Class untuk konfigurasi socket, termasuk membuat socket UDP dan mengikatnya ke alamat lokal
class sockConfig:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_address = ("192.168.0.122", 9001)
    socket.bind(local_address)


# Fungsi untuk menampilkan semua pesan yang disimpan di store_message
def showMessage():
    print("Pesan baru:")
    for message in store_message:
        print(message)


# Fungsi untuk mengirim pesan atau file ke beberapa IP tujuan terpilih
def multicast(socket):
    pilihan_ip = []
    for ip in range(len(list_IP)):
        print("Pilih IP:")
        for idx, address in enumerate(list_IP):
            print(f"{idx}. {address}")
        print("4. Exit")

        list_index = int(input("Masukkan IP tujuan: "))
        if list_index == 4:
            break
        pilihan_ip.append(list_index)
        os.system("cls")
    
    mode = mode_pesan()
    if mode == 1:
        message = input("Masukkan pesan: ")
        for ip in pilihan_ip:
            send_message(socket, list_IP[ip], message)
    elif mode == 2:
        message = []
        print("Input paragraf:")
        while True:
            message.append(input("Ketik (.) untuk berhenti: "))
            if message[-1] == ".":
                message = ". ".join(message)
                break
        for ip in pilihan_ip:
            send_message(socket, list_IP[ip], message)
    elif mode == 3:
        for ip in pilihan_ip:
            send_file(socket, list_IP[ip], 3)
    elif mode == 4:
        for ip in pilihan_ip:
            send_file(socket, list_IP[ip], 4)
    elif mode == 5:
        for ip in pilihan_ip:
            send_file(socket, list_IP[ip], 5)
    elif mode == 6:
        for ip in pilihan_ip:
            send_file(socket, list_IP[ip], 6)


# Fungsi untuk mengirim pesan atau file ke semua IP tujuan yang ada di dalam list_IP
def broadcast(socket):
    mode = mode_pesan()
    if mode == 1:
        message = input("Masukkan pesan: ")
        for ip in list_IP:
            send_message(socket, ip, message)
    elif mode == 2:
        message = []
        print("Input paragraf:")
        while True:
            message.append(input("Ketik (.) untuk berhenti: "))
            if message[-1] == ".":
                message = ". ".join(message)
                break
        for ip in list_IP:
            send_message(socket, ip, message)
    elif mode == 3:
        for ip in list_IP:
            send_file(socket, ip, 3)
    elif mode == 4:
        for ip in list_IP:
            send_file(socket, ip, 4)
    elif mode == 5:
        for ip in list_IP:
            send_file(socket, ip, 5)
    elif mode == 6:
        for ip in list_IP:
            send_file(socket, ip, 6)


# Fungsi untuk menerima pesan dari socket, baik itu pesan teks atau file
def recieve_message(socket):
    while True:
        data, address = socket.recvfrom(4096)
        message = f"From: {address} : {data.decode('utf-8')}"

        formats = ["docx", "pdf", "jpg", "png", "mp3", "mp4"]
        if any(format in message for format in formats):
            recieve_file(socket, data.decode("utf-8"))
        else:
            store_message.append(message)


# Fungsi untuk mengirim pesan teks ke alamat tertentu dan menyimpannya di store_message
def send_message(socket, address, message):
    store_message.append(f"Server Dharma ke {address}: {message}")
    socket.sendto(message.encode("utf-8"), address)


# Fungsi untuk mengirim file ke alamat tertentu berdasarkan format yang dipilih
def send_file(socket, server_address, file_format):
    if file_format == 3:
        file_path = "Server_Dharma/Dharma.pdf"
    elif file_format == 4:
        file_path = "Server_Dharma/Dharma.jpg"
    elif file_format == 5:
        file_path = "Server_Dharma/Dharma.mp3"
    elif file_format == 6:
        file_path = "Server_Dharma/Dharma.mp4"

    file_name = os.path.basename(file_path)
    file_size = str(os.path.getsize(file_path))

    socket.sendto(f"{file_name},{file_size}".encode(), server_address)

    with open(file_path, "rb") as file:
        for data in iter(lambda: file.read(4096), b""):
            socket.sendto(data, server_address)

    socket.sendto("File berhasil dikirim!".encode('utf-8'), server_address)
    store_message.append(f"File {file_name} berhasil terkirim ke {server_address}!")


# Fungsi untuk menerima file yang dikirim dan menyimpannya ke folder tujuan
def recieve_file(socket, file_info):
    file_info = file_info.split(",")
    file_name = file_info[0]
    file_size = int(file_info[1])

    destination_folder = "download_dharma"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    file_path = os.path.join(destination_folder, file_name)

    with open(file_path, "wb") as file:
        received_bytes = 0
        while received_bytes < file_size:
            data, _ = socket.recvfrom(4096)
            received_bytes += len(data)
            file.write(data)

    store_message.append(f"File berhasil diterima: {file_path}")


# Fungsi untuk memilih mode pengiriman pesan atau file
def mode_pesan():
    print("1. Kirim 1 kalimat\n2. Kirim 1 paragraph\n3. Kirim dokumen (docx/pdf)\n4. Kirim gambar (jpg/png)\n5. Kirim suara (mp3)\n6. Kirim video (mp4)")
    return int(input("Pilih mode pesan : "))


# Fungsi untuk menjalankan thread penerima pesan
def threading_slot():
    recv_thread = threading.Thread(target=recieve_message, args=(sockConfig.socket,))
    recv_thread.daemon = True
    recv_thread.start()


# Fungsi utama yang menjalankan logika aplikasi. Fungsi ini mengatur thread untuk penerimaan pesan dan meminta input pengguna untuk memilih metode pengiriman (unicast, multicast, broadcast) serta mode pesan
def main():
    threading_slot()

    while True:
        showMessage()
        choose = input(
            "1. Unicast\n2. Multicast\n3. Broadcast\n4. Lihat Pesan\nPilih metode: ")

        if choose == "1":
            print("Pilih IP:")
            for idx, address in enumerate(list_IP):
                print(f"{idx}. {address}")
            dst = int(input("Masukkan IP tujuan: "))

            mode = mode_pesan()
            if mode == 1:
                message = input("Masukkan pesan: ")
                send_message(sockConfig.socket, list_IP[dst], message)
            elif mode == 2:
                message = []
                print("Input paragraf:")
                while True:
                    message.append(input("Ketik (.) untuk berhenti: "))
                    if message[-1] == ".":
                        message = ". ".join(message)
                        break
                send_message(sockConfig.socket, list_IP[dst], message)
            elif mode == 3:
                send_file(sockConfig.socket, list_IP[dst], 3)
            elif mode == 4:
                send_file(sockConfig.socket, list_IP[dst], 4)
            elif mode == 5:
                send_file(sockConfig.socket, list_IP[dst], 5)
            elif mode == 6:
                send_file(sockConfig.socket, list_IP[dst], 6)
        elif choose == "2":
            multicast(sockConfig.socket)
        elif choose == "3":
            broadcast(sockConfig.socket)
        else:
            pass

        os.system("cls")

if __name__ == "__main__":
    main()