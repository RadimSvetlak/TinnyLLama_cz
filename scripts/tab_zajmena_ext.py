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

    # Přivlastňovací with gender specifics
    "můj": {
        "singular": {
            "m_živ": ["můj", "mého", "mému", "mého", "můj", "mém", "mým"],
            "m_než": ["můj", "mého", "mému", "můj", "můj", "mém", "mým"],
            "ž": ["moje", "mojí", "mojí", "moji", "moje", "mojí", "mojí"],
            "s": ["moje", "mého", "mému", "moje", "moje", "mém", "mým"]
        },
        "plural": {
            "m_živ": ["moji", "mých", "mým", "moje", "moji", "mých", "mými"],
            "m_než": ["moje", "mých", "mým", "moje", "moje", "mých", "mými"],
            "ž": ["moje", "mých", "mým", "moje", "moje", "mých", "mými"],
            "s": ["moje", "mých", "mým", "moje", "moje", "mých", "mými"]
        }
    },
    "tvůj": {
        "singular": {
            "m_živ": ["tvůj", "tvého", "tvému", "tvého", "tvůj", "tvém", "tvým"],
            "m_než": ["tvůj", "tvého", "tvému", "tvůj", "tvůj", "tvém", "tvým"],
            "ž": ["tvoje", "tvojí", "tvojí", "tvoji", "tvoje", "tvojí", "tvojí"],
            "s": ["tvoje", "tvého", "tvému", "tvoje", "tvoje", "tvém", "tvým"]
        },
        "plural": {
            "m_živ": ["tvoji", "tvých", "tvým", "tvoje", "tvoji", "tvých", "tvými"],
            "m_než": ["tvoje", "tvých", "tvým", "tvoje", "tvoje", "tvých", "tvými"],
            "ž": ["tvoje", "tvých", "tvým", "tvoje", "tvoje", "tvých", "tvými"],
            "s": ["tvoje", "tvých", "tvým", "tvoje", "tvoje", "tvých", "tvými"]
        }
    },
    "náš": {
        "singular": {
            "m_živ": ["náš", "našeho", "našemu", "našeho", "náš", "našem", "naším"],
            "m_než": ["náš", "našeho", "našemu", "náš", "náš", "našem", "naším"],
            "ž": ["naše", "naší", "naší", "naši", "naše", "naší", "naší"],
            "s": ["naše", "našeho", "našemu", "naše", "naše", "našem", "naším"]
        },
        "plural": {
            "m_živ": ["naši", "našich", "našim", "naše", "naši", "našich", "našimi"],
            "m_než": ["naše", "našich", "našim", "naše", "naše", "našich", "našimi"],
            "ž": ["naše", "našich", "našim", "naše", "naše", "našich", "našimi"],
            "s": ["naše", "našich", "našim", "naše", "naše", "našich", "našimi"]
        }
    },
    "váš": {
        "singular": {
            "m_živ": ["váš", "vašeho", "vašemu", "vašeho", "váš", "vašem", "vaším"],
            "m_než": ["váš", "vašeho", "vašemu", "váš", "váš", "vašem", "vaším"],
            "ž": ["vaše", "vaší", "vaší", "vaši", "vaše", "vaší", "vaší"],
            "s": ["vaše", "vašeho", "vašemu", "vaše", "vaše", "vašem", "vaším"]
        },
        "plural": {
            "m_živ": ["vaši", "vašich", "vašim", "vaše", "vaši", "vašich", "vašimi"],
            "m_než": ["vaše", "vašich", "vašim", "vaše", "vaše", "vašich", "vašimi"],
            "ž": ["vaše", "vašich", "vašim", "vaše", "vaše", "vašich", "vašimi"],
            "s": ["vaše", "vašich", "vašim", "vaše", "vaše", "vašich", "vašimi"]
        }
    },

    # Zvratné
    "se": {
        "singular": ["se", "sebe", "sobě", "sebe", "-", "sobě", "sebou"],
        "plural_base": "se",
        "plural": ["se", "sebe", "sobě", "sebe", "-", "sobě", "sebou"]
    },

    # Zvratné přivlastňovací with gender specifics
    "svůj": {
        "singular": {
            "m_živ": ["svůj", "svého", "svému", "svého", "svůj", "svém", "svým"],
            "m_než": ["svůj", "svého", "svému", "svůj", "svůj", "svém", "svým"],
            "ž": ["svoje", "svojí", "svojí", "svoji", "svoje", "svojí", "svojí"],
            "s": ["svoje", "svého", "svému", "svoje", "svoje", "svém", "svým"]
        },
        "plural": {
            "m_živ": ["svoji", "svých", "svým", "svoje", "svoji", "svých", "svými"],
            "m_než": ["svoje", "svých", "svým", "svoje", "svoje", "svých", "svými"],
            "ž": ["svoje", "svých", "svým", "svoje", "svoje", "svých", "svými"],
            "s": ["svoje", "svých", "svým", "svoje", "svoje", "svých", "svými"]
        }
    }
}