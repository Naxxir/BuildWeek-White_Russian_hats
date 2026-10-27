import requests

url = input("Inserisci l'URL target: ")

metodi = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD", "TRACE"]

for metodo in metodi:
    try:
        risposta = requests.request(
            metodo,
            url,
            timeout=5,
            allow_redirects=False
        )

        if risposta.status_code not in [405, 501]:
            print(f"{metodo}: potenzialmente abilitato ({risposta.status_code})")
        else:
            print(f"{metodo}: non supportato ({risposta.status_code})")

    except requests.RequestException:
        print(f"{metodo}: errore nella richiesta")