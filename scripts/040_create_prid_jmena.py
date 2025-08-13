# ------------------------------------------------------------
# Název: Generátor tréninkových úloh pro přídavná jména v češtině
# Popis:
#   Tento skript vytváří JSONL soubor s tréninkovými dvojicemi
#   prompt–completion pro procvičování přídavných jmen a jejich
#   shody s podstatnými jmény v různých rodech, číslech a pádech.
#
#   Obsahuje:
#     - Funkci generate_adjective_tasks:
#         Náhodně vybírá rod, podstatné jméno, přídavné jméno, číslo
#         (sg/pl) a pád, a generuje úlohy ve formátu:
#         prompt = instrukce k vytvoření shody adjektiv a substantiv
#         completion = správná dvojice tvarů (přídavné + podstatné jméno).
#     - Funkci generate_extra_prompts:
#         * Úlohy na transformaci přídavných jmen mezi pády.
#         * Úlohy na shodu přídavného jména s daným podstatným jménem.
#         * Úlohy na stupňování vybraných přídavných jmen (2. a 3. stupeň).
#         * Dodatečné otázky kombinující přídavné a podstatné jméno
#           v konkrétním pádě a čísle.
#     - Export všech úloh do JSON Lines formátu.
#
# Vstupy:
#   - Slovník `adjectives` obsahující tvary přídavných jmen dle rodu,
#     čísla a pádu.
#   - Slovník `nouns` obsahující tvary podstatných jmen dle rodu,
#     čísla a pádu.
#   - Seznam `cases` s názvy pádů.
#
# Výstup:
#   - Soubor "adjective_tasks.jsonl" obsahující generované prompty
#     a odpovědi pro trénink modelu.
#
# Závislosti:
#   - Python 3.8+
#   - random (standardní knihovna)
#   - json (standardní knihovna)
#
# Autor: [Tvůj Nick/Jméno]
# ------------------------------------------------------------



adjectives = {
    "velký": {
        "ž": {
            "sg": ["velká", "velké", "velké", "velkou", "velká", "velké", "velkou"],
            "pl": ["velké", "velkých", "velkým", "velké", "velkými", "velkých", "velké"]
        },
        "s": {
            "sg": ["velké", "velkého", "velkému", "velké", "velké", "velkém", "velkým"],
            "pl": ["velká", "velkých", "velkým", "velká", "velkými", "velkých", "velká"]
        },
        "m_živ": {
            "sg": ["velký", "velkého", "velkému", "velkého", "velký", "velkém", "velkým"],
            "pl": ["velcí", "velkých", "velkým", "velké", "velcí", "velkých", "velkými"]
        },
        "m_nživ": {
            "sg": ["velký", "velkého", "velkému", "velký", "velký", "velkém", "velkým"],
            "pl": ["velké", "velkých", "velkým", "velké", "velké", "velkých", "velkými"]
        }
    },
    "malý": {
        "ž": {
            "sg": ["malá", "malé", "malé", "malou", "malá", "malé", "malou"],
            "pl": ["malé", "malých", "malým", "malé", "malými", "malých", "malé"]
        },
        "s": {
            "sg": ["malé", "malého", "malému", "malé", "malé", "malém", "malým"],
            "pl": ["malá", "malých", "malým", "malá", "malými", "malých", "malá"]
        },
        "m_živ": {
            "sg": ["malý", "malého", "malému", "malého", "malý", "malém", "malým"],
            "pl": ["malí", "malých", "malým", "malé", "malí", "malých", "malými"]
        },
        "m_nživ": {
            "sg": ["malý", "malého", "malému", "malý", "malý", "malém", "malým"],
            "pl": ["malé", "malých", "malým", "malé", "malé", "malých", "malými"]
        }
    },

    "nový": {
        "ž": {
            "sg": ["nová", "nové", "nové", "novou", "nová", "nové", "novou"],
            "pl": ["nové", "nových", "novým", "nové", "novými", "nových", "nové"]
        },
        "s": {
            "sg": ["nové", "nového", "novému", "nové", "nové", "novém", "novým"],
            "pl": ["nová", "nových", "novým", "nová", "novými", "nových", "nová"]
        },
        "m_živ": {
            "sg": ["nový", "nového", "novému", "nového", "nový", "novém", "novým"],
            "pl": ["noví", "nových", "novým", "nové", "noví", "nových", "novými"]
        },
        "m_nživ": {
            "sg": ["nový", "nového", "novému", "nový", "nový", "novém", "novým"],
            "pl": ["nové", "nových", "novým", "nové", "nové", "nových", "novými"]
        }
    },

    "starý": {
        "ž": {
            "sg": ["stará", "staré", "staré", "starou", "stará", "staré", "starou"],
            "pl": ["staré", "starých", "starým", "staré", "starými", "starých", "staré"]
        },
        "s": {
            "sg": ["staré", "starého", "starému", "staré", "staré", "starém", "starým"],
            "pl": ["stará", "starých", "starým", "stará", "starými", "starých", "stará"]
        },
        "m_živ": {
            "sg": ["starý", "starého", "starému", "starého", "starý", "starém", "starým"],
            "pl": ["staří", "starých", "starým", "staré", "staří", "starých", "starými"]
        },
        "m_nživ": {
            "sg": ["starý", "starého", "starému", "starý", "starý", "starém", "starým"],
            "pl": ["staré", "starých", "starým", "staré", "staré", "starých", "starými"]
        }
    },

    "český": {
        "ž": {
            "sg": ["česká", "české", "české", "českou", "česká", "české", "českou"],
            "pl": ["české", "českých", "českým", "české", "českými", "českých", "české"]
        },
        "s": {
            "sg": ["české", "českého", "českému", "české", "české", "českém", "českým"],
            "pl": ["česká", "českých", "českým", "česká", "českými", "českých", "česká"]
        },
        "m_živ": {
            "sg": ["český", "českého", "českému", "českého", "český", "českém", "českým"],
            "pl": ["čeští", "českých", "českým", "české", "čeští", "českých", "českými"]
        },
        "m_nživ": {
            "sg": ["český", "českého", "českému", "český", "český", "českém", "českým"],
            "pl": ["české", "českých", "českým", "české", "české", "českých", "českými"]
        }
    },
    "dobrý": {
        "ž": {
            "sg": ["dobrá", "dobré", "dobré", "dobrou", "dobrá", "dobré", "dobrou"],
            "pl": ["dobré", "dobrých", "dobrým", "dobré", "dobrými", "dobrých", "dobré"]
        },
        "s": {
            "sg": ["dobré", "dobrého", "dobrému", "dobré", "dobré", "dobrém", "dobrým"],
            "pl": ["dobrá", "dobrých", "dobrým", "dobrá", "dobrými", "dobrých", "dobrá"]
        },
        "m_živ": {
            "sg": ["dobrý", "dobrého", "dobrému", "dobrého", "dobrý", "dobrém", "dobrým"],
            "pl": ["dobří", "dobrých", "dobrým", "dobré", "dobří", "dobrých", "dobrými"]
        },
        "m_nživ": {
            "sg": ["dobrý", "dobrého", "dobrému", "dobrý", "dobrý", "dobrém", "dobrým"],
            "pl": ["dobré", "dobrých", "dobrým", "dobré", "dobré", "dobrých", "dobrými"]
        }
    },

    "špatný": {
        "ž": {
            "sg": ["špatná", "špatné", "špatné", "špatnou", "špatná", "špatné", "špatnou"],
            "pl": ["špatné", "špatných", "špatným", "špatné", "špatnými", "špatných", "špatné"]
        },
        "s": {
            "sg": ["špatné", "špatného", "špatnému", "špatné", "špatné", "špatném", "špatným"],
            "pl": ["špatná", "špatných", "špatným", "špatná", "špatnými", "špatných", "špatná"]
        },
        "m_živ": {
            "sg": ["špatný", "špatného", "špatnému", "špatného", "špatný", "špatném", "špatným"],
            "pl": ["špatní", "špatných", "špatným", "špatné", "špatní", "špatných", "špatnými"]
        },
        "m_nživ": {
            "sg": ["špatný", "špatného", "špatnému", "špatný", "špatný", "špatném", "špatným"],
            "pl": ["špatné", "špatných", "špatným", "špatné", "špatné", "špatných", "špatnými"]
        }
    },

    "krásný": {
        "ž": {
            "sg": ["krásná", "krásné", "krásné", "krásnou", "krásná", "krásné", "krásnou"],
            "pl": ["krásné", "krásných", "krásným", "krásné", "krásnými", "krásných", "krásné"]
        },
        "s": {
            "sg": ["krásné", "krásného", "krásnému", "krásné", "krásné", "krásném", "krásným"],
            "pl": ["krásná", "krásných", "krásným", "krásná", "krásnými", "krásných", "krásná"]
        },
        "m_živ": {
            "sg": ["krásný", "krásného", "krásnému", "krásného", "krásný", "krásném", "krásným"],
            "pl": ["krásní", "krásných", "krásným", "krásné", "krásní", "krásných", "krásnými"]
        },
        "m_nživ": {
            "sg": ["krásný", "krásného", "krásnému", "krásný", "krásný", "krásném", "krásným"],
            "pl": ["krásné", "krásných", "krásným", "krásné", "krásné", "krásných", "krásnými"]
        }
    },

    "rychlý": {
        "ž": {
            "sg": ["rychlá", "rychlé", "rychlé", "rychlou", "rychlá", "rychlé", "rychlou"],
            "pl": ["rychlé", "rychlých", "rychlým", "rychlé", "rychlými", "rychlých", "rychlé"]
        },
        "s": {
            "sg": ["rychlé", "rychlého", "rychlému", "rychlé", "rychlé", "rychlém", "rychlým"],
            "pl": ["rychlá", "rychlých", "rychlým", "rychlá", "rychlými", "rychlých", "rychlá"]
        },
        "m_živ": {
            "sg": ["rychlý", "rychlého", "rychlému", "rychlého", "rychlý", "rychlém", "rychlým"],
            "pl": ["rychlí", "rychlých", "rychlým", "rychlé", "rychlí", "rychlých", "rychlými"]
        },
        "m_nživ": {
            "sg": ["rychlý", "rychlého", "rychlému", "rychlý", "rychlý", "rychlém", "rychlým"],
            "pl": ["rychlé", "rychlých", "rychlým", "rychlé", "rychlé", "rychlých", "rychlými"]
        }
    },

    "těžký": {
        "ž": {
            "sg": ["těžká", "těžké", "těžké", "těžkou", "těžká", "těžké", "těžkou"],
            "pl": ["těžké", "těžkých", "těžkým", "těžké", "těžkými", "těžkých", "těžké"]
        },
        "s": {
            "sg": ["těžké", "těžkého", "těžkému", "těžké", "těžké", "těžkém", "těžkým"],
            "pl": ["těžká", "těžkých", "těžkým", "těžká", "těžkými", "těžkých", "těžká"]
        },
        "m_živ": {
            "sg": ["těžký", "těžkého", "těžkému", "těžkého", "těžký", "těžkém", "těžkým"],
            "pl": ["těžcí", "těžkých", "těžkým", "těžké", "těžcí", "těžkých", "těžkými"]
        },
        "m_nživ": {
            "sg": ["těžký", "těžkého", "těžkému", "těžký", "těžký", "těžkém", "těžkým"],
            "pl": ["těžké", "těžkých", "těžkým", "těžké", "těžké", "těžkých", "těžkými"]
        }
    }   
}

nouns = {
    "ž": {
        "kniha": {
            "sg": ["kniha", "knihy", "knize", "knihu", "kniho", "knize", "knihou"],
            "pl": ["knihy", "knih", "knihám", "knihy", "knihy", "knihách", "knihami"]
        },
        "žena": {
            "sg": ["žena", "ženy", "ženě", "ženu", "ženo", "ženě", "ženou"],
            "pl": ["ženy", "žen", "ženám", "ženy", "ženy", "ženách", "ženami"]
        },
        "škola": {
            "sg": ["škola", "školy", "škole", "školu", "školo", "škole", "školou"],
            "pl": ["školy", "škol", "školám", "školy", "školy", "školách", "školami"]
        },
        "ulice": {
            "sg": ["ulice", "ulice", "ulici", "ulici", "ulice", "ulici", "ulicí"],
            "pl": ["ulice", "ulic", "ulicím", "ulice", "ulice", "ulicích", "ulicemi"]
        },
        "noc": {
            "sg": ["noc", "noci", "noci", "noc", "noci", "noci", "nocí"],
            "pl": ["noci", "nocí", "nocím", "noci", "noci", "nocích", "nocemi"]
        }
    },
    "s": {
        "auto": {
            "sg": ["auto", "auta", "autu", "auto", "auto", "autu", "autem"],
            "pl": ["auta", "aut", "autům", "auta", "auta", "autech", "auty"]
        },
        "město": {
            "sg": ["město", "města", "městu", "město", "město", "městě", "městem"],
            "pl": ["města", "měst", "městům", "města", "města", "městech", "městy"]
        },
        "moře": {
            "sg": ["moře", "moře", "moři", "moře", "moře", "moři", "mořem"],
            "pl": ["moře", "moří", "mořím", "moře", "moře", "mořích", "mořemi"]
        },
        "slunce": {
            "sg": ["slunce", "slunce", "slunci", "slunce", "slunce", "slunci", "sluncem"],
            "pl": ["slunce", "sluncí", "sluncím", "slunce", "slunce", "sluncích", "slunci"]
        },
        "srdce": {
            "sg": ["srdce", "srdce", "srdci", "srdce", "srdce", "srdci", "srdcem"],
            "pl": ["srdce", "srdcí", "srdcím", "srdce", "srdce", "srdcích", "srdci"]
        }
    },
    "m_živ": {
        "muž": {
            "sg": ["muž", "muže", "muži", "muže", "muži", "muži", "mužem"],
            "pl": ["muži", "mužů", "mužům", "muže", "muži", "mužích", "muži"]
        },
        "student": {
            "sg": ["student", "studenta", "studentovi", "studenta", "studente", "studentovi", "studentem"],
            "pl": ["studenti", "studentů", "studentům", "studenty", "studenti", "studentech", "studenty"]
        },
        "učitel": {
            "sg": ["učitel", "učitele", "učiteli", "učitele", "učiteli", "učiteli", "učitelem"],
            "pl": ["učitelé", "učitelů", "učitelům", "učitele", "učitelé", "učitelích", "učiteli"]
        },
        "lékař": {
            "sg": ["lékař", "lékaře", "lékaři", "lékaře", "lékaři", "lékaři", "lékařem"],
            "pl": ["lékaři", "lékařů", "lékařům", "lékaře", "lékaři", "lékařích", "lékaři"]
        },
        "kluk": {
            "sg": ["kluk", "kluka", "klukovi", "kluka", "kluku", "klukovi", "klukem"],
            "pl": ["kluci", "kluků", "klukům", "kluky", "kluci", "klucích", "kluky"]
        }
    },
    "m_nživ": {
        "dům": {
            "sg": ["dům", "domu", "domu", "dům", "dome", "domě", "domem"],
            "pl": ["domy", "domů", "domům", "domy", "domy", "domech", "domy"]
        },
        "hrad": {
            "sg": ["hrad", "hradu", "hradu", "hrad", "hrade", "hradě", "hradem"],
            "pl": ["hrady", "hradů", "hradům", "hrady", "hrady", "hradech", "hrady"]
        },
        "strom": {
            "sg": ["strom", "stromu", "stromu", "strom", "strome", "stromě", "stromem"],
            "pl": ["stromy", "stromů", "stromům", "stromy", "stromy", "stromech", "stromy"]
        },
        "papír": {
            "sg": ["papír", "papíru", "papíru", "papír", "papíre", "papíře", "papírem"],
            "pl": ["papíry", "papírů", "papírům", "papíry", "papíry", "papírech", "papíry"]
        },
        "stůl": {
            "sg": ["stůl", "stolu", "stolu", "stůl", "stole", "stole", "stolem"],
            "pl": ["stoly", "stolů", "stolům", "stoly", "stoly", "stolech", "stoly"]
        }
    }
}
import random
import json

# Pádové názvy
cases = ["1. pád", "2. pád", "3. pád", "4. pád", "5. pád", "6. pád", "7. pád"]

def generate_adjective_tasks(adjectives, nouns, cases, num_tasks=300):
    tasks = []

    for _ in range(num_tasks):
        rod = random.choice(list(nouns.keys()))
        podst_jm = random.choice(list(nouns[rod].keys()))
        adj = random.choice(list(adjectives.keys()))
        cislo = random.choice(["sg", "pl"])
        pad_index = random.randint(0, 6)
        pad_label = cases[pad_index]

        try:
            adj_form = adjectives[adj][rod][cislo][pad_index]
            noun_form = nouns[rod][podst_jm][cislo][pad_index]
        except KeyError:
            continue

        prompt = f"Napiš přídavné jméno '{adj}' ve spojení se slovem '{podst_jm}'. Použij {pad_label}, {cislo}"
        completion = f"{adj_form} {noun_form}"

        tasks.append({
            "prompt": prompt,
            "completion": completion
        })

    return tasks

def generate_extra_prompts(adjectives, nouns, cases, num_per_type=50):
    prompts = []

    # 2. Transformace mezi pády
    for _ in range(num_per_type):
        adj = random.choice(list(adjectives.keys()))
        rod = random.choice(list(adjectives[adj].keys()))
        cislo = random.choice(["sg", "pl"])
        from_index = random.randint(0, 6)
        to_index = random.randint(0, 6)
        if from_index == to_index:
            continue

        try:
            from_form = adjectives[adj][rod][cislo][from_index]
            to_form = adjectives[adj][rod][cislo][to_index]
        except KeyError:
            continue

        prompts.append({
            "prompt": f"Změň přídavné jméno '{adj}' z {cases[from_index]} do {cases[to_index]} ({cislo}, {rod} rod):",
            "completion": to_form
        })

    # 3. Shoda s podstatným jménem
    for _ in range(num_per_type):
        rod = random.choice(list(nouns.keys()))
        podst_jm = random.choice(list(nouns[rod].keys()))
        adj = random.choice(list(adjectives.keys()))
        cislo = random.choice(["sg", "pl"])
        pad_index = random.randint(0, 6)

        try:
            adj_form = adjectives[adj][rod][cislo][pad_index]
        except KeyError:
            continue

        prompts.append({
            "prompt": f"Jaký tvar má přídavné jméno '{adj}' pro podstatné jméno '{podst_jm}' ({cases[pad_index]}, {cislo})?",
            "completion": adj_form
        })

    # 4. Stupňování
    gradation_map = {
        "malý": ["menší", "nejmenší"],
        "dobrý": ["lepší", "nejlepší"],
        "špatný": ["horší", "nejhorší"],
        "vysoký": ["vyšší", "nejvyšší"],
        "rychlý": ["rychlejší", "nejrychlejší"]
    }
    for adj, forms in gradation_map.items():
        prompts.append({
            "prompt": f"Jaký je 2. stupeň přídavného jména '{adj}'?",
            "completion": forms[0]
        })
        prompts.append({
            "prompt": f"Jaký je 3. stupeň přídavného jména '{adj}'?",
            "completion": forms[1]
        })

    # 7. Otázky
    for _ in range(num_per_type):
        rod = random.choice(list(nouns.keys()))
        podst_jm = random.choice(list(nouns[rod].keys()))
        adj = random.choice(list(adjectives.keys()))
        cislo = random.choice(["sg", "pl"])
        pad_index = random.randint(0, 6)

        try:
            adj_form = adjectives[adj][rod][cislo][pad_index]
            noun_form = nouns[rod][podst_jm][cislo][pad_index]
        except KeyError:
            continue

        prompts.append({
            "prompt": f"Jaký tvar má přídavné jméno '{adj}' pro slovo '{podst_jm}' v {cases[pad_index]} ({cislo})?",
            "completion": f"{adj_form} {noun_form}"
        })

    return prompts

# Použití + export
if __name__ == "__main__":
    # Předpokládáme, že máš definované `adjectives` a `nouns`
    tasks = generate_adjective_tasks(adjectives, nouns, cases, num_tasks=300)
    extra_tasks = extra_tasks = generate_extra_prompts(adjectives, nouns, cases)
    all_tasks = tasks + extra_tasks

    with open("adjective_tasks.jsonl", "w", encoding="utf-8") as f:
        for task in all_tasks:
            f.write(json.dumps(task, ensure_ascii=False) + "\n")

    print(f"✅ Vygenerováno {len(all_tasks)} úloh (včetně smysluplných) a uloženo do 'adjective_tasks.jsonl'")