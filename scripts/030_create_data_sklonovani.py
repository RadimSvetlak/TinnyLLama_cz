# -*- coding: utf-8 -*-

"""
# 📄 Generátor tréninkových promptů pro podstatná jména

Tento skript automaticky vytváří **rozšířený set úloh** pro trénink modelu na skloňování podstatných jmen.  
Používá:
- **`nouns`** z modulu [`tab_nouns.py`] – obsahuje podstatná jména roztříděná podle rodu a životnosti, včetně všech pádů pro jednotné a množné číslo.
- **`adjectives`** z modulu [`tab_adjectives.py`] – obsahuje skloňované tvary přídavných jmen podle rodu, čísla a pádu.

## 🔹 Co skript dělá
1. **Importuje** data z `tab_nouns` a `tab_adjectives`.
2. **Pro každý lemma** (slovo) a dostupné číslo (sg/pl):
   - Vygeneruje **10 typů úloh** pro každý pád:
     1. Přímý požadavek na tvar.
     2. Otázka odpovídající pádu.
     3. Doplňovačka (cloze) s kontextem.
     4. Multiple-choice s distractory.
     5. Oprava chybného tvaru ve větě.
     6. Určení pádu podle zadaného tvaru.
     7. Převod věty do jiného pádu.
     8. Určení tvaru v opačném čísle (pokud existuje).
     9. Pádová série (více pádů za sebou).
     10. Spojení s přídavným jménem (tvar adjektiva se určuje z `tab_adjectives` podle rodu, čísla a pádu).
   - Přidá souhrnnou úlohu pro všechny pády.
3. **Uloží** všechny generované úlohy do souboru `train_prompts_nouns.jsonl` ve formátu JSON Lines.

## 🔹 Formát vstupních dat (`tab_nouns.nouns`)
"""

import json, random
from tab_nouns import nouns
from tab_adjectives import adjectives

CASE_NAMES = ["Nominativ", "Genitiv", "Dativ", "Akuzativ", "Vokativ", "Lokál", "Instrumentál"]
CASE_QUESTIONS = {
    "Nominativ": "Kdo? Co?",
    "Genitiv": "Koho? Čeho?",
    "Dativ": "Komu? Čemu?",
    "Akuzativ": "Koho? Co?",
    "Vokativ": "Oslovení",
    "Lokál": "O kom? O čem?",
    "Instrumentál": "S kým? S čím?"
}
SENTENCE_STARTERS = {
    "Nominativ": ["Toto je ", "Tohle je ", "Hlavní postava je ", "Na fotografii je "],
    "Genitiv": ["Bez ", "Uprostřed ", "Vedle ", "Během "],
    "Dativ": ["Za to děkuji ", "Napíšu ", "Pomohu ", "Svěřil jsem se "],
    "Akuzativ": ["Vidím ", "Potřebuji ", "Hledám ", "Přinesl jsem "],
    "Vokativ": ["Hej, ", "Haló, ", "Milý ", "Vážený "],
    "Lokál": ["Mluvili jsme o ", "Píšu o ", "Přemýšlím o ", "Četl jsem o "],
    "Instrumentál": ["Jdu s ", "Pracuji s ", "Setkal jsem se s ", "Mluvím s "],
}
GENDER_MAP = {
    "ž": {"gender": "feminine", "animacy": "inanimate"},
    "s": {"gender": "neuter", "animacy": "inanimate"},
    "m_živ": {"gender": "masculine", "animacy": "animate"},
    "m_nživ": {"gender": "masculine", "animacy": "inanimate"}
}

def validate_forms(forms):
    return isinstance(forms, list) and len(forms) == 7 and all(isinstance(x, str) and x.strip() for x in forms)

def generate_tasks(lemma, forms, number, gender_key, opposite_forms=None, include_vocative=True):
    rows = []
    nlabel = 'jednotném' if number == 'sg' else 'množném'
    for i, form in enumerate(forms):
        case_name = CASE_NAMES[i]
        if case_name == "Vokativ" and not include_vocative:
            continue

        # 1 přímý tvar
        rows.append({"prompt": f"Napiš slovo „{lemma}“ v {i+1}. pádě ({nlabel} číslo).", "completion": form})
        # 2 pádová otázka
        rows.append({"prompt": f"Na otázku „{CASE_QUESTIONS[case_name]}“ odpovídá u slova „{lemma}“ tvar ({nlabel}):", "completion": form})
        # 3 cloze
        starter = random.choice(SENTENCE_STARTERS[case_name])
        rows.append({"prompt": f"Doplň správný tvar: {starter} ({lemma} v pádě {case_name}, {nlabel}).", "completion": form})
        # 4 multiple choice
        distractors = random.sample([f for j,f in enumerate(forms) if j != i], min(2, 6))
        opts = [form] + distractors
        random.shuffle(opts)
        rows.append({"prompt": f"Vyber správný {i+1}. pád slova „{lemma}“ ({nlabel}): {' / '.join(opts)}", "completion": form})
        # 5 oprava chyby
        wrong = random.choice(distractors) if distractors else form
        sentence = f"Bez {wrong} se neobejdu." if case_name=="Genitiv" else f"Vidím {wrong}."
        rows.append({"prompt": f"Ve větě je chybný tvar, nahraď ho správným {i+1}. pádem slova „{lemma}“: {sentence}", "completion": form})
        # 6 určení pádu
        rows.append({"prompt": f"Urči, ve kterém pádě ({nlabel}) je tvar „{form}“ slova „{lemma}“.", "completion": f"{i+1}. pád"})
        # 7 změna pádu
        target_idx = random.choice([x for x in range(7) if x != i])
        rows.append({"prompt": f"Změň větu „Toto je {form}“ tak, aby „{lemma}“ bylo v {CASE_NAMES[target_idx]} ({nlabel}):", "completion": forms[target_idx]})
        # 8 protikladné číslo
        if opposite_forms and validate_forms(opposite_forms):
            opp_label = 'množném' if number == 'sg' else 'jednotném'
            rows.append({"prompt": f"Napiš {i+1}. pád v {opp_label} čísle ke tvaru „{form}“.", "completion": opposite_forms[i]})
        # 9 pádová série
        if i <= 4:
            end = min(i+3, 7)
            rows.append({"prompt": f"Napiš tvary {', '.join(CASE_NAMES[i:end])} ({nlabel}) slova „{lemma}“.", "completion": ", ".join(forms[i:end])})
        # 10 spojení s přídavným jménem – použij skloňování z tab_adjectives
        adj_lemma = random.choice(list(adjectives.keys()))
        adj_form = adj_lemma
        if gender_key in adjectives[adj_lemma]:
            if number in adjectives[adj_lemma][gender_key]:
                adj_forms = adjectives[adj_lemma][gender_key][number]
                if i < len(adj_forms):
                    adj_form = adj_forms[i]
        completion = f"{adj_form} {form}"
        rows.append({"prompt": f"Spojte slovo „{lemma}“ v {i+1}. pádě ({nlabel}) s přídavným jménem „{adj_lemma}“.", "completion": completion})

    # souhrn všech pádů
    rows.append({"prompt": f"Vypiš všech 7 pádů ({nlabel}) slova „{lemma}“.", "completion": "\n".join(forms)})
    return rows

# hlavní běh
out_rows = []
for gender_key, words in nouns.items():
    meta = GENDER_MAP.get(gender_key, {"gender": "unknown", "animacy": "unknown"})
    include_voc = not (meta["animacy"] == "inanimate")  # vokativ vypnout pro neživotná
    for lemma, entry in words.items():
        sg_forms = entry.get("sg") if validate_forms(entry.get("sg", [])) else None
        pl_forms = entry.get("pl") if validate_forms(entry.get("pl", [])) else None
        if sg_forms:
            out_rows.extend(generate_tasks(lemma, sg_forms, "sg", gender_key, opposite_forms=pl_forms, include_vocative=include_voc))
        if pl_forms:
            out_rows.extend(generate_tasks(lemma, pl_forms, "pl", gender_key, opposite_forms=sg_forms, include_vocative=include_voc))

with open("train_prompts_nouns.jsonl", "w", encoding="utf-8") as f:
    for r in out_rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"Hotovo. Uloženo {len(out_rows)} řádků do train_prompts_nouns.jsonl")