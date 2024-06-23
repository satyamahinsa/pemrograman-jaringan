import socket
import threading
import os


store_message = []
list_IP = [
    ("127.0.0.2", 8001),
    ("127.0.0.3", 8002),
    ("127.0.0.4", 8003),
    ("127.0.0.5", 8004),
    ("127.0.0.6", 8005),
    ("127.0.0.8", 8007),
    ("127.0.0.9", 8008),
    ("127.0.0.10", 8009),
    ("127.0.0.11", 8010),
]


class sockConfig:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_address = ("127.0.0.7", 8006)
    socket.bind(local_address)


def showMessage():
    print("Pesan baru:")
    for message in store_message:
        print(message)


def multicast(socket):
    remaining_IPs = list_IP[:]  # Salin list_IP ke remaining_IPs agar bisa dimodifikasi
    pilihan_ip = []

    while True:
        print("Pilih IP:")
        for idx, address in enumerate(remaining_IPs):
            print(f"{idx}. {address}")
        print("4. Exit")

        list_index = int(input("Masukkan IP tujuan: "))
        if list_index == 4:
            break
        if list_index < len(remaining_IPs):
            pilihan_ip.append(remaining_IPs[list_index])
            remaining_IPs.pop(list_index)  # Hapus IP yang dipilih dari remaining_IPs
        os.system("cls")

    # PENGIRIMAN
    mode = mode_pesan()
    if mode == 1:
        message = input("Masukkan pesan: ")
        for ip in pilihan_ip:
            send_message(socket, ip, message)
    elif mode == 2:
        message = []
        print("Input paragraf:")
        while True:
            message.append(input("Ketik (.) untuk berhenti: "))
            if message[-1] == ".":
                message = ". ".join(message)
                break
        for ip in pilihan_ip:
            send_message(socket, ip, message)
    elif mode == 3:
        for ip in pilihan_ip:
            send_file(socket, ip, 3)
    elif mode == 4:
        for ip in pilihan_ip:
            send_file(socket, ip, 4)
    elif mode == 5:
        for ip in pilihan_ip:
            send_file(socket, ip, 5)
    elif mode == 6:
        for ip in pilihan_ip:
            send_file(socket, ip, 6)


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


def recieve_message(socket):
    while True:
        data, address = socket.recvfrom(4096)
        message = f"From: {address} : {data.decode('utf-8')}"

        formats = ["docx", "pdf", "jpg", "png", "mp3", "mp4"]
        if any(format in message for format in formats):
            recieve_file(socket, data.decode("utf-8"))
        else:
            store_message.append(message)


def send_message(socket, address, message):
    store_message.append(f"Server 7 ke {address}: {message}")
    socket.sendto(message.encode("utf-8"), address)


def send_file(socket, server_address, file_format):
    if file_format == 3:
        file_path = "server7/server7.pdf"
    elif file_format == 4:
        file_path = "server7/server7.jpg"
    elif file_format == 5:
        file_path = "server7/server7.mp3"
    elif file_format == 6:
        file_path = "server7/server7.mp4"

    file_name = os.path.basename(file_path)
    file_size = str(os.path.getsize(file_path))

    socket.sendto(f"{file_name},{file_size}".encode(), server_address)

    with open(file_path, "rb") as file:
        for data in iter(lambda: file.read(4096), b""):
            socket.sendto(data, server_address)

    socket.sendto("File berhasil dikirim!".encode('utf-8'), server_address)
    store_message.append(f"File {file_name} berhasil terkirim ke {server_address}!")


def recieve_file(socket, file_info):
    file_info = file_info.split(",")
    file_name = file_info[0]
    file_size = int(file_info[1])

    destination_folder = "download_server7"
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


def mode_pesan():
    print("1. Kirim 1 kalimat\n2. Kirim 1 paragraph\n3. Kirim dokumen (pdf)\n4. Kirim gambar (jpg)\n5. Kirim suara (mp3)\n6. Kirim video (mp4)")
    return int(input("Pilih mode pesan : "))


def threading_slot():
    recv_thread = threading.Thread(target=recieve_message, args=(sockConfig.socket,))
    recv_thread.daemon = True
    recv_thread.start()


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