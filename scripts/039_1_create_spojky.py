import json
import random

spojky = {
    "slucovaci": ["a", "i", "ani", "nebo"],
    "odporovaci": ["ale", "avšak", "však", "nýbrž", "jenže"],
    "vylucovaci": ["nebo", "anebo"],
    "podradici": ["že", "protože", "jestliže", "když", "aby", "ačkoliv", "pokud", "jakmile"]
}

# Jednoduché věty pro generování
casti_vet = [
    ("Přišel", "odešel"),
    ("Bylo hezky", "šli jsme ven"),
    ("Nevěděl", "zeptal se"),
    ("Zůstal doma", "pršelo"),
    ("Udělal chybu", "přiznal se")
]

rows = []
POCET = 5

# 1) Urči, zda se píše čárka
for typ, spojky_list in spojky.items():
    for spojka in spojky_list:
        for _ in range(POCET):
            v1, v2 = random.choice(casti_vet)
            rows.append({
                "prompt": f"Píše se čárka před '{spojka}' ve větě: '{v1} {spojka} {v2}'?",
                "completion": "ano" if typ in ("odporovaci", "vylucovaci", "podradici") else "ne"
            })

# 2) Doplň chybějící čárku
for typ, spojky_list in spojky.items():
    for spojka in spojky_list:
        if typ in ("odporovaci", "vylucovaci", "podradici"):
            for _ in range(POCET):
                v1, v2 = random.choice(casti_vet)
                rows.append({
                    "prompt": f"Doplň čárku: '{v1} {spojka} {v2}'",
                    "completion": f"{v1}, {spojka} {v2}"
                })

# 3) Vyber správnou variantu
for typ, spojky_list in spojky.items():
    for spojka in spojky_list:
        for _ in range(POCET):
            v1, v2 = random.choice(casti_vet)
            if typ in ("odporovaci", "vylucovaci", "podradici"):
                correct = f"{v1}, {spojka} {v2}"
                wrong = f"{v1} {spojka} {v2}"
            else:
                correct = f"{v1} {spojka} {v2}"
                wrong = f"{v1}, {spojka} {v2}"
            options = [correct, wrong]
            random.shuffle(options)
            rows.append({
                "prompt": f"Vyber správnou variantu: A) '{options[0]}'  B) '{options[1]}'",
                "completion": correct
            })

# 4) Oprav chybnou čárku
for typ, spojky_list in spojky.items():
    for spojka in spojky_list:
        for _ in range(POCET):
            v1, v2 = random.choice(casti_vet)
            if typ in ("slucovaci",):
                wrong = f"{v1}, {spojka} {v2}"
                correct = f"{v1} {spojka} {v2}"
            else:
                wrong = f"{v1} {spojka} {v2}"
                correct = f"{v1}, {spojka} {v2}"
            rows.append({
                "prompt": f"Oprav interpunkci: '{wrong}'",
                "completion": correct
            })

# 5) Urči typ spojky
for typ, spojky_list in spojky.items():
    for spojka in spojky_list:
        rows.append({
            "prompt": f"Jaký typ spojky je '{spojka}'?",
            "completion": typ
        })
# 6) Urči typ spojky
for typ, spojky_list in spojky.items():
    for spojka in spojky_list:
        # varianta bez kontextu
        rows.append({
            "prompt": f"Urči typ spojky: '{spojka}'",
            "completion": typ
        })
        # varianta s kontextem
        v1, v2 = random.choice(casti_vet)
        rows.append({
            "prompt": f"Urči typ spojky ve větě: '{v1} {spojka} {v2}'",
            "completion": typ
        })        

# Uložení
with open("training_spojky.jsonl", "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"✅ Hotovo: {len(rows)} úloh uloženo do training_spojky.jsonl")