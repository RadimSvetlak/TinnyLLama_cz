# -*- coding: utf-8 -*-
import json
import random
from collections import defaultdict, Counter

# Import necessary structures from the provided files
from tab_nouns import nouns as raw_nouns
from tab_slovesa import verb_conjugations

# ========= Nastavení =========
OUTPUT_FILE = "cz_verb_noun_training.jsonl"
DEBUG = True
SEED = 42

# Jaké typy úloh generovat
INCLUDE_FILL = True
INCLUDE_MCQ = True
INCLUDE_NEGATION = True
INCLUDE_TIME_TRANSFORMS = True
INCLUDE_IMPERATIVE = True

# ========= =========
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RED = "\033[91m"

# ========= Klíče tabulek =========
TENSES = ["přítomný", "minulý", "budoucí"]
NUM_LABELS = [("sg", "j.č."), ("pl", "mn.č.")]  # mapování interních klíčů sg/pl na klíče sloves

# Mapování rodů z tab_nouns.py na klíče rodů v minulém čase v tab_slovesa.py (m, ž, s)
GENDER_MAP = {
    "ž": "ž",
    "s": "s",
    "m_živ": "m",
    "m_nživ": "m",
}

# ========= Pomocné =========
def flatten_strings(x, out):
    if isinstance(x, str):
        out.add(x)
    elif isinstance(x, dict):
        for v in x.values():
            flatten_strings(v, out)
    elif isinstance(x, (list, tuple)):
        for v in x:
            flatten_strings(v, out)

def build_distractor_pool_verbs():
    pool = set()
    for _, forms in verb_conjugations.items():
        flatten_strings(forms, pool)
    return list(pool)

def normalize_nouns(raw):
    out = []
    counts = Counter()
    for g_key, lemmas in raw.items():
        for lemma, forms in lemmas.items():
            try:
                sg_nom = forms["sg"][0]
                pl_nom = forms["pl"][0]
            except (KeyError, IndexError):
                if DEBUG:
                    print(RED + f"❌ Chybí nominativ pro {g_key} -> {lemma}" + RESET)
                continue
            g_val = GENDER_MAP.get(g_key)
            if g_val is None:
                if DEBUG:
                    print(RED + f"❌ Neznámý rod '{g_key}' u {lemma} — přeskočeno" + RESET)
                continue
            out.append({"lemma": lemma, "gender": g_val, "sg": sg_nom, "pl": pl_nom})
            counts[g_val] += 1
    if DEBUG:
        print(GREEN + f"✅ Převod nouns: {len(out)} položek" + RESET)
        print(CYAN + f"   Rozdělení rodů: {dict(counts)}" + RESET)
    return out

def get_3rd_person_form(verb, vforms, tense, num_key, noun_gender):
    if tense not in vforms:
        if DEBUG:
            print(f"[MISS tense] {verb}: '{tense}' není v {list(vforms.keys())}")
        return None

    block = vforms[tense]
    if num_key not in block:
        if DEBUG:
            print(f"[MISS number] {verb} {tense}: '{num_key}' není v {list(block.keys())}")
        return None

    node = block[num_key]

    if tense == "minulý":
        if not isinstance(node, dict):
            if DEBUG:
                print(f"[MISS shape] {verb} {tense} {num_key}: očekáván slovník podle rodu")
            return None
        if noun_gender not in node:
            if DEBUG:
                print(f"[MISS gender] {verb} {tense} {num_key}: '{noun_gender}' není v {list(node.keys())}")
            return None
        persons = node[noun_gender]
        if not isinstance(persons, dict) or 3 not in persons:
            if DEBUG:
                keys = list(persons.keys()) if isinstance(persons, dict) else type(persons)
                print(f"[MISS person] {verb} {tense} {num_key} {noun_gender}: 3. osoba chybí, klíče: {keys}")
            return None
        return persons[3]

    persons = node
    if not isinstance(persons, dict) or 3 not in persons:
        if DEBUG:
            keys = list(persons.keys()) if isinstance(persons, dict) else type(persons)
            print(f"[MISS person] {verb} {tense} {num_key}: 3. osoba chybí, klíče: {keys}")
        return None
    return persons[3]

def get_imperative_form(vforms, num_key, person):
    tense_key = "rozkazovací"
    if tense_key not in vforms:
        return None
    block = vforms[tense_key]
    if num_key not in block:
        return None
    return block[num_key].get(person)

def cz_number_label_short(num_key):
    return num_key

def cz_tense_label(tense):
    return tense

# ========= Šablony úloh =========
def task_form_question(verb, subject, tense, num_key, form):
    return {
        "prompt": f"Jaký je tvar slovesa „{verb}“ pro „{subject}“ ({cz_tense_label(tense)}, 3. os., {cz_number_label_short(num_key)})?",
        "completion": form
    }

def task_fill_sentence(subject, verb, tense, num_key, form):
    return {
        "prompt": f"Doplň tvar slovesa „{verb}“: {subject} ___ ({cz_tense_label(tense)}, {cz_number_label_short(num_key)})",
        "completion": form
    }

def task_mcq(subject, verb, tense, num_key, form, distractors):
    opts = [form]
    pool = [x for x in distractors if x != form]
    if len(pool) >= 2:
        opts += random.sample(pool, 2)
    else:
        opts += pool[:2]
        while len(opts) < 3:
            opts.append(pool[0])  # or add a default distractor
    random.shuffle(opts)
    labels = ["A", "B", "C"]
    choices = " ".join(f"{labels[i]}) {opts[i]}" for i in range(3))
    return {
        "prompt": f"Vyber správný tvar: {subject} ___ ({verb}, {cz_tense_label(tense)}, {cz_number_label_short(num_key)}). {choices}",
        "completion": form
    }

def task_negation(subject, form):
    return {
        "prompt": f"Vytvoř zápor: {subject} {form}",
        "completion": f"{subject} ne{form}"
    }

def task_time_transform(subject, verb, tense_from, tense_to, form_from, form_to, num_key):
    return {
        "prompt": f"Převeď z {cz_tense_label(tense_from)} do {cz_tense_label(tense_to)}: {subject} {form_from} ({cz_number_label_short(num_key)})",
        "completion": f"{subject} {form_to}"
    }

def task_imperative(verb, person, num_key, form):
    return {
        "prompt": f"Jaký je rozkazovací tvar slovesa „{verb}“ (osoba {person}, {num_key})?",
        "completion": form
    }

# ========= Generátor =========
def generate_verb_noun_training_data(
    output_file=OUTPUT_FILE,
    seed=SEED
):
    random.seed(seed)
    rows = []
    stats = defaultdict(int)

    nouns = normalize_nouns(raw_nouns)
    distractor_pool = build_distractor_pool_verbs()

    print(MAGENTA + "🚀 Start generování tréninkových dat..." + RESET)
    print(CYAN + f"ℹ️  Podstatná jména: {len(nouns)}" + RESET)
    print(CYAN + f"ℹ️  Slovesa: {len(verb_conjugations)}" + RESET)

    for v_idx, (verb, vforms) in enumerate(verb_conjugations.items(), start=1):
        if DEBUG:
            print(YELLOW + f"➡️  Sloveso ({v_idx}/{len(verb_conjugations)}): {verb}" + RESET)
            print(CYAN + f"   • Klíče: {list(vforms.keys())}" + RESET)

        # Rozkazovací způsob – jednou za sloveso
        if INCLUDE_IMPERATIVE:
            imp_2_sg = get_imperative_form(vforms, "j.č.", 2)
            imp_2_pl = get_imperative_form(vforms, "mn.č.", 2)
            imp_1_pl = get_imperative_form(vforms, "mn.č.", 1)
            if imp_2_sg:
                rows.append(task_imperative(verb, 2, "j.č.", imp_2_sg)); stats["imperative_2_sg"] += 1
            if imp_2_pl:
                rows.append(task_imperative(verb, 2, "mn.č.", imp_2_pl)); stats["imperative_2_pl"] += 1
            if imp_1_pl:
                rows.append(task_imperative(verb, 1, "mn.č.", imp_1_pl)); stats["imperative_1_pl"] += 1
            if DEBUG and not (imp_2_sg or imp_2_pl or imp_1_pl):
                print("   ⚠️  Rozkazovací způsob nenalezen")

        # 3. osoba pro všechna podstatná jména v časech a číslech
        for tense in TENSES:
            if tense not in vforms:
                if DEBUG:
                    print(f"   [MISS tense] {verb}: chybí '{tense}', k dispozici {list(vforms.keys())}")
                continue

            for noun in nouns:
                for noun_num, num_key in NUM_LABELS:
                    form = get_3rd_person_form(verb, vforms, tense, num_key, noun["gender"])
                    if not form:
                        if DEBUG:
                            node = vforms.get(tense, {}).get(num_key)
                            print(f"   [MISS] {verb} – {tense} – {num_key} | node type={type(node).__name__}")
                        continue

                    subject = noun[noun_num]
                    rows.append(task_form_question(verb, subject, tense, num_key, form)); stats["form_q"] += 1

                    if INCLUDE_FILL:
                        rows.append(task_fill_sentence(subject, verb, tense, num_key, form)); stats["fill"] += 1
                    if INCLUDE_MCQ:
                        rows.append(task_mcq(subject, verb, tense, num_key, form, distractor_pool)); stats["mcq"] += 1
                    if INCLUDE_NEGATION:
                        rows.append(task_negation(subject, form)); stats["negation"] += 1

        # Převody mezi časy (pro stejný podmět, pokud má dostupné min. 2 časy)
        if INCLUDE_TIME_TRANSFORMS:
            for noun in nouns:
                for noun_num, num_key in NUM_LABELS:
                    available = []
                    for t in TENSES:
                        f = get_3rd_person_form(verb, vforms, t, num_key, noun["gender"])
                        if f:
                            available.append((t, f))
                    if len(available) > 1:
                        for i in range(len(available)):
                            for j in range(len(available)):
                                if i == j:
                                    continue
                                t_from, f_from = available[i]
                                t_to, f_to = available[j]
                                rows.append(task_time_transform(noun[noun_num], verb, t_from, t_to, f_from, f_to, num_key))
                                stats["time_transform"] += 1
                    elif DEBUG and available:
                        print(f"   [SKIP transform] {verb} {noun[noun_num]} {num_key}: jen jeden čas → {[(x[0], x[1]) for x in available]}")

    # Uložení
    with open(output_file, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Report
    print(GREEN + f"\n✅ Hotovo! Uloženo {len(rows)} párů do {output_file}" + RESET)
    print(MAGENTA + "   • Počty podle typu:" + RESET)
    for k in sorted(stats.keys()):
        print(f"     - {k}: {stats[k]}")

if __name__ == "__main__":
    generate_verb_noun_training_data()