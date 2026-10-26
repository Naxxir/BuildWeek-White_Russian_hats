import socket

# Richiesta dell'indirizzo IP all'utente
ip = input("Inserisci l'indirizzo IP del dispositivo da scansionare: ")

# Porte TCP da verificare
porte = [22, 53, 80, 443, 445, 3306, 3389, 8080]

TIMEOUT = 1

print(f"\nScansione del dispositivo: {ip}")
print("=" * 45)

for porta in porte:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)

    try:
        risultato = sock.connect_ex((ip, porta))

        if risultato == 0:
            print(f"PORTA {porta:5} - APERTA")
        else:
            print(f"PORTA {porta:5} - NON ACCESSIBILE")

    except socket.error as errore:
        print(f"PORTA {porta:5} - ERRORE: {errore}")

    finally:
        sock.close()

print("=" * 45)
print("Scansione completata.")