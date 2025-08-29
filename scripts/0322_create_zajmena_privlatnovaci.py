import json
import random
from tab_zajmena_ext import pronoun_declensions
from tab_nouns import nouns

cases = [
    "1. pád", "2. pád", "3. pád", "4. pád", "5. pád", "6. pád", "7. pád"
]

human_templates = {
    0: ["___ leží na stole.", "Jak bys řekl, že {lemma} patří mně?"],
    1: ["Bez ___ se neobejdu.", "Bojím se ___ ."],
    2: ["Podal jsem to ___ ."],
    3: ["Čtu ___ každý den."],
    4: ["___ , pojď sem!"],
    5: ["Mluvím o ___ ."],
    6: ["Jdu s ___ ."]
}

def ensure_forms(forms, fill="-"):
    if isinstance(forms, list):
        return (forms + [fill] * 7)[:7]
    elif isinstance(forms, str):
        return [forms] * 7
    else:
        return [fill] * 7
def generate_noun_possession_tasks():
    output_file = "generated_noun_possession_tasks.jsonl"
    rows = []

    for gender, noun_set in nouns.items():
        for noun, noun_forms in noun_set.items():
            noun_sg_forms = noun_forms["sg"]
            noun_pl_forms = noun_forms["pl"]

            for pronoun, data in pronoun_declensions.items():
                if "possessive" not in data:
                    continue

                singular_possessive_base = data["possessive"]["singular"]
                plural_possessive_base = data["possessive"]["plural"]

                if singular_possessive_base in pronoun_declensions:
                    possessive_sg_forms = ensure_forms(
                        pronoun_declensions[singular_possessive_base]
                        .get("singular", {})
                        .get(gender, [])
                    )
                    possessive_pl_forms = ensure_forms(
                        pronoun_declensions[plural_possessive_base]
                        .get("plural", {})
                        .get(gender, [])
                    )
                else:
                    possessive_sg_forms = ensure_forms(singular_possessive_base)
                    possessive_pl_forms = ensure_forms(plural_possessive_base)

                for i in range(7):
                    use_human = random.random() < 0.3  # 30% lidské věty

                    # ---- Singulár ----
                    if noun_sg_forms[i] != "-":
                        if use_human and i in human_templates:
                            template = random.choice(human_templates[i])
                            base_pronoun = singular_possessive_base
                            prompt_sg = (
                                f"doplnit ({base_pronoun}, {noun_sg_forms[0]}) ve {cases[i]}: "
                                + template.replace("{lemma}", noun_sg_forms[0])
                            )
                            completion_sg = template.replace(
                                "___",
                                f"{possessive_sg_forms[i]} {noun_sg_forms[i]}"
                            ).replace("{lemma}", noun_sg_forms[0])
                        else:
                            prompt_sg = (
                                f"Napiš přivlastňovací zájmeno pro '{noun_sg_forms[0]}' "
                                f"v {cases[i]}: {possessive_sg_forms[i]} ___"
                            )
                            completion_sg = f"{possessive_sg_forms[i]} {noun_sg_forms[i]}"
                        rows.append({"prompt": prompt_sg, "completion": completion_sg})

                    # ---- Plurál ----
                    if noun_pl_forms[i] != "-":
                        if use_human and i in human_templates:
                            template = random.choice(human_templates[i])
                            base_pronoun = plural_possessive_base
                            prompt_pl = (
                                f"doplnit ({base_pronoun}, {noun_pl_forms[0]}) ve {cases[i]}: "
                                + template.replace("{lemma}", noun_pl_forms[0])
                            )
                            completion_pl = template.replace(
                                "___",
                                f"{possessive_pl_forms[i]} {noun_pl_forms[i]}"
                            ).replace("{lemma}", noun_pl_forms[0])
                        else:
                            prompt_pl = (
                                f"Napiš přivlastňovací zájmeno pro '{noun_pl_forms[0]}' "
                                f"v {cases[i]}: {possessive_pl_forms[i]} ___"
                            )
                            completion_pl = f"{possessive_pl_forms[i]} {noun_pl_forms[i]}"
                        rows.append({"prompt": prompt_pl, "completion": completion_pl})

    with open(output_file, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"✅ Hotovo: {len(rows)} řádků uloženo do {output_file}")
if __name__ == "__main__":
    generate_noun_possession_tasks()