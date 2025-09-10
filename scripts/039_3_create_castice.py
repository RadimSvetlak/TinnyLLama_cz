import json
import random

# Slovníky
castice = {
    "modalni": ["asi", "snad", "prý", "určitě", "bohužel", "možná"],
    "zduraznovaci": ["jen", "právě", "přece", "teprve"],
    "tazaci": ["copak", "jestli", "zda"],
    "praci": ["ať", "nechť", "kéž"],
    "praci_aby": ["aby"]
}

citoslovce = {
    "city": ["ach", "jé", "fuj", "hurá"],
    "vyzvy": ["hej", "pst", "hop", "pozor"],
    "zvuky": ["bum", "mňau", "haf", "tik-tak"]
}

# Šablony pro částice
vety_castice = {
    "modalni": [
        "___ přijde později.",
        "___ se mu to podaří.",
        "___ to stihneme."
    ],
    "zduraznovaci": [
        "Podívej, to je ___ ale krása!",
        "To je ___ neuvěřitelné!"
    ],
    "tazaci": [
        "___ víš, co se stalo?",
        "Řekni mi, ___ přijde."
    ],
    "praci": [
        "___ se mu to podaří.",
        "___ můžeš, pojď sem!"
    ]
}

# Speciální šablony pro "aby"
vety_praci_aby = [
    "Přeji si, ___ se to stalo.",
    "Chtěl bych, ___ přišel včas.",
    "Udělal to, ___ vyhrál závod.",
    "Bylo by dobré, ___ se to podařilo."
]

# Šablony pro citoslovce
vety_citoslovce = {
    "city": [
        "___, to je ale krása!",
        "___, to snad není možné!"
    ],
    "vyzvy": [
        "___, pojď sem!",
        "___, dej mi to!"
    ],
    "zvuky": [
        "___, dveře se zabouchly.",
        "___, spadl talíř."
    ]
}

rows = []

# 1) Rozpoznání
for typ, slova in castice.items():
    for slovo in slova:
        rows.append({
            "prompt": f"Najdi částici ve větě: 'Řekl, že {slovo} přijde.'",
            "completion": slovo
        })

for typ, slova in citoslovce.items():
    for slovo in slova:
        rows.append({
            "prompt": f"Najdi citoslovce ve větě: '{slovo}, to je ale překvapení!'",
            "completion": slovo
        })

# 2) Klasifikace
for typ, slova in castice.items():
    for slovo in slova:
        rows.append({
            "prompt": f"Jaký typ částice je '{slovo}'?",
            "completion": typ
        })

for typ, slova in citoslovce.items():
    for slovo in slova:
        rows.append({
            "prompt": f"Jaký druh citoslovce je '{slovo}'?",
            "completion": typ
        })

# 3) Doplnění (unikátní kombinace)
for typ, slova in castice.items():
    if typ == "praci_aby":
        for slovo in slova:
            for sablona in vety_praci_aby:
                rows.append({
                    "prompt": f"Doplň chybějící částici: '{sablona}'",
                    "completion": slovo
                })
    elif typ in vety_castice:
        for slovo in slova:
            for sablona in vety_castice[typ]:
                rows.append({
                    "prompt": f"Doplň chybějící částici: '{sablona}'",
                    "completion": slovo
                })

for typ, slova in citoslovce.items():
    for slovo in slova:
        for sablona in vety_citoslovce[typ]:
            rows.append({
                "prompt": f"Doplň chybějící citoslovce: '{sablona}'",
                "completion": slovo
            })

# 4) Nahrazení
for typ, slova in castice.items():
    for slovo in slova:
        synonymum = random.choice([s for s in slova if s != slovo]) if len(slova) > 1 else slovo
        rows.append({
            "prompt": f"Nahraď částici '{slovo}' synonymem ve větě: 'Řekl, že {slovo} přijde.'",
            "completion": synonymum
        })

for typ, slova in citoslovce.items():
    for slovo in slova:
        synonymum = random.choice([s for s in slova if s != slovo]) if len(slova) > 1 else slovo
        rows.append({
            "prompt": f"Nahraď citoslovce '{slovo}' jiným se stejným významem.",
            "completion": synonymum
        })

# 5) Použití
for typ, slova in castice.items():
    for slovo in slova:
        rows.append({
            "prompt": f"Vytvoř větu s částicí '{slovo}'.",
            "completion": f"{slovo} to stihneme."
        })

for typ, slova in citoslovce.items():
    for slovo in slova:
        rows.append({
            "prompt": f"Vytvoř větu s citoslovcem '{slovo}'.",
            "completion": f"{slovo}, to je ale překvapení!"
        })

# Uložení
with open("training_castice_citoslovce.jsonl", "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"✅ Hotovo: {len(rows)} úloh uloženo do training_castice_citoslovce.jsonl")