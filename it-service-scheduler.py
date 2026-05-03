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

def SJFAlgorithm(lista_tiketa): 
    trenutno_vrijeme = 0 # alocirano vrijeme gdje mjerimo sve operacije /poredimo ih s ovom nulom koja raste
    zavrseni_tiketi = [] #appendaju se zavrseni procesi nakon obrade u ovu listu

    while len(lista_tiketa) > 0:
        dostupni = [] #procesi koji su vec stigli u sistem
        for t in lista_tiketa:
            if t["dolazak"] <= trenutno_vrijeme: 
                dostupni.append(t) #prolazak kroz citavu listu tiketa, provjeravamo da li je vrijeme dolaska manje ili vece od 
                #trenutnog vremena, ako jeste, dodajemo ga u privremenu listu dostupnih procesa koji su stigli u sistem i cekaju svoj red
            #ovo fakticki simulira kao "fizicki red" u cekaonici, samo oni koji su prisutni ulaze u izbor, 
            #npr ako je t["dolazak"] = 12, a trenutno_vrijeme = 10, program "vidi" da 
            #jos nije usao u procese i ignorise ga dok trenutno_vrijeme ne otkuca na 12

        if len(dostupni) == 0: #ako niko nije stigao, vrijeme se mora nastaviti otkucavati, tako da pse povecava za 1
            trenutno_vrijeme+=1 #povecava se za jednu jedinicu vremena dok se neko ne pojavi
            continue #vracanje na pocetak while petlje da provjerimo je li iko stigao i ko je
        
        najkraci = dostupni[0]
        for t in dostupni:
            if t["trajanje"] < najkraci["trajanje"]: najkraci = t
        #uzimamo (pretpostavljamo) da je najkraci proces prvi u nizu dostupnih, 
        # i onda provjeravamo prolazimo kroz citavu listu dostupnih 
        #provjeravamo da li postoji ikakav proces kojem je trajanje (burst time) manji od zadanog, ako jeste on postaje novi najkraci

        trenutno_vrijeme += najkraci["trajanje"] # -> non-preemptive (znaci da kada jednom se odlucimo za rasporedjivanje procesa - on se mora uraditi do kraja bez prekida)
        #npr ako je trenutno_vrijeme bio na 5.minuti, a usluga traje 10 minuta -> automatski ih sabiramo 
        # i postavljamo trenutno_vrijeme na 15.minutu (to znaci da je procesor bio zauzet cijelo to vrijeme i nije mogao gledati druge narudzbe)
    
        najkraci["kraj"] = trenutno_vrijeme #ovdje upisujemo tacno kada je klijent dobio uslugu

        najkraci["tat"] = najkraci["kraj"] - najkraci["dolazak"] #tat - ukupno vrijeme koje je proces proveo u sistemu (od ulasksa od zavrsetka)
        #npr. klijent je poslao request u 5.minuti (dolazak), a usluga stize tek u 20.minuti(kraj)
        # njegov turnaround time (tat) je 20-5 = 15
        najkraci["wt"] = najkraci["tat"] - najkraci["trajanje"] #wt - waiting time(vrijeme cekanja) 
        #npr. klijent je ukupno bio u sistemu 15 minuta (tat), a sama priprema traje 10 minuta (trajanje)
        #to znaci da 5 minuta je samo chillao i cekao da neko uopste pocne raditi na njegovom requestu

        zavrseni_tiketi.append(najkraci) # kada imamo zavrsena popunjena sva polja, prebacujemo privremenu listu najkraci u listu zavrsenih poslova
        lista_tiketa.remove(najkraci) #brise taj tiket iz glavne liste
    return zavrseni_tiketi

def ispis(rezultati):
    print("\n" + "="*30)
    print("       FINALNI IZVJEŠTAJ")
    print("="*30)
    
    for r in rezultati:
        # Provjeri da li su ključevi tačni: 'id', 'dolazak', 'trajanje', 'kraj', 'tat', 'wt'
        print(f"ID: {r['id']} | "
              f"Dolazak: {r['dolazak']} min | "
              f"Trajanje: {r['trajanje']} min | "
              f"Kraj: {r['kraj']} | "
              f"TAT: {r['tat']} | "
              f"WT: {r['wt']}")
    
    suma_tat = 0
    suma_wt = 0
    n = len(rezultati)
    
    for r in rezultati:
        suma_tat += r['tat']
        suma_wt += r['wt']
    
    print("-" * 30)
    # Prikaz prosjeka na dvije decimale
    print(f"Prosječan TAT: {suma_tat / n:.2f} min")
    print(f"Prosječan WT: {suma_wt / n:.2f} min")
    input("\nPrisitni bilo sta za nastavak...")

def main(): 
    while True:
        ocisti_ekran()
        prikazi_meni()
        
        izbor = input("Vaš odabir: ")

        if izbor == '1':
            ocisti_ekran()
            print("--- SJF (Non-Preemptive) ---")
            tiketi = unos_podataka(ima_priority=False)
            rezultat = SJFAlgorithm(tiketi)
            ispis(rezultat)
            
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
