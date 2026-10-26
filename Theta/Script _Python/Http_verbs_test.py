import requests
from requests.exceptions import RequestException

# Sostituisci con l'indirizzo del tuo web server di test.
URL = input("Inserisci l'Url da testare: ")


# Usa un endpoint di test dedicato.
# POST e PUT creano o modificano dati; DELETE può eliminarli.
payload = {
    "nome": "Test rete aziendale",
    "stato": "verifica"
}

tests = [
    ("GET", None),
    ("POST", payload),
    ("PUT", payload),
    ("DELETE", None),
]

for method, data in tests:
    try:
        response = requests.request(
            method,
            URL,
            json=data,
            timeout=5
        )

        print(f"\nMetodo: {method}")
        print(f"URL: {URL}")
        print(f"Codice HTTP: {response.status_code}")
        print(f"Risposta: {response.text[:300]}")

        if 200 <= response.status_code < 300:
            print("Esito: richiesta completata con successo")
        elif response.status_code == 404:
            print("Esito: endpoint non trovato")
        elif response.status_code == 405:
            print("Esito: metodo HTTP non consentito")
        elif response.status_code == 401:
            print("Esito: autenticazione richiesta")
        elif response.status_code == 403:
            print("Esito: accesso vietato")
        else:
            print("Esito: verificare la risposta del server")

    except RequestException as error:
        print(f"\nMetodo: {method}")
        print(f"Errore di connessione: {error}")