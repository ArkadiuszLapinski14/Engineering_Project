import time

def save_time_difference():
    current_time = int(time.time())
    filename = "current_time.txt"

    with open(filename, "a") as file:
        file.write("\n")  # Dodanie nowej linii przed zapisem różnicy czasu

        if not file.tell():  # Sprawdzenie, czy plik jest pusty
            file.write("0")  # Jeśli pusty, zapisanie 0 jako pierwszą wartość

        file.seek(0)  # Przejście na początek pliku
        previous_time = int(file.read().strip())  # Wczytanie poprzedniego czasu z pliku
        time_difference = current_time - previous_time  # Obliczenie różnicy czasu

        file.seek(0, 2)  # Przejście na koniec pliku
        file.write(f"{time_difference}\n")  # Zapisanie różnicy czasu na końcu pliku

    print(f"Zapisano różnicę czasu ({time_difference} sekundy) do pliku {filename}.")