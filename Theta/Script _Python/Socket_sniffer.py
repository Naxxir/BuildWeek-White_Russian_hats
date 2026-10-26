from scapy.all import sniff, IP, TCP, UDP


def analizza_pacchetto(pacchetto):
    if IP in pacchetto:
        sorgente = pacchetto[IP].src
        destinazione = pacchetto[IP].dst
        protocollo = pacchetto[IP].proto

        print("-" * 60)
        print(f"IP sorgente:      {sorgente}")
        print(f"IP destinazione:  {destinazione}")

        if TCP in pacchetto:
            print("Protocollo:       TCP")
            print(f"Porta sorgente:   {pacchetto[TCP].sport}")
            print(f"Porta destinazione: {pacchetto[TCP].dport}")

        elif UDP in pacchetto:
            print("Protocollo:       UDP")
            print(f"Porta sorgente:   {pacchetto[UDP].sport}")
            print(f"Porta destinazione: {pacchetto[UDP].dport}")

        else:
            print(f"Protocollo IP:    {protocollo}")

print("Cattura del traffico avviata...")
print("Premi CTRL+C per interrompere.")

try:
    sniff(
        filter="tcp port 80 or tcp port 443",
            prn=lambda p: p.summary(),
            store=False
    )
except KeyboardInterrupt:
    print("\nCattura terminata.")