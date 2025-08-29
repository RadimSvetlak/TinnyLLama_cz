# -*- coding: utf-8 -*-
import json
import random
from tab_zajmena import pronoun_declensions  # Import tables with pronoun declensions

# Pády a otázky
cases = [
    "1. pád", "2. pád", "3. pád", "4. pád", "5. pád", "6. pád", "7. pád"
]
case_names = [
    "nominativ", "genitiv", "dativ", "akuzativ", "vokativ", "lokál", "instrumentál"
]
padove_otazky = [
    "Kdo?", "Koho?", "Komu?", "Koho?", "Oslovení", "O kom?", "S kým?"
]

# Lexical variety and idiomatic/pragmatic sentence starters
sentence_starters_singular = {
    "1. pád": ["Toto je", "Zde stojí", "Tohle je", "Tam sedí", "To je", "Tady leží"],
    "2. pád": ["Bez", "Kvůli", "Vedle", "Uprostřed", "Místo", "Blízko"],
    "3. pád": ["K", "Díky", "Proti", "Kvůli", "Napříč", "O směrem k"],
    "4. pád": ["Vidím", "Potřebuji", "Hledám", "Mám rád", "Čekám na", "Ztratil jsem"],
    "5. pád": ["Hej,", "Vážení,", "Přátelé,", "Ty,", "Pane,", "Slečno,"],
    "6. pád": ["O", "Na", "V", "Při", "Po", "Během"],
    "7. pád": ["S", "Spolu s", "Před", "Za", "Mezi", "Nad"]
}
sentence_starters_plural = {
    "1. pád": ["Toto jsou", "Zde stojí", "Tohle jsou", "Tam sedí", "To jsou", "Ti tam jsou"],
    "2. pád": ["Bez", "Kvůli", "Vedle", "Uprostřed", "Místo", "Blízko"],
    "3. pád": ["K", "Díky", "Proti", "Kvůli", "Napříč", "O směrem k"],
    "4. pád": ["Vidím", "Potřebuji", "Hledám", "Mám rád", "Čekám na", "Ztratil jsem"],
    "5. pád": ["Hej,", "Vážení,", "Přátelé,", "Vy,", "Drazí,", "Vážené dámy,"],
    "6. pád": ["O", "Na", "V", "Při", "Po", "Během"],
    "7. pád": ["S", "Spolu s", "Před", "Za", "Mezi", "Nad"]
}

def build_distractor_pool():
    pool = set()
    for pdata in pronoun_declensions.values():
        for form in pdata.get("singular", []):
            if form and form != "-":
                pool.add(form)
        for form in pdata.get("plural", []):
            if form and form != "-":
                pool.add(form)
        if pdata.get("plural_base"):
            pool.add(pdata["plural_base"])
        poss = pdata.get("possessive")
        if poss:
            pool.add(poss.get("singular", ""))
            pool.add(poss.get("plural", ""))
    return [p for p in pool if p and p != "-"]

def labeled_mc_row(lemma, case_label, extra_desc, correct, distractor_pool):
    """Create multiple-choice question with A/B/C options and context."""
    candidates = [x for x in distractor_pool if x != correct]
    if len(candidates) < 2:
        return None
    distractors = random.sample(candidates, 2)
    options = [correct] + distractors
    random.shuffle(options)
    labels = ["A", "B", "C"]
    labeled_opts = [f"{labels[i]} {options[i]}" for i in range(3)]
    desc = f" v {case_label}u "
    if extra_desc:
        desc += f" ({extra_desc})"
    prompt = f"Vyber zájmeno '{lemma}'{desc}: " + " ".join(labeled_opts)
    return {"prompt": prompt, "completion": correct}

def task_negation(pronoun, form, case_label):
    """Add tasks involving negation."""
    return {
        "prompt": f"Neguj větu: Ne {form} (zájmeno '{pronoun}', {case_label})",
        "completion": f"Ne {form}"
    }

def task_questions(pronoun, form, question):
    """Add tasks involving questions."""
    return {
        "prompt": f"Zodpovězte otázku '{question}' s použitím zájmena '{pronoun}': Jaký tvar?",
        "completion": form
    }

def generate_extended_prompts():
    output_file = "train_zajmena.jsonl"
    rows = []
    distractor_pool = build_distractor_pool()

    for pronoun, data in pronoun_declensions.items():
        singular = data["singular"]
        plural = data["plural"]
        plural_base = data["plural_base"]

        # Pluralization prompts
        rows.append({"prompt": f"Množné číslo od zájmena „{pronoun}“:", "completion": plural_base})
        rows.append({"prompt": f"Jaký je tvar zájmena „{pronoun}“ v množném čísle?", "completion": plural_base})

        # Possessive pronoun mapping
        if "possessive" in data:
            poss_sg = data["possessive"]["singular"]
            poss_pl = data["possessive"]["plural"]
            rows.append({"prompt": f"Jaké přivlastňovací zájmeno odpovídá osobnímu zájmenu „{pronoun}“ v jednotném čísle?", "completion": poss_sg})
            rows.append({"prompt": f"Jaké přivlastňovací zájmeno odpovídá osobnímu zájmenu „{pronoun}“ v množném čísle?", "completion": poss_pl})
            rows.append({"prompt": f"Zájmeno „{pronoun}“ souvisí s přivlastňovacím zájmenem:", "completion": f"{poss_sg} / {poss_pl}"})

        for i in range(7):
            case_label = cases[i]
            case_name = case_names[i]
            question = padove_otazky[i]

            # Singular
            if singular[i] != "-":
                rows.extend([
                    {"prompt": f"Jaký je {case_label} ({case_name}) jednotného čísla zájmena „{pronoun}“?", "completion": singular[i]},
                    {"prompt": f"Na otázku „{question}“ odpovídá u zájmena „{pronoun}“ tvar:", "completion": singular[i]},
                    {"prompt": f"Doplň správný tvar: {random.choice(sentence_starters_singular[case_label])} ___ (zájmeno „{pronoun}“, {case_label})", "completion": singular[i]},
                    task_negation(pronoun, singular[i], case_label),
                    task_questions(pronoun, singular[i], question)
                ])

                # Case conversion – singular
                for j in range(7):
                    if i != j and singular[j] != "-":
                        rows.append({
                            "prompt": f"Převeď zájmeno „{singular[i]}“ z {cases[i]}u do {cases[j]}u:",
                            "completion": singular[j]
                        })

                other_opts = [form for form in singular if form != "-" and form != singular[i]]
                if len(other_opts) >= 2:
                    opts = random.sample(other_opts, 2) + [singular[i]]
                    random.shuffle(opts)
                    rows.append({"prompt": f"Vyber správný tvar zájmena „{pronoun}“ ve {case_label}: {opts}", "completion": singular[i]})

                # MC with labeled A/B/C and context
                extra_desc = ""
                if pronoun in ["můj", "tvůj", "náš", "váš", "svůj"]:
                    extra_desc = "přivlastňovací tvar"
                mc = labeled_mc_row(pronoun, case_label, extra_desc, singular[i], distractor_pool)
                if mc:
                    rows.append(mc)

            # Plural
            if plural[i] != "-":
                rows.extend([
                    {"prompt": f"Jaký je {case_label} ({case_name}) množného čísla zájmena „{pronoun}“?", "completion": plural[i]},
                    {"prompt": f"Na otázku „{question}“ odpovídá u zájmena „{plural_base}“ tvar:", "completion": plural[i]},
                    {"prompt": f"Doplň správný tvar: {random.choice(sentence_starters_plural[case_label])} ___ (zájmeno „{plural_base}“, {case_label})", "completion": plural[i]},
                    task_negation(plural_base, plural[i], case_label),
                    task_questions(plural_base, plural[i], question)
                ])

                # MC with labeled A/B/C and context
                extra_desc = ""
                if pronoun in ["můj", "tvůj", "náš", "váš", "svůj"]:
                    extra_desc = "přivlastňovací tvar"
                mc_pl = labeled_mc_row(pronoun, case_label, extra_desc, plural[i], distractor_pool)
                if mc_pl:
                    rows.append(mc_pl)

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"✅ Hotovo: {len(rows)} řádků uloženo do {output_file}")

# Run
if __name__ == "__main__":
    generate_extended_prompts()