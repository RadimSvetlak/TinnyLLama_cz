# -*- coding: utf-8 -*-
import json
import random
from tab_prislovce import prislovce_kone
from tab_nouns import nouns
from tab_slovesa import verb_conjugations

rows = []


def random_verb_present_3sg():
    lemma = random.choice(list(verb_conjugations.keys()))
    form = verb_conjugations[lemma]["přítomný"]["j.č."][3]
    return form


# Pomocné funkce
def parse_degrees(record):
    parts = [p.strip() for p in record.get("stupně", "").split(",")]
    base = parts[0] if len(parts) > 0 else ""
    comp = parts[1] if len(parts) > 1 else ""
    sup = parts[2] if len(parts) > 2 else ""
    return base, comp, sup

def list_all_noun_lemmas():
    lemmas = []
    for rod in nouns:
        lemmas.extend(list(nouns[rod].keys()))
    return lemmas

def random_noun_lemma(exclude=None):
    candidates = list_all_noun_lemmas()
    if exclude:
        candidates = [c for c in candidates if c not in exclude]
    return random.choice(candidates) if candidates else "kůň"

for adj, data in prislovce_kone.items():
    base, comp, sup = parse_degrees(data)
    if not (base and comp and sup):
        continue  # přeskoč nekompletní záznamy

    synonyma = data.get("synonyma", [])
    antonyma = data.get("antonyma", [])
    typ = data.get("typ", "")
    otazka = data.get("otázka", "")

    # 1) 2. stupeň
    rows.append({
        "prompt": f"napiš 2. stupeň příslovce: '{base}'",
        "completion": comp
    })

    # 2) 3. stupeň
    rows.append({
        "prompt": f"napiš 3. stupeň příslovce: '{base}'",
        "completion": sup
    })

    # 3) převod na přídavné jméno
    rows.append({
        "prompt": f"převeď příslovce: '{base}' na přídavné jméno",
        "completion": adj
    })

    # 4) synonymum (1. stupeň)
    if synonyma:
        rows.append({
            "prompt": f"napiš synonymum: '{base}'",
            "completion": random.choice(synonyma)
        })

    # 5) antonymum (1. stupeň)
    if antonyma:
        rows.append({
            "prompt": f"napiš antonymum: '{base}'",
            "completion": random.choice(antonyma)
        })

    # 6) typická otázka
    rows.append({
        "prompt": f"typická otázka pro: '{base}'",
        "completion": otazka
    })

    # 7) druh příslovce
    rows.append({
        "prompt": f"urči druh příslovce: '{base}'",
        "completion": typ
    })

    # 8) výběr: A/B/C = příslovce (správně), přídavné jméno, podstatné jméno
    noun_lemma = random_noun_lemma(exclude={base, adj})
    options = [base, adj, noun_lemma]
    random.shuffle(options)
    rows.append({
        "prompt": f"vyber příslovce: A '{options[0]}', B '{options[1]}', C '{options[2]}'",
        "completion": base
    })

    # 9) „stupňuj příslovce“
    rows.append({
        "prompt": f"stupňuj příslovce: '{base}'",
        "completion": f"{base}, {comp}, {sup}"
    })

    # 10) „uveď vyšší stupeň příslovce“
    rows.append({
        "prompt": f"uveď vyšší stupeň příslovce: '{base}'",
        "completion": comp
    })

    # 11) „nahraď synonymem v nižším stupni“
    # Prompt musí obsahovat vyšší stupeň (2. nebo 3.), completion je synonymum v 1. stupni.
    if synonyma:
        higher_form = random.choice([comp, sup])
        rows.append({
            "prompt": f"nahraď příslovce '{higher_form}' synonymem v nižším stupni",
            "completion": random.choice(synonyma)
        })

    # 12) nahraď příslovce '<sloveso> <2 stupeň>' antonymem
    if antonyma:
        verb_form = random_verb_present_3sg()
        rows.append({
            "prompt": f"nahraď příslovce '{verb_form} {comp}' antonymem",
            "completion": f"{verb_form} {random.choice(antonyma)}"
        })

    # 13) doplň příslovce k slovesu
    rows.append({
        "prompt": f"doplň příslovce do věty: On ___ {random_verb_present_3sg()}",
        "completion": base
    })

    # 14) nahraď příslovce u slovesa synonymem
    if synonyma:
        verb_form = random_verb_present_3sg()
        sentence = f"On {verb_form} {base}"
        rows.append({
            "prompt": f"nahraď příslovce ve větě synonymem: {sentence}",
            "completion": sentence.replace(base, random.choice(synonyma))
        })

    # 15) nahraď příslovce u slovesa antonymem
    if antonyma:
        verb_form = random_verb_present_3sg()
        sentence = f"On {verb_form} {base}"
        rows.append({
            "prompt": f"nahraď příslovce ve větě antonymem: {sentence}",
            "completion": sentence.replace(base, random.choice(antonyma))
        })


# ====== Uložení do JSONL ======
output_file = "training_prislovce_tasks.jsonl"
with open(output_file, "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"✅ Hotovo: {len(rows)} úloh uloženo do {output_file}")