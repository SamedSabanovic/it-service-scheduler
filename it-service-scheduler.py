import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# global list sa privremenim tiketima koji se unose preko forme, a zatim se obradjuju kada se pokrene algoritam
privremeni_tiketi = []

def osvjezi_formu():
    # ako je izabran Priority Scheduling (vrijednost "3"), prikat ce se polje za prioritet
    if izbor_algoritma.get() == "3":
        lbl_prioritet.grid()
        ent_prioritet.grid()
    else:
        lbl_prioritet.grid_remove()
        ent_prioritet.grid_remove()

def dodaj_tiket():
    try:
        dolazak = int(ent_dolazak.get())
        trajanje = int(ent_trajanje.get())
        prioritet = 0
        
        if izbor_algoritma.get() == "3":
            prioritet = int(ent_prioritet.get())

        sljedeci_id = len(privremeni_tiketi) + 1 #+1 jer id pocinje od 1, a ne od 0, tako da prvi tiket ima id 1, drugi 2 itd.
        
        # isti fazon kao i struct u c++, inicijalizacija strukture(rjecnika) za jedan tiket
        tiket = {
            "id": sljedeci_id,
            "dolazak": dolazak,
            "trajanje": trajanje,
            "preostalo": trajanje,  # Pocinje sa punim trajanjem (for SRTF)
            "prioritet": prioritet,
            "kraj": 0,              # Vrijeme kada je posao zavrsen
            "tat": 0,               # Turnaround Time (Ukupno vrijeme u sistemu)
            "wt": 0                 # Waiting Time (Vrijeme cekanja)
        }
        
        privremeni_tiketi.append(tiket)
        
        # Upisujemo u tabelu na ekranu (prikazujemo prazna polja za rezultate za sada)
        tabela.insert("", "end", values=(tiket["id"], tiket["dolazak"], tiket["trajanje"], tiket["prioritet"], "", "", ""))
        
        # Brisanje unosa iz polja nakon uspjesnog dodavanja, 
        # da bi korisnik mogao unijeti novi tiket bez potrebe 
        # da rucno brise prethodne unose
        ent_dolazak.delete(0, tk.END)
        ent_trajanje.delete(0, tk.END)
        ent_prioritet.delete(0, tk.END)
        
    except ValueError:
        messagebox.showerror("Greska", "Molimo unesite ispravne numericke vrijednosti.")

# funkcija za non-preemptive SJF algoritam, koji se poziva kada korisnik izabere opciju 1 
# preko radio buttona, i prima listu tiketa koja se koristi samo za obradu algoritma, 
# a original lista tiketa ostaje netaknuta za prikaz u tabeli, 
# jer algoritam ce mijenjati polja poput "kraj", "tat" i "wt"
# algoritam radi tako sto prvo provjerava koji su tiketi stigli u sistem 
# (dolazak <= trenutno_vrijeme), zatim od tih dostupnih tiketa bira onaj sa najkracim trajanjem, 
# i onda ga obradi do kraja (non-preemptive), azurira vrijeme kraja, TAT i WT,
# i onda ga prebaci u listu zavrsenih tiketa, 
# dok se originalna lista tiketa koristi samo za prikaz u tabeli
def SJFAlgorithmNonPE(lista_tiketa): 
    trenutno_vrijeme = 0 # alocirano vrijeme gdje mjerimo sve operacije 
    #/poredimo ih s ovom nulom koja raste
    zavrseni_tiketi = [] #appendaju se zavrseni procesi nakon obrade u ovu listu
    dnevnik_rada = [] # privremena lista u koju upisujemo tekstualne recenice o radu procesora, da bi profesor vidio hronologiju

    while len(lista_tiketa) > 0:
        dostupni = [] #procesi koji su vec stigli u sistem
        for t in lista_tiketa:
            if t["dolazak"] <= trenutno_vrijeme: 
                dostupni.append(t) #prolazak kroz citavu listu tiketa, provjeravamo da li je vrijeme dolaska manje ili vece od 
                #trenutnog vremena, ako jeste, dodajemo ga u privremenu listu dostupnih procesa koji su stigli u sistem i cekaju svoj red

        if len(dostupni) == 0: #ako niko nije stigao, vrijeme se mora nastaviti otkucavati, tako da pse povecava za 1
            # u dnevnik upisujemo da u ovoj minuti procesor nema sta da radi jer nijedna narudzba jos nije stigla
            dnevnik_rada.append(f"Minuta {trenutno_vrijeme}: Procesor besposlen (nema narudzi).")
            trenutno_vrijeme+=1 #povecava se za jednu jedinicu vremena dok se neko ne pojavi
            continue #vracanje na pocetak while petlje da provjerimo je li iko stigao i ko je

        najkraci = dostupni[0]
        for t in dostupni:
            if t["trajanje"] < najkraci["trajanje"]: najkraci = t
        #uzimamo (pretpostavljamo) da je najkraci proces prvi u nizu dostupnih, 
        # i onda provjeravamo prolazimo kroz citavu listu dostupnih 
        #provjeravamo da li postoji ikakav proces kojem je trajanje (burst time) manji od zadanog, ako jeste on postaje novi najkraci

        # spasavamo pocetnu minutu rada na ovom tiketu prije nego sto povecamo sistemski sat
        pocetak = trenutno_vrijeme
        trenutno_vrijeme += najkraci["trajanje"] # -> non-preemptive 
        #(znaci da kada jednom se odlucimo za rasporedjivanje procesa 
        #- on se mora uraditi do kraja bez prekida)
        #npr ako je trenutno_vrijeme bio na 5.minuti, a usluga traje 10 minuta -> 
        # automatski ih sabiramo 
        # i postavljamo trenutno_vrijeme na 15.minutu (to znaci da je procesor bio zauzet 
        # cijelo to vrijeme i nije mogao gledati druge narudzbe)
        
        # nakon sto smo obradili cijeli tiket, u dnevnik upisujemo tacno od koje do koje minute je radio taj tiket bez ikakvih prekida
        dnevnik_rada.append(f"Minuta {pocetak} do {trenutno_vrijeme}: Izvodi se Tiket #{najkraci['id']} bez prekidanja (Trajanje: {najkraci['trajanje']} min).")
    
        najkraci["kraj"] = trenutno_vrijeme #ovdje upisujemo tacno kada je klijent dobio uslugu

        najkraci["tat"] = najkraci["kraj"] - najkraci["dolazak"] #tat - 
        #ukupno vrijeme koje je proces proveo u sistemu (od ulasksa od zavrsetka)
        #npr. klijent je poslao request u 5.minuti (dolazak), a usluga stize tek u 20.minuti(kraj)
        # njegov turnaround time (tat) je 20-5 = 15
        najkraci["wt"] = najkraci["tat"] - najkraci["trajanje"] #wt - waiting time(vrijeme cekanja) 
        #npr. klijent je ukupno bio u sistemu 15 minuta (tat), a sama priprema traje 10 minuta (trajanje)
        #to znaci da 5 minuta je samo chillao i cekao da neko uopste pocne raditi na njegovom requestu

        zavrseni_tiketi.append(najkraci) # kada imamo zavrsena popunjena sva polja, prebacujemo privremenu listu najkraci u listu zavrsenih poslova
        lista_tiketa.remove(najkraci) #brise taj tiket iz glavne liste
        
    return zavrseni_tiketi, dnevnik_rada # vracamo i gotove tikete za tabelu ali i dnevnik koji ce se ispisati u tekstualno polje


# funkcija za SJF preemptive(SRTF), radi na slican nacin kao i non-preemptive, 
# ali sa jednom bitnom razlikom, da svi procesi koji su dostupni (stigli u sistem) se provjeravaju na svakoj jedinici vremena,
# i ako se pojavi novi proces sa kracim trajanjem od trenutno izvrsenog procesa, 
# trenutni proces se prekida (preempted) i novi proces sa kracim trajanjem se pocinje izvrsavati
def SJFAlgorithmPE(lista_tiketa): 
    trenutno_vrijeme = 0 # alocirano vrijeme gdje mjerimo sve operacije 
    # /poredimo ih s ovom nulom koja raste
    zavrseni_tiketi = [] #appendaju se zavrseni procesi nakon obrade u ovu listu
    dnevnik_rada = [] # privremena lista u koju upisujemo desavanja minutu po minutu, ukljucujuci i prekide koji se dese
    
    zadnji_izvrsavani_id = None # varijabla koja pamti id tiketa koji je radio u prosloj minuti, pomocu nje znamo da li je doslo do prekida

    while len(lista_tiketa) > 0:
        dostupni = [] #privremena lista dostupnih procesa koji su stigli u sistem
        for t in lista_tiketa: 
            if t["dolazak"] <= trenutno_vrijeme: 
                dostupni.append(t) #prolazak kroz citavu listu tiketa, 
                #provjeravamo da li je vrijeme dolaska manje ili vece od 
                #trenutnog vremena, ako jeste, dodajemo ga u privremenu listu 
                #dostupnih procesa koji su stigli u sistem i cekaju svoj red

        if len(dostupni) == 0:
            # ako nema nikoga u redu, biljezimo to u dnevnik, povecavamo sat i resetujemo zadnji id jer procesor odmaram
            dnevnik_rada.append(f"Minuta {trenutno_vrijeme}: Procesor besposlen (nema narudzi).")
            trenutno_vrijeme += 1
            zadnji_izvrsavani_id = None
            continue # ako niko nije stigao, 
        #vrijeme se mora nastaviti otkucavati, 
        # tako da pse povecava za 1, i vraca se na pocetak while petlje 
        # da provjeri je li iko stigao i ko je (isto kao i kod non-preemptive)

        najkraci = dostupni[0] #uzimamo (pretpostavljamo) da je najkraci proces 
        #prvi u nizu dostupnih, i onda provjeravamo prolazimo kroz citavu listu dostupnih
        for t in dostupni: 
            if t["preostalo"] < najkraci["preostalo"]:
                najkraci = t #provjeravamo da li postoji ikakav proces 
                #kojem je preostalo vrijeme (remaining time) manji od zadanog, 
                #ako jeste on postaje novi najkraci
        
        # uslov za detekciju prekida: ako je u prosloj minuti radio jedan tiket, a sada je odabran drugi tiket, to znaci da se desio prekid
        if zadnji_izvrsavani_id is not None and zadnji_izvrsavani_id != najkraci["id"]:
            # upisujemo poruku o prekidu u dnevnik, navodeci ko je prekinut, a ko je preuzeo procesor i koliko mu je minuta ostalo
            dnevnik_rada.append(f"-> PREKID u minuti {trenutno_vrijeme}: Zaustavlja se Tiket #{zadnji_izvrsavani_id}, preuzima se kraci Tiket #{najkraci['id']} (Preostalo: {najkraci['preostalo']} min).")
        # uslov za pocetak novog rada: ako je procesor bio slobodan ili je tek pokrenut tiket po prvi put
        elif zadnji_izvrsavani_id is None or zadnji_izvrsavani_id != najkraci["id"]:
            dnevnik_rada.append(f"Minuta {trenutno_vrijeme}: Pokrece se Tiket #{najkraci['id']} (Preostalo: {najkraci['preostalo']} min).")

        # azuriramo zadnji izvrsavani id da bi u narednoj minuti znali sta je radilo
        zadnji_izvrsavani_id = najkraci["id"]
        
        trenutno_vrijeme += 1 #povecavamo vrijeme za jednu jedinicu, 
        # jer se algoritam provjerava na svakoj jedinici vremena, 
        # vrijeme se racuna kao da su svi dostupni procesi cekali tu jedinicu vremena,
        # iako se izvrsava samo jedan proces, npr. ako trenutno_vrijeme je na 5.minuti, 
        # a imamo 3 procesa koji su stigli, svi oni cekaju tu jednu jedinicu vremena, 
        # ali se samo jedan proces izvrsava, onaj koji je odabran kao najkraci, 

        najkraci["preostalo"] -= 1 #smanjujemo preostalo vrijeme za odabrani proces,
        # jer se izvrsava ta jedinica vremena, npr. ako je preostalo vrijeme bilo 10 minuta, 
        # nakon izvrsavanja jedne jedinice vremena, preostalo vrijeme postaje 9 minuta, 
        # i tako dalje

        if najkraci["preostalo"] == 0: #ako je preostalo vrijeme postalo 0, 
        #znaci da je proces zavrsio
            # biljezimo u dnevnik da je ovaj konkretni tiket potpuno zavrsio svoj rad
            dnevnik_rada.append(f"Minuta {trenutno_vrijeme}: Tiket #{najkraci['id']} je USPJESNO KOMPLETIRAN.")
            najkraci["kraj"] = trenutno_vrijeme #ovdje upisujemo tacno kada je klijent dobio uslugu
            najkraci["tat"] = najkraci["kraj"] - najkraci["dolazak"] 
            #tat - ukupno vrijeme koje je proces proveo u sistemu (od ulasksa od zavrsetka)
            #npr. klijent je poslao request u 5.minuti (dolazak), a usluga stize tek u 20.minuti(kraj)
            # njegov turnaround time (tat) je 20-5 = 15
            najkraci["wt"] = najkraci["tat"] - najkraci["trajanje"]
            #wt - waiting time(vrijeme cekanja) 
            # npr. klijent je ukupno bio u sistemu 15 minuta (tat),
            # a trajanje procesa bilo 5 minuta, 
            # pa je vrijeme cekanja 15 - 5 = 10 minuta
            zavrseni_tiketi.append(najkraci) 
            # kada imamo zavrsena popunjena sva polja, 
            # prebacujemo privremenu listu najkraci u listu zavrsenih poslova
            lista_tiketa.remove(najkraci)
            #brise taj tiket iz glavne liste, ako je proces zavrsio,
            # uklanja se iz liste tiketa koji cekaju na obradu
            
            # resetujemo zadnji id na none jer je tiket gotov, pa u narednoj minuti biramo ponovo ispocetka
            zadnji_izvrsavani_id = None
            
    return zavrseni_tiketi, dnevnik_rada # vracamo listu kompletiranih tiketa i gotov dnevnik sa svim prekidima


#funkcija za prikaz rezultata u tabeli, koja se poziva nakon obrade algoritma, 
# i prima listu zavrsenih tiketa sa popunjenim poljima za kraj, tat i wt
def prikazi_rezultate_u_tabeli(rezultati, dnevnik):
    # omogucavamo pisanje u tekstualno polje dnevnika, brisemo stari tekst, upisujemo liniju po liniju novog dnevnika i ponovo ga zakljucavamo
    txt_dnevnik.config(state="normal")
    txt_dnevnik.delete("1.0", tk.END)
    for linija in dnevnik:
        txt_dnevnik.insert(tk.END, linija + "\n")
    txt_dnevnik.config(state="disabled")

    # cistimo tabelu od prethodnih rezultata prije nego sto upisemo nove, da ne bi bilo dupliranja podataka
    for stavka in tabela.get_children():
        tabela.delete(stavka)
        
    # sort po ID-u po redu, lambda funkcija nam pomaze da sortiramo listu rezultata po kljucu "id" koji je broj narudzbe, 
    # tako da se prikazuju u redoslijedu unosa, a ne po vremenu dolaska ili necemu drugom
    rezultati.sort(key=lambda x: x["id"])

    suma_tat = 0 
    suma_wt = 0

    for r in rezultati:
        # upisivanje gotovih podataka u tabelu, sada vec sa popunjenim poljima za kraj, tat i wt
        tabela.insert("", "end", values=(
            r["id"], r["dolazak"], r["trajanje"], r["prioritet"], r["kraj"], r["tat"], r["wt"]
        ))
        suma_tat += r["tat"] 
        suma_wt += r["wt"]

    # racunamo prosjecan TAT i WT, dijeljenjem ukupne sume sa brojem tiketa (n), i prikazujemo ih u labeli ispod tabele
    # n::.2f znaci da ce se broj formatirati sa 2 decimale, 
    # tako da dobijemo lijep i pregledan prikaz prosjecnih vrijednosti
    n = len(rezultati)
    lbl_statistika.config(text=f"Prosječan TAT: {suma_tat / n:.2f} min  |  Prosječan WT: {suma_wt / n:.2f} min")

#funkcija koja se poziva kada korisnik klikne na dugme "POKRENI OBRADU", 
# ona provjerava koji je algoritam izabran preko radio buttona
def pokreni_algoritam():
    # ako je lista tiketa prazna, ne mozemo pokrenuti algoritam, jer nema sta da se obradi, tako da prikazujemo upozorenje korisniku
    if not privremeni_tiketi:
        messagebox.showwarning("Upozorenje", "Lista tiketa je prazna. Unesite podatke prvo.")
        return

    algoritam = izbor_algoritma.get() #uzimamo vrijednost iz radio buttona da znamo koji algoritam je izabran, 
    #i onda na osnovu toga pokrecemo odgovarajuci kod
    
    # pravi se copy liste tiketa, da ne bi mijenjali originalnu listu tiketa koja se koristi za prikaz u tabeli,
    # jer algoritmi ce mijenjati polja poput "kraj", "tat" i "wt", a treba 
    # da tabela ostane netaknuta dok se ne prikazu rezultati, 
    # tako da pravimo novu listu koja ce se koristiti samo za obradu algoritma
    lista_za_obradu = [tiket.copy() for tiket in privremeni_tiketi]

    #konacan izbor algoritma, i pozivanje odgovarajuce funkcije, a zatim prikaz rezultata u tabeli
    if algoritam == "1":
        rezultati, dnevnik = SJFAlgorithmNonPE(lista_za_obradu)
        prikazi_rezultate_u_tabeli(rezultati, dnevnik)
    elif algoritam == "2":
        rezultati, dnevnik = SJFAlgorithmPE(lista_za_obradu)
        prikazi_rezultate_u_tabeli(rezultati, dnevnik)
    elif algoritam == "3":
        messagebox.showinfo("Priority", "Ovdje će ići tvoj Priority kôd.")

#standard cls funkcija koja cisti sve podatke i resetuje formu, 
# tako da korisnik moze poceti unositi nove tikete od nule
def ocisti_sve():
    privremeni_tiketi.clear()
    for stavka in tabela.get_children():
        tabela.delete(stavka)
    # cistimo tekstualno polje dnevnika i ponovo ga zakljucavamo
    txt_dnevnik.config(state="normal")
    txt_dnevnik.delete("1.0", tk.END)
    txt_dnevnik.config(state="disabled")
    lbl_statistika.config(text="Prosječan TAT: 0.00 min  |  Prosječan WT: 0.00 min")

#basic definicija glavnog prozora aplikacije, sa naslovom i dimenzijama, 
# a zatim se kreiraju svi potrebni widgeti (labela, entry, button, treeview) 
# i organizuju u odgovarajuce okvire (frame) da bi aplikacija bila pregledna i funkcionalna
root = tk.Tk()
root.title("IT Service - Sistem za upravljanje tiketima")
root.geometry("1000x1000")

# naslov aplikacije, i formatiranje fonta da bude veci i boldovan, da se istice na vrhu prozora
naslov = tk.Label(root, text="IT SERVICE - SISTEM ZA UPRAVLJANJE TIKETIMA", font=("Arial", 16, "bold"))
naslov.pack(pady=10)

# okvir za izbor algoritma, sa radio buttonima koji omogucavaju korisniku 
# da izabere koji algoritam zeli koristiti za obradu tiketa, 
# a zatim se poziva funkcija osvjezi_formu() koja ce prikazati ili sakriti polje za prioritet 
# u zavisnosti od izbora algoritma, fill="x" znaci da ce okvir zauzeti cijelu sirinu prozora, 
# a padx i pady dodaju malo prostora oko okvira
okvir_meni = tk.LabelFrame(root, text=" Izaberite neki od sljedeće ponuđenih algoritama ", font=("Arial", 10, "bold"), padx=10, pady=5)
okvir_meni.pack(fill="x", padx=20, pady=5)

# varijabla koja ce cuvati vrijednost izabranog radio buttona, 
# default je postavljen na "1" sto znaci da je SJF non-preemptive 
# izabran kao default opcija kada se aplikacija pokrene, 
# tako da korisnik odmah moze poceti unositi tikete bez potrebe da prvo bira algoritam, 
# a zatim se poziva funkcija osvjezi_formu() koja ce sakriti polje za prioritet 
# jer SJF ne koristi prioritet, 
# i prikazati ga samo kada korisnik izabere opciju 3 (Priority Scheduling)
izbor_algoritma = tk.StringVar(value="1")

#opcije radio buttona za izbor algoritma, svaki sa svojom vrijednoscu ("1" za SJF non-preemptive, "2" za SRTF, "3" za Priority), 
# i svaki poziva funkciju osvjezi_formu() kada se izabere, 
# da bi se prikazalo ili sakrilo polje za prioritet, anchor "w" znaci da ce tekst biti poravnat lijevo, 
# a pady=2 dodaje malo vertikalnog prostora izmedju radio buttona, 
# okvir_meni je roditeljski widget u koji se smjestaju radio buttoni
rb_sjf = ttk.Radiobutton(okvir_meni, text="Shortest Job First (SJF - Non-Preemptive)", variable=izbor_algoritma, value="1", command=osvjezi_formu)
rb_sjf.pack(anchor="w", pady=2)

rb_srtf = ttk.Radiobutton(okvir_meni, text="Shortest Job First preemptive (SRTF)", variable=izbor_algoritma, value="2", command=osvjezi_formu)
rb_srtf.pack(anchor="w", pady=2)

rb_priority = ttk.Radiobutton(okvir_meni, text="Priority Scheduling", variable=izbor_algoritma, value="3", command=osvjezi_formu)
rb_priority.pack(anchor="w", pady=2)

# okvir za unos podataka, gdje korisnik moze unijeti vrijeme dolaska narudzbe, vrijeme pripreme narudzbe, i prioritet (ako je izabran Priority Scheduling),
# a zatim klikom na dugme "Dodaj tiket" dodaje taj tiket u privremenu listu tiketa i prikazuje ga u tabeli, 
# fill="x" znaci da ce okvir zauzeti cijelu sirinu prozora, a padx i pady dodaju malo prostora oko okvira sa x i y ose
okvir_unos = tk.LabelFrame(root, text=" Unos podataka ", font=("Arial", 10, "bold"), padx=10, pady=5)
okvir_unos.pack(fill="x", padx=20, pady=5)

tk.Label(okvir_unos, text="Vrijeme dolaska (min):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
ent_dolazak = ttk.Entry(okvir_unos, width=8)
ent_dolazak.grid(row=0, column=1, padx=5, pady=5)

tk.Label(okvir_unos, text="Vrijeme pripreme (min):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
ent_trajanje = ttk.Entry(okvir_unos, width=8)
ent_trajanje.grid(row=0, column=3, padx=5, pady=5)

# polje za prioritet se kreira, ali se sakriva po defaultu, 
# jer aplikacija starta sa SJF opcijom koja ne koristi prioritet, 
# ali ce se prikazati kada korisnik izabere opciju 3 (Priority Scheduling) preko radio buttona
lbl_prioritet = tk.Label(okvir_unos, text="Prioritet (0 - najveći):")
lbl_prioritet.grid(row=0, column=4, sticky="w", padx=5, pady=5)
ent_prioritet = ttk.Entry(okvir_unos, width=8)
ent_prioritet.grid(row=0, column=5, padx=5, pady=5)

# Sakriveno polje po defaultu jer aplikacija starta sa SJF opcijom
lbl_prioritet.grid_remove()
ent_prioritet.grid_remove()

# dugme za dodavanje tiketa, koje poziva funkciju dodaj_tiket() kada se klikne, 
# a ta funkcija ce uzeti unesene podatke, kreirati tiket, dodati ga u privremenu listu tiketa, 
# i prikazati ga u tabeli, a zatim ocistiti polja za unos da bi korisnik mogao unijeti novi tiket
btn_dodaj = ttk.Button(okvir_unos, text="Dodaj tiket", command=dodaj_tiket)
btn_dodaj.grid(row=0, column=6, padx=15, pady=5)

# okvir za tekstualni dnevnik rada koji hronoloski prikazuje izvrsavanje i prekide procesa u realnom vremenu minutu po minutu
okvir_dnevnik = tk.LabelFrame(root, text=" Hronološki proces izvršavanja (Dnevnik rada) ", font=("Arial", 10, "bold"), padx=10, pady=5)
okvir_dnevnik.pack(fill="x", padx=20, pady=5)

# tekstualni widget u koji upisujemo recenice dnevnika, stavljen je na visinu 8 i zakljucan (disabled) da korisnik ne moze sam brisati tekst
txt_dnevnik = tk.Text(okvir_dnevnik, height=8, font=("Courier New", 10), state="disabled", bg="#f8f9fa")
txt_dnevnik.pack(fill="x", expand=True)

# tabela za prikaz tiketa, gdje se prikazuju svi unijeti tiketi sa njihovim vremenom dolaska, trajanjem, prioritetom (ako postoji),
# i nakon obrade algoritma, prikazuju se i vrijeme kraja, TAT i WT, okvir_tabela je parent widget u koji se smjesta tabela, 
# fill="both" znaci da ce tabela zauzeti sav prostor unutar okvira, 
# expand=True znaci da ce se tabela prosiriti ako se prozor poveca
okvir_tabela = tk.LabelFrame(root, text=" Prikaz narudžbi sa izračunatim vrijednostima ", font=("Arial", 10, "bold"), padx=10, pady=5)
okvir_tabela.pack(fill="both", expand=True, padx=20, pady=5)

# definicija kolona tabele, gdje se navode nazivi kolona koje ce se prikazivati, 
# i zatim se kreira Treeview widget koji ce biti tabela, sa tim kolonama, 
# i show="headings" znaci da ce se prikazivati samo zaglavlja kolona, 
# bez defaultne prve kolone koja se koristi za hijerarhiju
kolone = ("id", "dolazak", "trajanje", "prioritet", "kraj", "tat", "wt")
tabela = ttk.Treeview(okvir_tabela, columns=kolone, show="headings")

# postavljanje naziva kolona u tabeli, gdje se koristi metoda heading() 
# da se definise tekst koji ce se prikazivati u zaglavlju svake kolone
tabela.heading("id", text="#Br.Narudzbe")
tabela.heading("dolazak", text="T-DolaskaNarudzbe")
tabela.heading("trajanje", text="T-PripremeNarudzbe")
tabela.heading("prioritet", text="Prioritet")
tabela.heading("kraj", text="T-Kompletiranja")
tabela.heading("tat", text="UkupnoPovratno-T")
tabela.heading("wt", text="T-Cekanja")

# postavljanje sirine i poravnanja za svaku kolonu, 
# gdje se koristi metoda column() da se definise sirina kolone (width=110) i poravnanje teksta 
# (anchor="center") da bude centrirano
# prikazat ce se sve kolone sa istom sirinom od 110 piksela, i tekst ce biti centriran u svakoj celiji tabele, 
# sto ce dati uredan i pregledan izgled tabele
for kol in kolone:
    tabela.column(kol, width=110, anchor="center")

# smjestanje tabele unutar okvira_tabela, 
# fill="both" znaci da ce tabela zauzeti sav prostor unutar okvira
# pack metoda se koristi za organizaciju widgeta u prozoru, 
# i u ovom slucaju tabela ce se prosiriti da popuni sav prostor unutar okvira_tabela, 
# a expand=True znaci da ce se tabela prosiriti ako se prozor poveca
tabela.pack(fill="both", expand=True)

# upravljacki okvir sa dugmadima za pokretanje obrade i ciscenje tabele,
# a zatim labela za prikaz prosjecnog TAT i WT nakon obrade 
okvir_akcije = tk.Frame(root)
okvir_akcije.pack(fill="x", padx=20, pady=10)

btn_obradi = ttk.Button(okvir_akcije, text="POKRENI OBRADU", command=pokreni_algoritam)
btn_obradi.pack(side="left", padx=5)

btn_ocisti = ttk.Button(okvir_akcije, text="Očisti sve", command=ocisti_sve)
btn_ocisti.pack(side="left", padx=5)

lbl_statistika = tk.Label(okvir_akcije, text="Prosječan TAT: 0.00 min  |  Prosječan WT: 0.00 min", font=("Arial", 11, "bold"))
lbl_statistika.pack(side="right", padx=10)

root.mainloop() # pokrece glavnu petlju aplikacije, 
#koja ceka na korisnicke akcije i osvjezava interfejs prema potrebi