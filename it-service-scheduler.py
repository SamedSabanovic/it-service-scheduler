import os
import time


def ocisti_ekran():
    # Funkcija za brisanje terminala kako bi meni uvijek bio na vrhu
    os.system('cls' if os.name == 'nt' else 'clear')

def prikazi_meni():
    print("\n" + "="*50)
    print("       IT SERVICE - SISTEM ZA UPRAVLJANJE TIKETIMA")
    print("="*50)
    print("Izaberite neki od sljedeće ponuđenih algoritama:")
    print("-" * 50)
    print("[1] Shortest Job First (SJF - Non-Preemptive)")
    print("[2] Shortest Job First preemptive (SRTF)")
    print("[3] Priority Scheduling")
    print("[4] Izlaz iz aplikacije")
    print("-" * 50)

def unos_podataka(ima_priority = False): 
    #Unos broja tiketa
    brojTiketa = int(input("\n Unesi ukupan broj narudžbi/tiketa: "))
    lista_tiketa = []

    for i in range(brojTiketa):
        print(f"\n--- Podaci za tiket br. {i+1} ---")

        # Vrijeme dolaska: npr. 0 ako je narudžba tu odmah, ili 5 ako stiže kasnije
        dolazak = int(input("Vrijeme dolaska narudžbe (min): "))
        # Burst time: koliko minuta nam treba da završimo posao
        trajanje = int(input("Vrijeme pripreme narudžbe (min): "))
        
        #isti fazon kao i struct u c++, inicijalizacija strukture(rjecnika) za jedan tiket
        tiket = {
            "id": i + 1,
            "dolazak": dolazak,
            "trajanje": trajanje,
            "preostalo": trajanje,  # Pocinje sa punim trajanjem (for SRTF)
            "prioritet": 0,
            "kraj": 0,              # Vrijeme kada je posao završen
            "tat": 0,               # Turnaround Time (Ukupno vrijeme u sistemu)
            "wt": 0                 # Waiting Time (Vrijeme čekanja)
        }

        if (ima_priority): 
            tiket["prioritet"] = int(input("Prioritet (0 - najveći): "))
        
        lista_tiketa.append(tiket)
    return lista_tiketa

def main(): 
    while True:
        ocisti_ekran()
        prikazi_meni()
        
        izbor = input("Vaš odabir: ")

        if izbor == '1':
            ocisti_ekran()
            print("--- SJF (Non-Preemptive) ---")
            tiketi = unos_podataka(ima_priority=False)
            
        elif izbor == '2':
            ocisti_ekran()
            print("--- Shortest Remaining Time First (SRTF) ---")
            tiketi = unos_podataka(ima_priority=False)
            
        elif izbor == '3':
            ocisti_ekran()
            print("--- Priority Scheduling ---")
            tiketi = unos_podataka(ima_priority = True)
            
        elif izbor == '4':
            print("\nIzlazak iz sistema...")
            break
            
        else:
            print("\nGreška: Nevalidna opcija. Pokušajte ponovo.")
            time.sleep(1)

if __name__ == "__main__":
    main()
