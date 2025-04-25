import csv
from datetime import datetime, timedelta

VILOTID_MINIMUM = timedelta(hours=11)

def läs_arbetsdagar_csv(filnamn):
    """
    Läser arbetsdagar från CSV-fil.
    Format: datum,start_tid,sluttid
    Exempelrad: 2025-04-09,08:00,16:00
    """
    arbetsdagar = []
    with open(filnamn, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # hoppa över header
        for rad in reader:
            datum = rad[0]
            start_tid = rad[1]
            sluttid = rad[2]
            start_dt = datetime.strptime(f"{datum} {start_tid}", "%Y-%m-%d %H:%M")
            slutt_dt = datetime.strptime(f"{datum} {sluttid}", "%Y-%m-%d %H:%M")
            if slutt_dt < start_dt:
                slutt_dt += timedelta(days=1)  # för nattpass
            arbetsdagar.append((start_dt, slutt_dt))
    return arbetsdagar

def kontrollera_vilotid(arbetsdagar):
    for i in range(1, len(arbetsdagar)):
        _, slut_förra = arbetsdagar[i - 1]
        start_nästa, _ = arbetsdagar[i]
        vilotid = start_nästa - slut_förra
        print(f"\n🕒 Kontroll mellan pass {i} och {i+1}:")
        print(f"Slut föregående: {slut_förra}, Start nästa: {start_nästa}")
        if vilotid >= VILOTID_MINIMUM:
            print(f"✅ OK - Vilotid: {vilotid}")
        else:
            print(f"⚠️  Varning - Endast {vilotid} vilotid! (Krav: minst 11 timmar)")

if __name__ == "__main__":
    filnamn = "arbetsdagar.csv"
    arbetsdagar = läs_arbetsdagar_csv(filnamn)
    kontrollera_vilotid(sorted(arbetsdagar))
