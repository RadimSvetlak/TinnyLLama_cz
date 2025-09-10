import json
import random
from tab_nouns import nouns

# Předložky rozdělené podle pádu
predlozky_pady = {
    2: ["do", "od", "bez", "z", "ze", "u", "kromě", "místo", "podél",
        "okolo", "kolem", "vedle", "během", "pomocí", "ohledně"],
    3: ["k", "ke", "ku", "naproti", "kvůli", "díky", "vůči", "navzdory", "oproti"],
    4: ["na", "o", "pro", "přes", "pod", "nad", "mezi", "za", "po", "mimo", "skrz"],
    5: [],
    6: ["v", "ve", "na", "o", "při", "po", "nad", "pod", "mezi", "před", "za"],
    7: ["s", "se", "nad", "pod", "před", "za", "mezi"]
}

def vyber_predlozku_k_ke(slovo: str) -> str:
    slovo = slovo.lower()
    if slovo.startswith(("k", "g", "h")) or (
        len(slovo) > 1 and slovo[0] in "kstp" and slovo[1] in "rlmn"
    ):
        return "ke"
    return "k"

def vyber_predlozku_z_ze(slovo: str) -> str:
    slovo = slovo.lower()
    if slovo.startswith(("s", "z", "š", "ž")) or (
        len(slovo) > 1 and slovo[0] in "szšž" and slovo[1] not in "aeiouáéěíóúůý"
    ):
        return "ze"
    return "z"

def vyber_predlozku_s_se(slovo: str) -> str:
    slovo = slovo.lower()
    if slovo.startswith(("s", "š", "z", "ž")) or (
        len(slovo) > 1 and slovo[0] in "szšž" and slovo[1] not in "aeiouáéěíóúůý"
    ):
        return "se"
    return "s"

def random_noun_and_form(pad: int):
    rod = random.choice(list(nouns.keys()))
    lemma = random.choice(list(nouns[rod].keys()))
    form = nouns[rod][lemma]["sg"][pad - 1]
    return lemma, form

rows = []
POCET_NOUNS_NA_PREDLOZKU = 15

# 1) až 6) doplň správný pád
for pad in range(2, 8):  # 2. až 7. pád
    for pred in predlozky_pady[pad]:
        for _ in range(POCET_NOUNS_NA_PREDLOZKU):
            lemma, form = random_noun_and_form(pad)
            base_pred = pred
            if pred in ("k", "ke"):
                base_pred = vyber_predlozku_k_ke(form)
            if pred in ("z", "ze"):
                base_pred = vyber_predlozku_z_ze(form)
            if pred in ("s", "se"):
                base_pred = vyber_predlozku_s_se(form)

            rows.append({
                "prompt": f"doplň {pad}. pád slova '{lemma}': '{base_pred} __ '",
                "completion": f"{base_pred} {form}"
            })

# 7) až 13) urči pád po předložce (s podstatným jménem)
for pad in range(2, 8):
    for pred in predlozky_pady[pad]:
        lemma, form = random_noun_and_form(pad)
        base_pred = pred
        if pred in ("k", "ke"):
            base_pred = vyber_predlozku_k_ke(form)
        if pred in ("z", "ze"):
            base_pred = vyber_predlozku_z_ze(form)
        if pred in ("s", "se"):
            base_pred = vyber_predlozku_s_se(form)

        rows.append({
            "prompt": f"urči pád po předložce: '{base_pred} {form}'",
            "completion": str(pad)
        })

# 14) vyber správný tvar předložky (k/ke, z/ze, s/se)
varianty = {
    ("k", "ke"): vyber_predlozku_k_ke,
    ("z", "ze"): vyber_predlozku_z_ze,
    ("s", "se"): vyber_predlozku_s_se
}

for (var1, var2), func in varianty.items():
    pad = 3 if var1 in ("k", "ke") else (2 if var1 in ("z", "ze") else 7)
    for _ in range(POCET_NOUNS_NA_PREDLOZKU * 2):
        lemma, form = random_noun_and_form(pad)
        correct = func(form)
        wrong = var2 if correct == var1 else var1
        options = [correct, wrong]
        random.shuffle(options)
        rows.append({
            "prompt": f"vyber správnou variantu předložky pro '{form}': A '{options[0]}', B '{options[1]}'",
            "completion": correct
        })

# 15) doplň chybějící předložku podle významu
for pad in range(2, 8):
    for pred in predlozky_pady[pad]:
        for _ in range(POCET_NOUNS_NA_PREDLOZKU):
            lemma, form = random_noun_and_form(pad)
            base_pred = pred
            if pred in ("k", "ke"):
                base_pred = vyber_predlozku_k_ke(form)
            if pred in ("z", "ze"):
                base_pred = vyber_predlozku_z_ze(form)
            if pred in ("s", "se"):
                base_pred = vyber_predlozku_s_se(form)

            rows.append({
                "prompt": f"doplň chybějící předložku: '___ {form} '",
                "completion": base_pred
            })

# 16) oprav chybný tvar předložky
varianty = {
    ("k", "ke"): vyber_predlozku_k_ke,
    ("z", "ze"): vyber_predlozku_z_ze,
    ("s", "se"): vyber_predlozku_s_se
}

for (var1, var2), func in varianty.items():
    pad = 3 if var1 in ("k", "ke") else (2 if var1 in ("z", "ze") else 7)
    for _ in range(POCET_NOUNS_NA_PREDLOZKU * 2):
        lemma, form = random_noun_and_form(pad)
        correct = func(form)
        wrong = var1 if correct == var2 else var2  # záměrně opačně
        rows.append({
            "prompt": f"oprav chybný tvar: 'šel {wrong} {form}'",
            "completion": f"šel {correct} {form}"
        })

# Uložení
with open("training_predlozky.jsonl", "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"✅ Hotovo: {len(rows)} úloh uloženo do training_predlozky.jsonl")