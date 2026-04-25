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

def main():
    while True:
        ocisti_ekran()
        prikazi_meni()
        
        izbor = input("Vaš odabir: ")

        if izbor == '1':
            ocisti_ekran()
            print("--- SJF (Non-Preemptive) ---")
            # Ovdje ćemo kasnije dodati funkciju za unos i proračun
            input("\nOpcija u razvoju. Pritisnite bilo koju tipku za povratak...")
            
        elif izbor == '2':
            ocisti_ekran()
            print("--- Shortest Remaining Time First (SRTF) ---")
            input("\nOpcija u razvoju. Pritisnite bilo koju tipku za povratak...")
            
        elif izbor == '3':
            ocisti_ekran()
            print("--- Priority Scheduling ---")
            input("\nOpcija u razvoju. Pritisnite bilo koju tipku za povratak...")
            
        elif izbor == '4':
            print("\nIzlazak iz sistema...")
            break
            
        else:
            print("\nGreška: Nevalidna opcija. Pokušajte ponovo.")
            time.sleep(1)

if __name__ == "__main__":
    main()
