#!/usr/bin/env python3
"""
http_methods_scanner.py

Tool per l'enumerazione dei metodi HTTP abilitati su un determinato path
di un web server.

Uso:
    python3 http_methods_scanner.py -u http://192.168.50.2/phpMyAdmin/
    python3 http_methods_scanner.py -u http://192.168.50.2/phpMyAdmin/ --active
    python3 http_methods_scanner.py -u http://192.168.50.2/phpMyAdmin/ --active --insecure

Funzionamento:
    1. Modalità "passiva" (default): invia una richiesta OPTIONS al path
       indicato e legge l'header di risposta "Allow" (o "Public"), che
       secondo RFC 7231 dichiara i metodi supportati dalla risorsa.
    2. Modalità "attiva" (--active): oltre a OPTIONS, prova singolarmente
       un set di verbi HTTP comuni (GET, POST, PUT, DELETE, PATCH, TRACE,
       CONNECT, HEAD, ecc.) e classifica ciascuno come "abilitato" o
       "negato" in base al codice di stato HTTP ricevuto. Questo serve a
       verificare empiricamente quanto dichiarato da OPTIONS, dato che
       alcuni server non espongono correttamente l'header Allow o
       applicano filtri diversi a seconda del verbo.

Nota etica/legale:
    Usare questo strumento esclusivamente su sistemi per cui si ha
    autorizzazione esplicita (es. ambiente di laboratorio/VM personale),
    come previsto dalla traccia del progetto universitario.
"""

import argparse
import sys
from urllib.parse import urlparse

import requests
from requests.exceptions import RequestException

# Disabilita i warning per certificati self-signed quando si usa --insecure
import urllib3

# Set di verbi HTTP da testare in modalità attiva.
# Si includono sia i metodi "standard" sia alcuni meno comuni ma rilevanti
# dal punto di vista della sicurezza (es. TRACE per XST, PUT/DELETE per
# eventuale upload/remozione file non autorizzata).
HTTP_METHODS = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
    "PATCH",
    "TRACE",
    "CONNECT",
]

# Codici di stato che, in modalità attiva, consideriamo indicativi di un
# metodo "abilitato" (la richiesta è stata accettata/elaborata dal server
# per quella risorsa, anche se poi risponde con un errore applicativo).
# Si escludono i codici che indicano esplicitamente che il metodo non è
# permesso o non è supportato.
METHOD_NOT_ALLOWED_CODES = {405, 501}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Enumera i metodi HTTP abilitati su un path di un web server."
    )
    parser.add_argument(
        "-u", "--url",
        required=True,
        help="URL completo del path da analizzare (es. http://192.168.50.2/phpMyAdmin/)"
    )
    parser.add_argument(
        "--active",
        action="store_true",
        help="Abilita il test attivo: prova singolarmente ogni metodo HTTP noto."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout (in secondi) per ogni richiesta HTTP (default: 5)."
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disabilita la verifica del certificato TLS (per ambienti di test con cert self-signed)."
    )
    return parser.parse_args()


def validate_url(url: str) -> str:
    """Verifica che l'URL sia ben formato e restituisce lo schema normalizzato."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        print(f"[!] Schema URL non valido: '{parsed.scheme}'. Usa http:// o https://")
        sys.exit(1)
    if not parsed.netloc:
        print("[!] URL non valido: manca l'host.")
        sys.exit(1)
    return url


def test_options(url: str, timeout: float, verify: bool) -> list:
    """
    Invia una richiesta OPTIONS al path indicato e restituisce la lista
    dei metodi dichiarati nell'header 'Allow' (o 'Public' come fallback).
    """
    try:
        resp = requests.options(url, timeout=timeout, verify=verify)
    except RequestException as e:
        print(f"[!] Errore durante la richiesta OPTIONS: {e}")
        return []

    allow_header = resp.headers.get("Allow") or resp.headers.get("Public")

    print(f"[*] Richiesta OPTIONS -> status: {resp.status_code}")
    if allow_header:
        methods = [m.strip().upper() for m in allow_header.split(",") if m.strip()]
        print(f"[*] Header 'Allow'/'Public' trovato: {allow_header}")
        return methods
    else:
        print("[*] Nessun header 'Allow'/'Public' presente nella risposta OPTIONS.")
        return []


def test_active_methods(url: str, timeout: float, verify: bool) -> dict:
    """
    Prova singolarmente ciascun metodo HTTP noto sul path indicato e
    restituisce un dizionario {metodo: (status_code, abilitato_bool)}.
    """
    results = {}
    session = requests.Session()

    for method in HTTP_METHODS:
        try:
            resp = session.request(method, url, timeout=timeout, verify=verify, allow_redirects=False)
            status = resp.status_code
            enabled = status not in METHOD_NOT_ALLOWED_CODES
            results[method] = (status, enabled)
        except RequestException as e:
            results[method] = (None, False)
            print(f"[!] Errore testando il metodo {method}: {e}")

    return results


def print_active_results(results: dict):
    print("\n[*] Risultati test attivo (verbo per verbo):")
    print(f"{'Metodo':<10} {'Status':<10} {'Esito'}")
    print("-" * 35)
    for method, (status, enabled) in results.items():
        status_str = str(status) if status is not None else "ERRORE"
        esito = "ABILITATO" if enabled else "NEGATO"
        print(f"{method:<10} {status_str:<10} {esito}")


def main():
    args = parse_args()
    url = validate_url(args.url)
    verify_tls = not args.insecure

    if args.insecure:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print(f"[*] Target: {url}")
    print("[*] Fase 1: richiesta OPTIONS (metodo passivo)\n")

    allowed_from_options = test_options(url, args.timeout, verify_tls)

    if allowed_from_options:
        print("\n[+] Metodi dichiarati dal server (header Allow/Public):")
        for m in allowed_from_options:
            print(f"    - {m}")
    else:
        print("\n[-] Nessun metodo dichiarato esplicitamente via OPTIONS.")

    if args.active:
        print("\n[*] Fase 2: test attivo di ciascun metodo HTTP\n")
        active_results = test_active_methods(url, args.timeout, verify_tls)
        print_active_results(active_results)

        enabled_methods = [m for m, (s, e) in active_results.items() if e]
        print("\n[+] Metodi risultati abilitati (test attivo):")
        for m in enabled_methods:
            print(f"    - {m}")

        # Confronto tra quanto dichiarato via OPTIONS e quanto rilevato attivamente
        if allowed_from_options:
            declared = set(allowed_from_options)
            detected = set(enabled_methods)
            mismatch = detected.symmetric_difference(declared)
            if mismatch:
                print("\n[!] Discrepanza tra metodi dichiarati (OPTIONS) e rilevati (test attivo):")
                for m in sorted(mismatch):
                    in_options = "sì" if m in declared else "no"
                    in_active = "sì" if m in detected else "no"
                    print(f"    - {m}: dichiarato={in_options}, rilevato={in_active}")
            else:
                print("\n[*] Nessuna discrepanza tra OPTIONS e test attivo.")


if __name__ == "__main__":
    main()
