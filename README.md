# Progetto di rete per la Compagnia Theta

Progettazione, preventivo e test di sicurezza dell'infrastruttura di rete di un'azienda su due sedi, realizzati dal gruppo **White Russian Hats** (Cybersecurity & Threat Intelligence).

Il progetto comprende la topologia di rete, la segmentazione in VLAN, i dispositivi di sicurezza (firewall, IDS/IPS, DMZ), un preventivo dettagliato e tre strumenti di test scritti in Python. Include anche una **proposta alternativa** che collega le due sedi in un unico campus con fibra ottica.

## Contesto

La Compagnia Theta ha due sedi a 250 metri di distanza, la seconda nella zona PIP di Cavenago di Brianza:

| Sede | Piani | Postazioni |
|---|---|---|
| Edificio 1 (principale) | 6 | 120 (20 per piano) |
| Edificio 2 | 3 | 90 (30 per piano) |

## Obiettivi

- Topologia di rete scalabile e sicura
- Segmentazione in VLAN per piano
- Firewall e sistemi IDS/IPS
- Servizi web esposti in modo controllato in DMZ
- Test di sicurezza automatici
- Stessi standard di sicurezza su entrambe le sedi
- Raccomandazioni basate sui risultati dei test

## Architettura (progetto base)

Ogni sede ha una rete autonoma con il proprio perimetro di sicurezza.

**VLAN**

- Edificio 1: VLAN 10-15 (un piano per VLAN), VLAN 20 per il NAS, VLAN 30 per la DMZ
- Edificio 2: VLAN 10-12 (un piano per VLAN), VLAN 20 per il NAS, VLAN 30 per la DMZ
- Subnet /26 (255.255.255.192) per ogni piano, 64 indirizzi

**Switch e routing**

- Collegamenti trunk tra gli switch di piano, porte access verso i client
- Routing inter-VLAN sullo switch multilayer, con interfacce SVI come gateway
- Sottoreti /30 tra i dispositivi di sicurezza: Multilayer-Firewall `192.168.100.0/30`, Firewall-IPS `192.168.101.0/30`, IPS-Router `192.168.102.0/30`

## Sicurezza

- **Firewall perimetrale** con NAT: consente solo HTTP/HTTPS verso la DMZ e blocca il traffico in ingresso non autorizzato
- **IPS-1** tra router e firewall, **IDS-2** sulla DMZ, **IDS-3** sul core switch
- **DMZ** con web server raggiungibile dall'esterno solo sulla porta 80
- **NAS** in una VLAN dedicata, con utenti e permessi differenziati

## Preventivo

Importi in euro, IVA esclusa, con 1 anno di rinnovi incluso.

| Soluzione | Importo |
|---|---|
| Edificio 1 | 292.402 |
| Edificio 2 | 239.683 |
| **Progetto base (totale)** | **532.085** |
| **Alternativa campus** | **482.405** |

Tempi stimati per il progetto base: circa 6-7 settimane più collaudo (progettazione, cablaggio, configurazione, IDS/IPS in sola rivelazione e tuning, poi attivazione del blocco).

## Alternativa campus

Le due sedi sono collegate con una fibra ottica interrata di 250 metri in un unico campus a **core collassato**.

- Core collassato nell'Edificio 1 (2 switch Catalyst 9300 in stack) e aggregazione nell'Edificio 2
- 2 link da 10 Gbit/s in fibra monomodale su 2 cavidotti, uno di scorta
- Un solo perimetro di sicurezza: 1 firewall, 1 IPS, 2 IDS e un solo SOC esterno
- VLAN rinumerate: 10-15 per l'Edificio 1, 16-18 per l'Edificio 2, 20 (NAS) e 30 (DMZ) condivise
- Costo di circa 49.680 euro in meno rispetto al progetto base (circa il 9%), compreso il collegamento in fibra da 41.000 euro
- Tempi stimati: 8-10 settimane

Le voci di scavo, moduli ottici e moduli di rete sono **stime** da confermare con sopralluogo e preventivi dei fornitori.

## Strumenti di test in Python

Tre script sviluppati per verificare i servizi esposti:

| Script | Funzione |
|---|---|
| `port_scanner_test.py` | Scansione delle porte comuni tramite socket TCP |
| `http_verbs.py` | Elenco dei verbi HTTP abilitati su un URL |
| `Socket_sniffer.py` | Cattura e analisi del traffico di rete in tempo reale |

**Uso**

```bash
python3 port_scanner_test.py      # chiede l'indirizzo IP da scansionare
python3 http_verbs.py             # chiede l'URL da testare
sudo python3 Socket_sniffer.py    # richiede privilegi di amministratore, Ctrl+C per fermare
```

> **Uso responsabile.** Gli script vanno usati solo su sistemi propri o con autorizzazione esplicita. Nel progetto sono stati eseguiti in un laboratorio virtuale.

## Risultati dei test

- **Porte senza firewall:** risultavano aperte 22 (SSH), 53 (DNS), 80 (HTTP), 445 (SMB) e 3306 (MySQL)
- **Porte con firewall attivo:** resta aperta solo la porta 80, le altre sono filtrate
- **Verbi HTTP:** tutti i verbi testati risultano abilitati, compresi PUT, DELETE e TRACE
- **Sniffer:** il traffico di rete è visibile in tempo reale, da qui la necessità di HTTPS

## Raccomandazioni

**Priorità alta**

- **MySQL (3306):** accesso solo da localhost o da IP autorizzati, nessun accesso remoto per root
- **SMB (445):** disabilitare SMBv1, escludere condivisioni anonime, spegnere il servizio se non serve
- **HTTP senza HTTPS:** certificato TLS, reindirizzamento da 80 a 443, HSTS, TLS 1.0/1.1 disabilitati

**Priorità media**

- **SSH (22):** autenticazione a chiave, `PermitRootLogin no`, accesso limitato agli IP di amministrazione, fail2ban
- **DNS (53):** disattivare il servizio se non serve, disabilitare la ricorsione per gli esterni e i trasferimenti di zona

## Team

| Nome | Ruolo |
|---|---|
| Francesco Valentini | Network Architect e Lead Network Admin |
| Samuele Colasuonno | Network Admin e Security Specialist |
| Federico Lattanzi | Network Admin e Security Specialist |
| Daniele Perri | Python Developer (Security Testing) |
| Simone Varriale | Hardware e Cost Analyst |
| Isabel Carosiello | Project Manager e Report Lead |
