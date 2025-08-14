# -*- coding: utf-8 -*-

# Tabulka tvarů zájmen: osobní + přivlastňovací + zvratné + zvratné přivlastňovací
# Každé zájmeno má tvary pro jednotné a množné číslo (7 pádů),
# základ pro množné číslo, a případně odpovídající přivlastňovací zájmena.

pronoun_declensions = {
    # Osobní
    "já": {
        "singular": ["já", "mě", "mně", "mě", "já", "mně", "mnou"],
        "plural_base": "my",
        "plural": ["my", "nás", "nám", "nás", "my", "nás", "námi"],
        "possessive": {"singular": "můj", "plural": "náš"}
    },
    "ty": {
        "singular": ["ty", "tebe", "tobě", "tebe", "ty", "tobě", "tebou"],
        "plural_base": "vy",
        "plural": ["vy", "vás", "vám", "vás", "vy", "vás", "vámi"],
        "possessive": {"singular": "tvůj", "plural": "váš"}
    },
    "on": {
        "singular": ["on", "ho", "jemu", "ho", "on", "něm", "ním"],
        "plural_base": "oni",
        "plural": ["oni", "jich", "jim", "je", "oni", "nich", "nimi"],
        "possessive": {"singular": "jeho", "plural": "jejich"}
    },
    "ona": {
        "singular": ["ona", "jí", "jí", "ji", "ono", "ní", "ní"],
        "plural_base": "ony",
        "plural": ["ony", "jich", "jim", "je", "ony", "nich", "nimi"],
        "possessive": {"singular": "její", "plural": "jejich"}
    },
    "ono": {
        "singular": ["ono", "ho", "jemu", "ho", "ono", "něm", "ním"],
        "plural_base": "ona",
        "plural": ["ona", "jich", "jim", "je", "ona", "nich", "nimi"],
        "possessive": {"singular": "jeho", "plural": "jejich"}
    },

    # Přivlastňovací
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

    # Zvratné
    "se": {
        "singular": ["se", "sebe", "sobě", "sebe", "-", "sobě", "sebou"],
        "plural_base": "se",
        "plural": ["se", "sebe", "sobě", "sebe", "-", "sobě", "sebou"]
    },

    # Zvratné přivlastňovací
    "svůj": {
        "singular": ["svůj", "svého", "svému", "svého", "svůj", "svém", "svým"],
        "plural_base": "svoji",
        "plural": ["svoji", "svých", "svým", "svoje", "svoji", "svých", "svými"]
    }
}