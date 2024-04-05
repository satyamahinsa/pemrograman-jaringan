from numpy import pi

# Percobaan
# Menghitung jumlah huruf
kata = input("Masukkan input: ")
print("Jumlah karakter pada {} adalah {}".format(kata, len(kata)))

# Menghitung luas dan keliling lingkaran
r = int(input("Masukkan jari-jari: "))
luas = pi * (r**2)
keliling = 2 * pi * r
print("Lingkaran dengan jari-jari sebesar {} memiliki\nLuas: {} dan Keliling: {}".format(r, luas, keliling))

# Mengubah suhu dari Fahrenheit ke Celcius atau sebaliknya
def fh_to_cel(fahrenheit):
    return (fahrenheit - 32) * 5/9

def cel_to_fh(celcius):
    return (celcius * 5/9) + 32

pilihan = input("1. Fahrenheit ke celcius \n2. Celcius ke Fahrenheit \nPilih konversi suhu: ")

if pilihan == '1':
    fahrenheit = float(input("Masukkan suhu dalam Fahrenheit: "))
    celcius = fh_to_cel(fahrenheit)
    print("{:.2f} Fahrenheit sama dengan {:.2f} Celcius".format(fahrenheit, celcius))
elif pilihan == '2':
    celcius = float(input("Masukkan suhu dalam Celcius: "))
    fahrenheit = cel_to_fh(celcius)
    print("{:.2f} Celcius sama dengan {:.2f} Fahrenheit".format(celcius, fahrenheit))
else:
    print("Pilihan tidak valid")

# Mencetak bilangan genap dari 1 hingga 100
for i in range(1, 101):
    if i % 2 == 0:
        print(i, end=" ")
print("\n")


# Tugas
# Bilangan prima
def cek_prima(n):
    prima = True
    for i in range(2, n):
        if n % i == 0:
            prima = False
            break
    return prima

input_prima = int(input("Masukkan batasan: "))
for i in range(2, input_prima + 1):
    if cek_prima(i):
        print(i, end=" ")
print("\n")

for i in range(1, int(input("Masukkan n: ")) + 1):
    if (i % 3 == 0) and (i % 4 == 0):
        print("OKYES")
    elif i % 3 == 0:
        print("OK")
    elif i % 4 == 0:
        print("YES")
    else:
        print(i)
