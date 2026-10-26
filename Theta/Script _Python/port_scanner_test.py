import socket

# Dizionario: porta -> (servizio, descrizione)
SERVIZI = {
    22:   ("SSH",        "Accesso remoto sicuro da riga di comando e trasferimento file (SFTP/SCP)"),
    53:   ("DNS",        "Risoluzione dei nomi di dominio in indirizzi IP"),
    80:   ("HTTP",       "Navigazione web non cifrata"),
    443:  ("HTTPS",      "Navigazione web cifrata con TLS/SSL"),
    445:  ("SMB",        "Condivisione di file e stampanti in rete (Windows)"),
    3306: ("MySQL",      "Database MySQL / MariaDB"),
    3389: ("RDP",        "Desktop remoto di Windows"),
    8080: ("HTTP-Alt",   "Server web alternativo, proxy o pannelli di amministrazione"),
}

TIMEOUT = 1

# Richiesta dell'indirizzo IP all'utente
ip = input("Inserisci l'indirizzo IP del dispositivo da scansionare: ")

print(f"\nScansione del dispositivo: {ip}")
print("=" * 70)

for porta, (servizio, descrizione) in SERVIZI.items():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)

    try:
        risultato = sock.connect_ex((ip, porta))

        if risultato == 0:
            stato = "APERTA"
        else:
            stato = "NON ACCESSIBILE"

        print(f"PORTA {porta:5} [TCP] - {stato}")
        print(f"    Servizio:    {servizio}")
        print(f"    Descrizione: {descrizione}")
        print("-" * 70)

    except socket.error as errore:
        print(f"PORTA {porta:5} [TCP] - ERRORE: {errore}")
        print(f"    Servizio:    {servizio}")
        print("-" * 70)

    finally:
        sock.close()

print("=" * 70)
print("Scansione completata.")