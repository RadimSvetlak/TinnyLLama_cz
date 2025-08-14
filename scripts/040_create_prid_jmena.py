# ------------------------------------------------------------
# Název: Generátor tréninkových úloh pro přídavná jména v češtině
# Popis:
#   Vytváří JSONL soubor s tréninkovými dvojicemi prompt–completion
#   pro shodu adjektiv a substantiv (včetně 5. pádu), transformace
#   mezi pády, kontext s předložkami, vokativ, výběrové úlohy a
#   stupňování. Důraz na jasné instrukce a krátké odpovědi.
#
# Formát výstupu:
#   { "prompt": "...", "completion": "..." }
#
# Autor: [Tvůj Nick/Jméno]
# ------------------------------------------------------------

import random
import json
from collections import Counter

# --- Databáze tvarů ---

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
            "pl": ["rychlé", "rychlých", "rychlým", "rychlé", "rychlé", "rychkých", "rychlými"]
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
            # oprava lokálu sg: "autě" místo "autu"
            "sg": ["auto", "auta", "autu", "auto", "auto", "autě", "autem"],
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

# --- Konfigurace a utilitky ---

CASES = ["1. pád", "2. pád", "3. pád", "4. pád", "5. pád", "6. pád", "7. pád"]
CASE_INDEXES = list(range(7))  # 0..6, ponecháváme i 5. pád (vokativ)

PREP_BY_CASE = {
    1: [],                 # N
    2: ["bez", "do", "od"],# G
    3: ["k", "proti"],     # D
    4: ["pro", "na", "vidím"], # A; "vidím" použijeme jako slovesa v pseudo-větě
    5: [],                 # Vokativ bez předložky; speciální šablona níže
    6: ["o", "v", "na"],   # L
    7: ["s", "před", "za"] # I
}

def set_seed(seed: int = 42):
    random.seed(seed)

def case_label(pad_idx: int) -> str:
    return CASES[pad_idx]

def normalize_completion(text: str) -> str:
    # lowercase, jeden whitespace, bez tečky na konci
    t = " ".join(text.strip().split())
    if t.endswith("."):
        t = t[:-1]
    return t.lower()

def unique_key(adj, rod, cislo, pad_idx, noun):
    return (adj, rod, cislo, pad_idx, noun)
    
    
    
# --- generatory uloh  pro model ---    

def generate_adjective_tasks_balanced(adjectives, nouns, num_per_combo: int = 1):
    tasks = []
    seen = set()
    stats = Counter()
    for rod in nouns.keys():
        for podst_jm in nouns[rod].keys():
            for adj in adjectives.keys():
                for cislo in ["sg", "pl"]:
                    for pad_idx in CASE_INDEXES:
                        for _ in range(num_per_combo):
                            try:
                                adj_form = adjectives[adj][rod][cislo][pad_idx]
                                noun_form = nouns[rod][podst_jm][cislo][pad_idx]
                            except KeyError:
                                continue
                            key = unique_key(adj, rod, cislo, pad_idx, podst_jm)
                            if key in seen:
                                continue
                            seen.add(key)

                            prompt = (
                                f"Napiš krátkou větu, ve které použiješ spojení '{adj_form} {noun_form}'. "
                                f"Použij {pad_idx+1}. pád, {cislo} číslo, rod {rod}."
                            )
                            completion = f"Na stole leží {adj_form} {noun_form}."
                            tasks.append({"prompt": prompt, "completion": normalize_completion(completion)})
                            stats[("shoda", pad_idx)] += 1
    return tasks, stats


def generate_adjective_only_prompts(adjectives, nouns, num: int = 300):
    prompts = []
    stats = Counter()
    for _ in range(num):
        rod = random.choice(list(nouns.keys()))
        podst_jm = random.choice(list(nouns[rod].keys()))
        adj = random.choice(list(adjectives.keys()))
        cislo = random.choice(["sg", "pl"])
        pad_idx = random.choice(CASE_INDEXES)
        try:
            adj_form = adjectives[adj][rod][cislo][pad_idx]
        except KeyError:
            continue
        prompt = f"Použij přídavné jméno '{adj_form}' v krátké české větě."
        completion = f"Byl to velmi {adj_form} den."
        prompts.append({"prompt": prompt, "completion": normalize_completion(completion)})
        stats[("adj_only", pad_idx)] += 1
    return prompts, stats


def generate_case_transform_prompts(adjectives, num: int = 300):
    prompts = []
    stats = Counter()
    for _ in range(num):
        adj = random.choice(list(adjectives.keys()))
        rod = random.choice(list(adjectives[adj].keys()))
        cislo = random.choice(["sg", "pl"])
        src_idx, tgt_idx = random.sample(CASE_INDEXES, 2)
        try:
            src_form = adjectives[adj][rod][cislo][src_idx]
            tgt_form = adjectives[adj][rod][cislo][tgt_idx]
        except KeyError:
            continue
        prompt = (
            f"Změň tvar přídavného jména '{src_form}' z {src_idx+1}. pádu "
            f"na {tgt_idx+1}. pád a použij ho ve větě."
        )
        completion = f"Obdivoval {tgt_form} hory."
        prompts.append({"prompt": prompt, "completion": normalize_completion(completion)})
        stats[("transform", tgt_idx)] += 1
    return prompts, stats


def generate_prep_sentence_prompts(adjectives, nouns, num: int = 400):
    out = []
    stats = Counter()
    for _ in range(num):
        rod = random.choice(list(nouns.keys()))
        podst_jm = random.choice(list(nouns[rod].keys()))
        adj = random.choice(list(adjectives.keys()))
        cislo = random.choice(["sg", "pl"])
        pad_idx = random.choice(CASE_INDEXES)
        preps = PREP_BY_CASE.get(pad_idx + 1, [])
        if pad_idx == 4:
            continue
        try:
            adj_form = adjectives[adj][rod][cislo][pad_idx]
            noun_form = nouns[rod][podst_jm][cislo][pad_idx]
        except KeyError:
            continue
        if preps:
            prep = random.choice(preps)
            prompt = (
                f"Napiš větu, která začíná '{prep}' a pokračuje spojením '{adj_form} {noun_form}'."
            )
            completion = f"{prep} {adj_form} {noun_form} se skrýval poklad."
            out.append({"prompt": prompt, "completion": normalize_completion(completion)})
            stats[("prep_ctx", pad_idx)] += 1
    return out, stats


def generate_vocative_prompts(adjectives, nouns, num: int = 150):
    out = []
    stats = Counter()
    pad_idx = 4  # 5. pád
    for _ in range(num):
        rod = random.choice(list(nouns.keys()))
        podst_jm = random.choice(list(nouns[rod].keys()))
        adj = random.choice(list(adjectives.keys()))
        cislo = random.choice(["sg", "pl"])
        try:
            adj_form = adjectives[adj][rod][cislo][pad_idx]
            noun_form = nouns[rod][podst_jm][cislo][pad_idx]
        except KeyError:
            continue
        prompt = f"Vytvoř větu, kde někoho oslovuješ slovy '{adj_form} {noun_form}'."
        completion = f"{adj_form} {noun_form}, pojď sem!"
        out.append({"prompt": prompt, "completion": normalize_completion(completion)})
        stats[("vocative", pad_idx)] += 1
    return out, stats


def generate_ab_choice_prompts(adjectives, nouns, num: int = 200):
    out = []
    stats = Counter()
    for _ in range(num):
        rod = random.choice(list(nouns.keys()))
        podst_jm = random.choice(list(nouns[rod].keys()))
        adj = random.choice(list(adjectives.keys()))
        cislo = random.choice(["sg", "pl"])
        pad_idx = random.choice(CASE_INDEXES)
        try:
            correct_adj = adjectives[adj][rod][cislo][pad_idx]
            correct_noun = nouns[rod][podst_jm][cislo][pad_idx]
        except KeyError:
            continue
        wrong_pad = (pad_idx + random.choice([1, 2, 3])) % 7
        wrong_cislo = "pl" if cislo == "sg" else "sg"
        try:
            wrong_adj_1 = adjectives[adj][rod][cislo][wrong_pad]
            wrong_noun_1 = nouns[rod][podst_jm][cislo][wrong_pad]
            var_a = f"{correct_adj} {correct_noun}"
            var_b = f"{wrong_adj_1} {wrong_noun_1}"
        except KeyError:
            try:
                wrong_adj_2 = adjectives[adj][rod][wrong_cislo][pad_idx]
                wrong_noun_2 = nouns[rod][podst_jm][wrong_cislo][pad_idx]
                var_a = f"{correct_adj} {correct_noun}"
                var_b = f"{wrong_adj_2} {wrong_noun_2}"
            except KeyError:
                continue
        options = [normalize_completion(var_a), normalize_completion(var_b)]
        correct_is = random.choice([0, 1])
        if correct_is == 1:
            options.reverse()
        correct_letter = "A" if correct_is == 0 else "B"
        prompt = (
            f"Vyber správnou shodu přídavného a podstatného jména pro {pad_idx+1}. pád, {cislo} číslo, rod {rod}. "
            f"A: '{options[0]}', B: '{options[1]}'"
        )
        out.append({"prompt": prompt, "completion": correct_letter})
        stats[("choice", pad_idx)] += 1
    return out, stats


def generate_gradation_prompts():
    prompts = []
    stats = Counter()
    gradation_map = {
        "malý": ["menší", "nejmenší"],
        "dobrý": ["lepší", "nejlepší"],
        "špatný": ["horší", "nejhorší"],
        "vysoký": ["vyšší", "nejvyšší"],
        "rychlý": ["rychlejší", "nejrychlejší"]
    }
    for adj, (comp, superl) in gradation_map.items():
        # Druhý stupeň
        prompts.append({
            "prompt": f"Použij druhý stupeň přídavného jména '{adj}' v krátké české větě.",
            "completion": normalize_completion(f"Tento úkol je {comp} než předchozí.")
        })
        stats[("gradation", 2)] += 1

        # Třetí stupeň
        prompts.append({
            "prompt": f"Použij třetí stupeň přídavného jména '{adj}' v krátké české větě.",
            "completion": normalize_completion(f"To je {superl} vrchol v celém pohoří.")
        })
        stats[("gradation", 3)] += 1

    return prompts, stats




# --- Export a reporting ---

def write_jsonl(filename: str, tasks):
    with open(filename, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")

def print_report(stats: Counter):
    total = sum(stats.values())
    print(f"✅ Celkem vygenerováno {total} úloh.")
    by_type = Counter()
    by_case = Counter()
    for (t, p), n in stats.items():
        by_type[t] += n
        if p >= 0:
            by_case[p] += n
    print("— Podle typu:")
    for t, n in by_type.most_common():
        print(f"   {t:>10}: {n}")
    print("— Podle pádu (index 0..6):")
    for p in range(7):
        print(f"   {case_label(p):>7} -> {by_case.get(p, 0)}")

if __name__ == "__main__":
    set_seed(42)

    all_tasks = []
    all_stats = Counter()

    # Shoda adj+subst (vyvážené pokrytí všech kombinací) – pozor, může být velké
    tasks1, stats1 = generate_adjective_tasks_balanced(adjectives, nouns, num_per_combo=1)
    all_tasks += tasks1
    all_stats += stats1

    # Jen adj tvar (kratší odpověď)
    tasks2, stats2 = generate_adjective_only_prompts(adjectives, nouns, num=400)
    all_tasks += tasks2
    all_stats += stats2

    # Transformace mezi pády
    tasks3, stats3 = generate_case_transform_prompts(adjectives, num=400)
    all_tasks += tasks3
    all_stats += stats3

    # Kontext s předložkami (bez vokativu)
    tasks4, stats4 = generate_prep_sentence_prompts(adjectives, nouns, num=600)
    all_tasks += tasks4
    all_stats += stats4

    # Vokativ – explicitní šablona
    tasks5, stats5 = generate_vocative_prompts(adjectives, nouns, num=200)
    all_tasks += tasks5
    all_stats += stats5

    # Výběrové úlohy A/B
    tasks6, stats6 = generate_ab_choice_prompts(adjectives, nouns, num=300)
    all_tasks += tasks6
    all_stats += stats6

    # Stupňování
    tasks7, stats7 = generate_gradation_prompts()
    all_tasks += tasks7
    all_stats += stats7

    # Export
    write_jsonl("Pridavna_jmena.jsonl", all_tasks)
    print_report(all_stats)
