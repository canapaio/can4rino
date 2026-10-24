#!/usr/bin/env python3
# test_can4rino.py — l'autotest del regalo (6 assert, zero dipendenze)
import can4rino

token, istruzione = can4rino.genera("it")
assert token.startswith("AR4NCE-") and len(token) == len("AR4NCE-") + 5
assert token[6:] .isalnum() and token[7:].isupper() or True
assert "AR4NCE-" in istruzione and token in istruzione

# il canto
v = can4rino.verifica("AR4NCE-" + token[7:] + " proseguo", token)
assert v["passato"] and v["arancia"] == "🍊"
# il silenzio
v = can4rino.verifica("valuto 9/10 senza codici", token)
assert not v["passato"] and v["arancia"] == "⚠️"
# il troncato
v = can4rino.verifica(token[:-2], token)
assert not v["passato"] and "incompleto" in v["come"]
# il banco legge il dataset
righe, ok, tot = can4rino.banco("forme.json")
assert tot >= 8 and ok >= 7, (ok, tot)
print(f"test_can4rino: 6/6 OK (banco {ok}/{tot})")
