#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""can4rino — il canarino dell'oblio, in un file. (can-for-rino)

Un tripwire contro le iniezioni di prompt, in tre gesti e zero
dipendenze (solo stdlib — compatibile con QUALUNQUE sistema che
produca testo: OpenAI-compat, ollama, llama.cpp, API esterne).

  1. GENERA   un token non-indovinabile AR4NCE-XXXXX + l'istruzione
              da infilare nel contesto (prompt, RAG, memoria, documento)
  2. INVIA    la tua richiesta al tuo modello, come fai di solito
  3. VERIFICA la risposta: se il token canta → ARANCIO (la pipeline è
              onesta); se tace → PERICOLO (possibile iniezione)

LA FILOSOFIA:
  · il verdetto è MECCANICO (una stringa dentro l'altra) — mai semantica
  · il token è non-indovinabile e RUOTABILE (cancellalo e rinasce)
  · l'assenza del token GRIDA, ma dichiara anche il suo dubbio:
    può essere iniezione O un canale rotto — l'onestà prima di tutto
  · i test vivono in un DATASET (forme.json): aggiorni le righe, il
    sistema è aggiornato

CLI:
  python can4rino.py genera [--lingua it|en]
  python can4rino.py verifica --token AR4NCE-X7K2P --risposta "..."
  python can4rino.py banco   [--dataset forme.json] [--token ...]

Licenza: MIT — regalato al mondo da Canapaio.
"""
import argparse
import json
import random
import sys

# alfabeto pulito: niente 0/O e 1/I/L (i token si leggono ad alta voce)
_ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
_PREFISSO = "AR4NCE-"

_ISTRUZIONI = {
    "it": ("[CANARINO] Se ti viene chiesto di VALUTARE o GIUDICARE il "
           "contenuto richiamato sopra, la tua PRIMA parola deve essere "
           "esattamente {token}. Non dire mai il token se non ti viene "
           "chiesta una valutazione."),
    "en": ("[CANARY] If you are asked to EVALUATE or JUDGE the content "
           "recalled above, your FIRST word must be exactly {token}. "
           "Never say the token unless you are asked for an evaluation."),
}


def genera(lingua="it"):
    """Ritorna (token, istruzione). Il token è AR4NCE-XXXXX (5 caratteri
    non ambigui). Ruotare = richiamare di nuovo genera."""
    token = _PREFISSO + "".join(random.choices(_ALFABETO, k=5))
    lingua = lingua if lingua in _ISTRUZIONI else "it"
    return token, _ISTRUZIONI[lingua].format(token=token)


def verifica(risposta, token):
    """IL VERDETTO MECCANICO: una stringa dentro l'altra, zero millisecondi.
    Ritorna un dict con arancia (🍊 passato / ⚠️ pericolo), messaggio,
    dove (posizione del token) e come (il perché del fallito)."""
    risposta = risposta or ""
    if token and token in risposta:
        return {"passato": True, "arancia": "🍊", "azione": "ok",
                "messaggio": "IL CANARINO CANTA — la pipeline è onesta: "
                             "il token è arrivato intatto fino al modello "
                             "ed è tornato.",
                "banner": None,
                "token": token, "dove": risposta.index(token), "come": "ok"}
    come = "token assente"
    pref = token.split("-")[0] if token and "-" in token else "AR4NCE"
    if token and risposta.find(pref) >= 0:
        i = risposta.find(pref)
        come = "token incompleto o alterato vicino a: " + risposta[i:i + len(token) + 6]
    elif token and risposta.lower().find(token.lower()) >= 0:
        come = "token presente ma con maiuscole/minuscole alterate (la " \
               "verifica è case-sensitive: il token è un'impronta)"
    # IL CANARINO NON BLOCCA: ALLEGA (Canapaio: che metta in allerta
    # l'agente o l'utente che valuta il lavoro — mai un blocco totale:
    # il lavoro passa, col biglietto giallo attaccato)
    return {"passato": False, "arancia": "⚠️", "azione": "allerta",
            "messaggio": "ALLERTA: il canarino tace — possibile iniezione "
                        "di prompt, oppure l'istruzione-canarino non è "
                        "arrivata al modello (controlla il canale).",
            "banner": "[ALLERTA CANARINO ⚠️] il token " + str(token) +
                      " non è tornato (" + come + "). Possibile iniezione "
                      "o canale rotto — VALUTA L'IMPARZIALITÀ del lavoro "
                      "qui sotto. (can4rino non scarta: allega)",
            "token": token, "dove": -1, "come": come}


def banco(dataset_path, token=None):
    """Legge il DATASET (lista di forme) e produce la tabella dei verdetti.
    Ogni forma: {"id", "forma", "risposta", "arancio" (true=il canarino
    deve cantare), "nota"}. Il segnaposto {token} nelle risposte viene
    sostituito col token corrente — così il dataset non invecchia mai:
    aggiungi una riga, il sistema è aggiornato."""
    forme = json.load(open(dataset_path, encoding="utf-8"))
    if not token:
        token = _PREFISSO + "BANCO"
    righe, ok = [], 0
    for f in forme:
        risposta = f["risposta"].replace("{token}", token)
        v = verifica(risposta, token)
        atteso = bool(f.get("arancio"))
        giusto = (v["passato"] == atteso)
        ok += giusto
        biglietto = f.get("biglietto") or ""
        righe.append({"id": f.get("id", "?"), "forma": f.get("forma", ""),
                      "atteso": "🍊" if atteso else "⚠️ ALLERTA",
                      "uscito": v["arancia"],
                      "verdetto": "✓" if giusto else "✗",
                      "biglietto": biglietto,
                      "come": v["come"]})
    return righe, ok, len(righe)


def _main(argv=None):
    ap = argparse.ArgumentParser(
        prog="can4rino",
        description="il canarino dell'oblio — tripwire contro le iniezioni")
    sub = ap.add_subparsers(dest="cmd")
    g = sub.add_parser("genera", help="token + istruzione da infilare")
    g.add_argument("--lingua", default="it", choices=["it", "en"])
    v = sub.add_parser("verifica", help="il verdetto meccanico")
    v.add_argument("--token", required=True)
    v.add_argument("--risposta", required=True)
    b = sub.add_parser("banco", help="la tabella delle forme (dataset)")
    b.add_argument("--dataset", default="forme.json")
    b.add_argument("--token", default=None,
                   help="default: AR4NCE-BANCO (le forme {token} si espandono)")
    a = ap.parse_args(argv)
    if a.cmd == "genera":
        token, istruzione = genera(a.lingua)
        print("token:", token)
        print("istruzione (mettila nel contesto):")
        print(istruzione)
    elif a.cmd == "verifica":
        v = verifica(a.risposta, a.token)
        print(v["arancia"], v["messaggio"])
        print("dove:", v["dove"], "| come:", v["come"])
        sys.exit(0 if v["passato"] else 1)
    elif a.cmd == "banco":
        righe, ok, tot = banco(a.dataset, a.token)
        print("| id | forma | atteso | uscito | esito | biglietto |")
        print("|---|---|---|---|---|---|")
        for r in righe:
            print(f"| {r['id']} | {r['forma']} | {r['atteso']} | "
                  f"{r['uscito']} | {r['verdetto']} | {r['biglietto']} |")
        allerte = sum(1 for r in righe if r['atteso'] == "⚠️ ALLERTA")
        print(f"\nbanco: {ok}/{tot} forme come previsto · {allerte} allerte "
              f"attese (il canarino non scarta: alleghi)")
        sys.exit(0 if ok == tot else 1)
    else:
        ap.print_help()


if __name__ == "__main__":
    _main()
