# -*- coding: utf-8 -*-
import json
import random
from tab_slovesa import verb_conjugations
from tab_nouns import nouns

# ANSI barvy
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

sentence_starters_verbs = [
    "Každé ráno", "Právě teď", "Zítra odpoledne", "Včera večer", "Občas", "Rychle"
]
sentence_starters_nouns = [
    "Vidím", "Potřebuji", "Mluvím o", "Jdu s", "Stojím u"
]

cases = ["1. pád", "2. pád", "3. pád", "4. pád", "5. pád", "6. pád", "7. pád"]

def build_distractor_pool_verbs():
    print(CYAN + "🔹 Buduji seznam distraktorů pro slovesa..." + RESET)
    pool = set()
    for forms in verb_conjugations.values():
        for tense_forms in forms.values():
            for num_forms in tense_forms.values():
                if isinstance(num_forms, dict):
                    for val in num_forms.values():
                        if isinstance(val, str):
                            pool.add(val)
                        elif isinstance(val, dict):
                            pool.update(val.values())
    print(GREEN + f"   ✅ Distraktorů pro slovesa: {len(pool)}" + RESET)
    return list(pool)

def build_distractor_pool_nouns():
    print(CYAN + "🔹 Buduji seznam distraktorů pro podstatná jména..." + RESET)
    pool = set()
    for gender_dict in nouns.values():
        for forms in gender_dict.values():
            for num_forms in forms.values():
                pool.update(num_forms)
    print(GREEN + f"   ✅ Distraktorů pro podstatná jména: {len(pool)}" + RESET)
    return list(pool)

# ====== Funkce pro slovesa ======

def create_form_question_verb(verb, tense, number, person, form):
    return {"prompt": f"Jaký je tvar slovesa „{verb}“ v {person}. osobě {number} čísla {tense} času?",
            "completion": form}

def create_fill_sentence_verb(verb, tense, number, person, form):
    starter = random.choice(sentence_starters_verbs)
    return {"prompt": f"Doplň správný tvar slovesa „{verb}“ ({person}. os., {number} č., {tense} čas) do věty: {starter} ___ .",
            "completion": form}

def create_mc_task_verb(verb, tense, number, person, form, distractor_pool):
    distractors = random.sample([x for x in distractor_pool if x != form], k=2)
    options = distractors + [form]
    random.shuffle(options)
    labels = ["A", "B", "C"]
    labeled_opts = [f"{labels[i]} {options[i]}" for i in range(3)]
    return {"prompt": f"Vyber správný tvar slovesa „{verb}“ ({person}. os., {number} č., {tense} čas): " + " ".join(labeled_opts),
            "completion": form}

# ====== Funkce pro podstatná jména ======

def create_form_question_noun(noun, case_idx, form, number):
    return {"prompt": f"Jaký je {cases[case_idx]} {number} čísla podstatného jména „{noun}“?",
            "completion": form}

def create_fill_sentence_noun(noun, case_idx, form):
    starter = random.choice(sentence_starters_nouns)
    return {"prompt": f"Doplň správný tvar podstatného jména „{noun}“ ({cases[case_idx]}): {starter} ___ .",
            "completion": form}

def create_mc_task_noun(noun, case_idx, form, distractor_pool):
    distractors = random.sample([x for x in distractor_pool if x != form], k=2)
    options = distractors + [form]
    random.shuffle(options)
    labels = ["A", "B", "C"]
    labeled_opts = [f"{labels[i]} {options[i]}" for i in range(3)]
    return {"prompt": f"Vyber správný tvar podstatného jména „{noun}“ ({cases[case_idx]}): " + " ".join(labeled_opts),
            "completion": form}

# ====== Hlavní generátor ======

def generate_training_data():
    print(MAGENTA + "🚀 Start generování trénovacích dat..." + RESET)
    rows = []

    # --- Slovesa ---
    print(YELLOW + "=== Zpracovávám slovesa ===" + RESET)
    verb_distractors = build_distractor_pool_verbs()

    for idx, (verb, tenses) in enumerate(verb_conjugations.items(), start=1):
        print(f"➡️  ({idx}/{len(verb_conjugations)}) Sloveso: {verb}")
        for tense, numbers in tenses.items():
            for number, persons in numbers.items():
                if not isinstance(persons, dict):
                    continue
                for person, form in persons.items():
                    if isinstance(form, dict):
                        for gender, g_form in form.items():
                            rows.append(create_form_question_verb(verb, tense, number, f"{person} ({gender})", g_form))
                            rows.append(create_fill_sentence_verb(verb, tense, number, f"{person} ({gender})", g_form))
                            rows.append(create_mc_task_verb(verb, tense, number, f"{person} ({gender})", g_form, verb_distractors))
                    elif isinstance(form, str):
                        rows.append(create_form_question_verb(verb, tense, number, person, form))
                        rows.append(create_fill_sentence_verb(verb, tense, number, person, form))
                        rows.append(create_mc_task_verb(verb, tense, number, person, form, verb_distractors))

    # --- Podstatná jména ---
    print(YELLOW + "=== Zpracovávám podstatná jména ===" + RESET)
    noun_distractors = build_distractor_pool_nouns()

    for gender, words in nouns.items():
        for idx, (noun, forms) in enumerate(words.items(), start=1):
            print(f"➡️  ({idx}/{len(words)}) Podstatné jméno: {noun}")
            for num_label, forms_list in forms.items():
                for case_idx, form in enumerate(forms_list):
                    if form != "-":
                        rows.append(create_form_question_noun(noun, case_idx, form, "jednotného" if num_label == "sg" else "množného"))
                        rows.append(create_fill_sentence_noun(noun, case_idx, form))
                        rows.append(create_mc_task_noun(noun, case_idx, form, noun_distractors))

    # --- Zápis do souboru ---
    output_file = "train_slovesa_nouns.jsonl"
    print(MAGENTA + f"💾 Ukládám {len(rows)} řádků do souboru: {output_file}" + RESET)
    with open(output_file, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(GREEN + "✅ Generování dokončeno!" + RESET)

if __name__ == "__main__":
    generate_training_data()