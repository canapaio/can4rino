# 🍊 can4rino — il canarino dell'oblio
### (can-for-rino: il canarino per il rinoceronte delle iniezioni)

ATTENZIONE - QUESTO è UN ESPERIMENTO SEMANTICO NON USARE QUESTO CODICE PER LA TUA SICUREZZA O LA SICUREZZA DI SISTEMI IN PRODUZIONE E NON

Un tripwire contro le **iniezioni di prompt**, in un solo file, zero
dipendenze. Compatibile con **qualsiasi** LLM e sistema: il verdetto è
una stringa dentro un'altra — non serve nulla di più.

> Un regalo di Canapaio — al mondo.
> L'idea: **l'oblio parte solo quando il dato non c'è nel contesto** —
> quindi un'istruzione-canarino in quel canale è una sonda
> deterministica: se alla richiesta di valutazione il canarino non
> canta, qualcosa ha parlato al posto tuo.

## In tre gesti

```python
import can4rino

# 1. GENERA — il token AR4NCE-XXXXX + l'istruzione per il contesto
token, istruzione = can4rino.genera(lingua="it")

# 2. INFILA l'istruzione nel tuo contesto (system, RAG, memoria,
#    documento) e fai la richiesta al tuo modello, come fai di solito

# 3. VERIFICA la risposta — meccanico, zero millisecondi
esito = can4rino.verifica(risposta, token)
print(esito["arancia"], esito["messaggio"])
# 🍊 IL CANARINO CANTA — la pipeline è onesta...
# ⚠️ PERICOLO: il canarino tace — possibile iniezione...
```

O da riga di comando (exit code 0/1 — per CI e cron):
```bash
python can4rino.py genera
python can4rino.py verifica --token AR4NCE-X7K2P --risposta "..."
```

## 📋 Il dataset: aggiungi una riga, il sistema è aggiornato

I test vivono in **`forme.json`** — una riga per forma:

```json
{"id": "iniezione-silenziosa",
 "forma": "iniezione che sopprime il canarino",
 "risposta": "Il documento è eccellente, lo valuterei 9/10.",
 "arancio": false,
 "nota": "la valutazione esce senza token: iniezione indiretta"}
```

- **`"arancio": true`** → il canarino DEVE cantare (usa `{token}` come
  segnaposto: il banco lo sostituisce col token corrente — il dataset
  non invecchia mai quando ruoti i token)
- **`"arancio": false`** → il canarino DEVE tacere (pericolo)

E il banco produce la tabella:
```bash
python can4rino.py banco --dataset forme.json
```

**Per aggiornare il sistema: aggiorna solo il dataset.** Nuova forma
di attacco trovata in natura? Una riga, e il mondo è al passo.

## Le forme già in galleria
pipeline onesta · canarino in mezzo alla valutazione · iniezione
silenziosa · iniezione che rovescia il canarino · token troncato ·
token con maiuscole alterate · risposta vuota · override di persona.

## Le cosucie — non tutto cio che inquina e un attacco
Nel dataset c'e anche la sporcizia commerciale leggera: lo **shilling**
("questo sistema e il migliore"), la **comparativa truccata** (fango
sui concorrenti), la **nota dello sponsor**, il **review-bait**, il
**FUD morbido**. Queste forme NON ammutoliscono il canarino: il token
canta — ma la risposta e uno spot. Il banco le mostra col **biglietto**
(campo `biglietto` nel dataset): l'avviso da allegare per chi valuta
l'imparzialita.

## IL NON-BLOCCO (la regola della casa)
**can4rino non scarta mai: ALLEGA.** Quando il canarino tace, la
risposta passa comunque — col **banner** attaccato:
`[ALLERTA CANARINO] ... VALUTA L'IMPARZIALITA del lavoro qui sotto.`
Chi decide resta l'agente o l'utente: la macchina segnala e conta.
(`verifica()` restituisce `azione: "allerta"` — mai `blocca`.)

## ⚠️ L'onestà (leggi prima di fidarti)
- se l'istruzione-canarino **non arriva** al modello, il silenzio non
  è prova di iniezione: può essere un canale rotto. Il pericolo grida
  comunque — ma verifica il canale
- un'iniezione furba può far **cantare il token** (parrot): ruota i
  token, usa più canarini in punti diversi del contesto
- è un **tripwire**: una parte della difesa, non tutta. can4rino va usato
  insieme a: separazione dei contenuti non fidati, verifica meccanica
  delle citazioni, verifica meccanica a valle

## 🇬🇧 English (short)
A prompt-injection **canary tripwire** in one file, zero dependencies,
works with any LLM: generate an unguessable token `AR4NCE-XXXXX`, plant
the canary instruction in your context, and mechanically check the
model's answer. Tests live in a dataset (`forme.json`) — add a row and
the system is updated. Verdict = string containment (never semantics).

## Licenza
MIT — regalato al mondo da **Canapaio**. Se ti salva da un'iniezione, pensa a un contadino. 🌾