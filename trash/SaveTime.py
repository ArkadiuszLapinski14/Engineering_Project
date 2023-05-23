import time

def save_current_time():
    current_time = int(time.time())
    filename = "current_time.txt"
    with open(filename, "w") as file:
        file.write(str(current_time))
    print(f"Zapisano obecny czas ({current_time} sekundy) do pliku {filename}.")