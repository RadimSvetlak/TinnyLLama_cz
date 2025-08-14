# ------------------------------------------------------------
# Název: Generátor rozšířených tréninkových promptů pro česká zájmena
# Popis:
#   Tento skript vytváří JSONL soubor s tréninkovými dvojicemi prompt–completion
#   pro procvičování a učení správného skloňování českých zájmen v jednotném
#   i množném čísle, včetně přivlastňovacích tvarů.
#
#   Obsahuje:
#     - Seznam pádů, jejich názvů a odpovídajících pádových otázek.
#     - Slovníky se zájmeny a jejich tvary pro jednotné a množné číslo
#       (včetně přivlastňovacích zájmen).
#     - Sady náhodných začátků vět (sentence starters) pro tvorbu
#       doplňovacích úloh v každém pádě.
#     - Funkci generate_extended_prompts, která:
#         1) Generuje úlohy na určení množného čísla od zájmena.
#         2) Generuje úlohy na přiřazení přivlastňovacích zájmen.
#         3) Pro každý pád tvoří:
#              - otázky na určení správného tvaru,
#              - pádové otázky ("Kdo?", "Koho?" atd.),
#              - doplňovací věty se správným tvarem,
#              - převody mezi pády,
#              - výběrové otázky z několika možností.
#         4) Vše ukládá do souboru ve formátu JSON Lines.
#
# Vstup:
#   - Slovník pronoun_declensions se zájmeny a jejich tvary.
#   - Definice pádů, názvů pádů, pádových otázek a náhodných začátků vět.
#
# Výstup:
#   - Soubor "rozsirene_zajmena_prompty.jsonl" s řádky typu:
#       {"prompt": "...", "completion": "..."}
#
# Závislosti:
#   - Python 3.8+
#   - modul random (součást standardní knihovny)
#
# ------------------------------------------------------------

import json
import random

# Pády
cases = [
    "1. pád", "2. pád", "3. pád", "4. pád", "5. pád", "6. pád", "7. pád"
]
case_names = [
    "nominativ", "genitiv", "dativ", "akuzativ", "vokativ", "lokál", "instrumentál"
]
padove_otazky = [
    "Kdo?", "Koho?", "Komu?", "Koho?", "Oslovení", "O kom?", "S kým?"
]
sentence_starters_singular = {
    "1. pád": ["Toto je", "Zde stojí", "Tohle je", "Tam sedí", "To je"],
    "2. pád": ["Bez", "Kvůli", "Vedle", "Uprostřed", "Místo"],
    "3. pád": ["K", "Díky", "Proti", "Kvůli", "Napříč"],
    "4. pád": ["Vidím", "Potřebuji", "Hledám", "Mám rád", "Čekám na"],
    "5. pád": ["Hej,", "Vážení,", "Přátelé,", "Ty,", "Pane,"],
    "6. pád": ["O", "Na", "V", "Při", "Po"],
    "7. pád": ["S", "Spolu s", "Před", "Za", "Mezi"]
}

sentence_starters_plural = {
    "1. pád": ["Toto jsou", "Zde stojí", "Tohle jsou", "Tam sedí", "To jsou"],
    "2. pád": ["Bez", "Kvůli", "Vedle", "Uprostřed", "Místo"],
    "3. pád": ["K", "Díky", "Proti", "Kvůli", "Napříč"],
    "4. pád": ["Vidím", "Potřebuji", "Hledám", "Mám rád", "Čekám na"],
    "5. pád": ["Hej,", "Vážení,", "Přátelé,", "Vy,", "Drazí,"],
    "6. pád": ["O", "Na", "V", "Při", "Po"],
    "7. pád": ["S", "Spolu s", "Před", "Za", "Mezi"]
}


# Zájmena
pronoun_declensions = {
    "já": {
        "singular": ["já", "mě", "mně", "mě", "já", "mně", "mnou"],
        "plural_base": "my",
        "plural": ["my", "nás", "nám", "nás", "my", "nás", "námi"],
        "possessive": {
            "singular": "můj",
            "plural": "náš"
        }
    },
    "ty": {
        "singular": ["ty", "tebe", "tobě", "tebe", "ty", "tobě", "tebou"],
        "plural_base": "vy",
        "plural": ["vy", "vás", "vám", "vás", "vy", "vás", "vámi"],
        "possessive": {
            "singular": "tvůj",
            "plural": "váš"
        }
    },
    "on": {
        "singular": ["on", "ho", "jemu", "ho", "on", "něm", "ním"],
        "plural_base": "oni",
        "plural": ["oni", "jich", "jim", "je", "oni", "nich", "nimi"],
        "possessive": {
            "singular": "jeho",
            "plural": "jejich"
        }
    },
    "ona": {
        "singular": ["ona", "ji", "jí", "ji", "ona", "ní", "ní"],
        "plural_base": "ony",
        "plural": ["ony", "jich", "jim", "je", "ony", "nich", "nimi"],
        "possessive": {
            "singular": "její",
            "plural": "jejich"
        }
    },
    "ono": {
        "singular": ["ono", "ho", "jemu", "ho", "ono", "něm", "ním"],
        "plural_base": "ona",
        "plural": ["ona", "jich", "jim", "je", "ona", "nich", "nimi"],
        "possessive": {
            "singular": "jeho",
            "plural": "jejich"
        }
    },
    "my": {
        "singular": ["-", "-", "-", "-", "-", "-", "-"],
        "plural_base": "my",
        "plural": ["my", "nás", "nám", "nás", "my", "nás", "námi"],
        "possessive": {
            "singular": "můj",
            "plural": "náš"
        }
    },
    "vy": {
        "singular": ["-", "-", "-", "-", "-", "-", "-"],
        "plural_base": "vy",
        "plural": ["vy", "vás", "vám", "vás", "vy", "vás", "vámi"],
        "possessive": {
            "singular": "tvůj",
            "plural": "váš"
        }
    },
    "oni": {
        "singular": ["-", "-", "-", "-", "-", "-", "-"],
        "plural_base": "oni",
        "plural": ["oni", "jich", "jim", "je", "oni", "nich", "nimi"],
        "possessive": {
            "singular": "jeho",
            "plural": "jejich"
        }
    },
    "můj": {
        "singular": ["můj", "mého", "mému", "mého", "můj", "mém", "mým"],
        "plural_base": "moji",
        "plural": ["moji", "mých", "mým", "moje", "moji", "mých", "mými"]
    },
    "tvůj": {
        "singular": ["tvůj", "tvého", "tvému", "tvého", "tvůj", "tvém", "tvým"],
        "plural_base": "tvoji",
        "plural": ["tvoji", "tvých", "tvým", "tvoje", "tvoji", "tvých", "tvými"]
    },
    "náš": {
        "singular": ["náš", "našeho", "našemu", "našeho", "náš", "našem", "naším"],
        "plural_base": "naši",
        "plural": ["naši", "našich", "našim", "naše", "naši", "našich", "našimi"]
    },
    "váš": {
        "singular": ["váš", "vašeho", "vašemu", "vašeho", "váš", "vašem", "vaším"],
        "plural_base": "vaši",
        "plural": ["vaši", "vašich", "vašim", "vaše", "vaši", "vašich", "vašimi"]
    },
    "její": {
        "singular": ["její", "její", "její", "její", "její", "její", "její"],
        "plural_base": "její",
        "plural": ["její", "jejích", "jejím", "její", "její", "jejích", "jejími"]
    },
    "jejich": {
        "singular": ["jejich", "jejich", "jejich", "jejich", "jejich", "jejich", "jejich"],
        "plural_base": "jejich",
        "plural": ["jejich", "jejich", "jejich", "jejich", "jejich", "jejich", "jejich"]
    }
}


def generate_extended_prompts():
    output_file = "rozsirene_zajmena_prompty.jsonl"

    sentence_starters_singular = {
        "1. pád": ["Kdo?", "Co?", "Viděl to kdo?", "Řekl to kdo?", "Koupil to kdo?"],
        "2. pád": ["Bez", "Kvůli", "Vedle", "Uprostřed", "Místo"],
        "3. pád": ["K", "Díky", "Proti", "Kvůli", "Napříč"],
        "4. pád": ["Vidím", "Potřebuji", "Hledám", "Mám rád", "Čekám na"],
        "5. pád": ["Hej,", "Vážení,", "Přátelé,", "Ty,", "Pane,"],
        "6. pád": ["O", "Na", "V", "Při", "Po"],
        "7. pád": ["S", "Spolu s", "Před", "Za", "Mezi"]
    }

    sentence_starters_plural = {
        "1. pád": ["Kdo?", "Co?", "Viděl to kdo?", "Řekl to kdo?", "Koupil to kdo?"],
        "2. pád": ["Bez", "Kvůli", "Vedle", "Uprostřed", "Místo"],
        "3. pád": ["K", "Díky", "Proti", "Kvůli", "Napříč"],
        "4. pád": ["Vidím", "Potřebuji", "Hledám", "Mám rád", "Čekám na"],
        "5. pád": ["Hej,", "Vážení,", "Přátelé,", "Vy,", "Drazí,"],
        "6. pád": ["O", "Na", "V", "Při", "Po"],
        "7. pád": ["S", "Spolu s", "Před", "Za", "Mezi"]
    }

    with open(output_file, "w", encoding="utf-8") as f:
        for pronoun, data in pronoun_declensions.items():
            singular = data["singular"]
            plural = data["plural"]
            plural_base = data["plural_base"]

            # Množné číslo od zájmena
            f.write(json.dumps({
                "prompt": f"Množné číslo od zájmena '{pronoun}':",
                "completion": plural_base
            }, ensure_ascii=False) + "\n")

            # Převod mezi čísly
            f.write(json.dumps({
                "prompt": f"Jaký je tvar zájmena '{pronoun}' v množném čísle?",
                "completion": plural_base
            }, ensure_ascii=False) + "\n")

            # Připojení přivlastňovacího zájmena (pokud existuje)
            if "possessive" in data:
                possessive_sg = data["possessive"]["singular"]
                possessive_pl = data["possessive"]["plural"]

                f.write(json.dumps({
                    "prompt": f"Jaké přivlastňovací zájmeno odpovídá osobnímu zájmenu '{pronoun}' v jednotném čísle?",
                    "completion": possessive_sg
                }, ensure_ascii=False) + "\n")

                f.write(json.dumps({
                    "prompt": f"Jaké přivlastňovací zájmeno odpovídá osobnímu zájmenu '{pronoun}' v množném čísle?",
                    "completion": possessive_pl
                }, ensure_ascii=False) + "\n")

                f.write(json.dumps({
                    "prompt": f"Zájmeno '{pronoun}' souvisí s přivlastňovacím zájmenem:",
                    "completion": f"{possessive_sg} / {possessive_pl}"
                }, ensure_ascii=False) + "\n")

            for i in range(7):
                case_label = cases[i]
                case_name = case_names[i]
                question = padove_otazky[i]

                # Jednotné číslo
                if singular[i] != "-":
                    f.write(json.dumps({
                        "prompt": f"Jaký je {case_label} ({case_name}) jednotného čísla zájmena '{pronoun}'?",
                        "completion": singular[i]
                    }, ensure_ascii=False) + "\n")

                    f.write(json.dumps({
                        "prompt": f"Na otázku '{question}' odpovídá u zájmena '{pronoun}' tvar:",
                        "completion": singular[i]
                    }, ensure_ascii=False) + "\n")

                    starter = random.choice(sentence_starters_singular[case_label])
                    f.write(json.dumps({
                        "prompt": f"Doplň správný tvar: {starter} ___ (zájmeno '{pronoun}', {case_label})",
                        "completion": singular[i]
                    }, ensure_ascii=False) + "\n")

                # Množné číslo
                if plural[i] != "-":
                    f.write(json.dumps({
                        "prompt": f"Jaký je {case_label} ({case_name}) množného čísla zájmena '{pronoun}'?",
                        "completion": plural[i]
                    }, ensure_ascii=False) + "\n")

                    f.write(json.dumps({
                        "prompt": f"Na otázku '{question}' odpovídá u zájmena '{plural_base}' tvar:",
                        "completion": plural[i]
                    }, ensure_ascii=False) + "\n")

                    starter = random.choice(sentence_starters_plural[case_label])
                    f.write(json.dumps({
                        "prompt": f"Doplň správný tvar: {starter} ___ (zájmeno '{plural_base}', {case_label})",
                        "completion": plural[i]
                    }, ensure_ascii=False) + "\n")

                # Převod mezi pády – jednotné číslo
                for j in range(7):
                    if i != j and singular[i] != "-" and singular[j] != "-":
                        f.write(json.dumps({
                            "prompt": f"Převeď zájmeno '{pronoun}' z {cases[i]}u do {cases[j]}u:",
                            "completion": singular[j]
                        }, ensure_ascii=False) + "\n")

                # Výběr z možností – jednotné číslo
                if singular[i] != "-":
                    try:
                        options = random.sample([form for form in singular if form != "-" and form != singular[i]], k=2)
                        options.append(singular[i])
                        random.shuffle(options)
                        f.write(json.dumps({
                            "prompt": f"Vyber správný tvar zájmena '{pronoun}' ve {case_label}: {options}",
                            "completion": singular[i]
                        }, ensure_ascii=False) + "\n")
                    except:
                        print("nelze vytvořit pár, přeskakuji")
                        
                        
    print(f"\n✅ Hotovo: výstup uložen do souboru {output_file}")
# Spuštění
generate_extended_prompts()
