import socket
import threading
import os

store_message = []
list_IP = [
    ("192.168.8.204", 8002), # dharma
    ("192.168.8.104", 8003), # daffa
    # ("192.168.168.204", 8001), # dharma
]


# Create a UDP socket
class socketConfig:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_address = ("192.168.8.148", 8004)
    socket.bind(local_address)


def show_message():
    for message in store_message:
        print(message)


def multicast(socket):
    choose = []
    for i in range(len(list_IP)):
        print("Pilih IP:")
        for idx, address in enumerate(list_IP):
            print(f"{idx + 1}. {address}")
        print("4. Exit")

        list_index = int(input("Masukkan IP tujuan: "))
        if list_index == 4:
            break
        choose.append(list_index)
        os.system("cls")
        
    # PENGIRIMAN
    mode = mode_pesan()
    if mode == 1:
        message = input("Masukan pesan: ")
        for i in choose:
            socket.sendto(message.encode("utf-8"), list_IP[i])
    elif mode == 2:
        message = []
        print("Input paragraf:")
        while True:
            message.append(input("Ketika (.) untuk berhenti: "))
            if message[-1] == ".":
                message = ". ".join(message)
                break
        for i in choose:
            socket.sendto(message.encode("utf-8"), list_IP[i])
    elif mode == 3:
        for i in choose:
            send_file(socket, list_IP[i], 3)
    elif mode == 4:
        for i in choose:
            send_file(socket, list_IP[i], 4)
    elif mode == 5:
        for i in choose:
            send_file(socket, list_IP[i], 5)
    elif mode == 6:
        for i in choose:
            send_file(socket, list_IP[i], 6)


def broadcast(socket):
    mode = mode_pesan()
    if mode == 1:
        message = input("Masukan pesan: ")
        for ip in list_IP:
            socket.sendto(message.encode("utf-8"), ip)
    elif mode == 2:
        message = []
        print("Input paragraf:")
        while True:
            message.append(input("Ketik (.) untuk berhenti : "))
            if message[-1] == ".":
                message = ". ".join(message)
                break
        for ip in list_IP:
            socket.sendto(message.encode("utf-8"), ip)
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


def receive_message(socket):
    while True:
        data, address = socket.recvfrom(1024)
        message = f"From: {address} : {data.decode('utf-8')}"

        formats = ["docx", "pdf", "jpg", "png", "mp3", "mp4"]
        if any(format in message for format in formats):
            receive_file(socket, data.decode("utf-8"))
        else:
            store_message.append(message)


def send_message(socket, address):
    response = input("Masukkan pesan: ")
    if response != "":
        store_message.append(f"Server Satya: {response}")
        socket.sendto(response.encode("utf-8"), address)


def threading_slot():
    recv_thread = threading.Thread(target=receive_message, args=(socketConfig.socket,))
    recv_thread.daemon = True
    recv_thread.start()


def send_file(socket, server_address, file_format):
    if file_format == 3:
        file_path = "satya/satya.pdf"
    elif file_format == 4:
        file_path = "satya/satya.jpg"
    elif file_format == 5:
        file_path = "satya/satya.mp3"
    elif file_format == 6:
        file_path = "satya/satya.mp4"

    file_name = os.path.basename(file_path)
    file_size = str(os.path.getsize(file_path))

    socket.sendto(f"{file_name},{file_size}".encode(), server_address)

    with open(file_path, "rb") as file:
        # progress = tqdm.tqdm(unit="b", unit_scale=True, unit_divisor=1000, total=file_size)
        for data in iter(lambda: file.read(4096), b""):
            socket.sendto(data, server_address)
            # progress.update(len(data))

    socket.sendto(b"File send succesfully!", server_address)
    store_message.append(f"File {file_name} send succesfully!")


def receive_file(socket, file_info):
    file_info = file_info.split(",")
    file_name = file_info[0]
    file_size = int(file_info[1])

    destination_folder = "download_satya"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    file_path = os.path.join(destination_folder, file_name)

    with open(file_path, "wb") as file:
        received_bytes = 0
        # progress = tqdm.tqdm(unit="b", unit_scale=True, unit_divisor=1000, total=file_size)
        while received_bytes < file_size:
            data, _ = socket.recvfrom(4096)
            received_bytes += len(data)
            file.write(data)
            # progress.update(len(data))

    store_message.append(f"File berhasil diterima: {file_path}")


def mode_pesan():
    print("1. Kirim 1 kalimat\n2. Kirim 1 paragraph\n3. Kirim dokumen (docx/pdf)\n4. Kirim gambar (jpg/png)\n5. Kirim suara (mp3)\n6. Kirim video (mp4)")
    return int(input("Pilih mode pesan: "))


def main():
    threading_slot()

    while True:
        show_message()
        choose = input("1. Unicast\n2. Multicast\n3. Broadcast\n4. Lihat Pesan\nPilih metode: ")

        if choose == "1":
            print("Pilih IP:")
            for idx, address in enumerate(list_IP):
                print(f"{idx}. {address}")
            dst = int(input("Masukkan IP tujuan: "))

            mode = mode_pesan()
            if mode == 1:
                send_message(socketConfig.socket, list_IP[dst])
            elif mode == 2:
                message = []
                print("Input paragraf:")
                while True:
                    message.append(input("Ketik (.) untuk berhenti : "))
                    if message[-1] == ".":
                        message = ". ".join(message)
                        break
            elif mode == 3:
                send_file(socketConfig.socket, list_IP[dst], 3)
            elif mode == 4:
                send_file(socketConfig.socket, list_IP[dst], 4)
            elif mode == 5:
                send_file(socketConfig.socket, list_IP[dst], 5)
            elif mode == 6:
                send_file(socketConfig.socket, list_IP[dst], 6)
        elif choose == "2":
            multicast(socketConfig.socket)
        elif choose == "3":
            broadcast(socketConfig.socket)
        else:
            pass

        os.system("cls")
        


if __name__ == "__main__":
    main()