verb_conjugations = {
    "dělat": {
        "přítomný": {
            "j.č.": {1: "dělám", 2: "děláš", 3: "dělá"},
            "mn.č.": {1: "děláme", 2: "děláte", 3: "dělají"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "dělal jsem", 2: "dělal jsi", 3: "dělal"},
                "ž": {1: "dělala jsem", 2: "dělala jsi", 3: "dělala"},
                "s": {1: "dělalo jsem", 2: "dělalo jsi", 3: "dělalo"}
            },
            "mn.č.": {
                "m": {1: "dělali jsme", 2: "dělali jste", 3: "dělali"},
                "ž": {1: "dělaly jsme", 2: "dělaly jste", 3: "dělaly"},
                "s": {1: "dělala jsme", 2: "dělala jste", 3: "dělala"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu dělat", 2: "budeš dělat", 3: "bude dělat"},
            "mn.č.": {1: "budeme dělat", 2: "budete dělat", 3: "budou dělat"}
        },
        "rozkazovací": {
            "j.č.": {2: "dělej", 3: "ať dělá"},
            "mn.č.": {1: "dělejme", 2: "dělejte", 3: "ať dělají"}
        }
    },
    "nést": {
        "přítomný": {
            "j.č.": {1: "nesu", 2: "neseš", 3: "nese"},
            "mn.č.": {1: "neseme", 2: "nesete", 3: "nesou"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "nesl jsem", 2: "nesl jsi", 3: "nesl"},
                "ž": {1: "nesla jsem", 2: "nesla jsi", 3: "nesla"},
                "s": {1: "neslo jsem", 2: "neslo jsi", 3: "neslo"}
            },
            "mn.č.": {
                "m": {1: "nesli jsme", 2: "nesli jste", 3: "nesli"},
                "ž": {1: "nesly jsme", 2: "nesly jste", 3: "nesly"},
                "s": {1: "nesla jsme", 2: "nesla jste", 3: "nesla"}
            }
        },
        "budoucí": {
            "j.č.": {1: "ponesu", 2: "poneseš", 3: "ponese"},
            "mn.č.": {1: "poneseme", 2: "ponesete", 3: "ponesou"}
        },
        "rozkazovací": {
            "j.č.": {2: "nes", 3: "ať nese"},
            "mn.č.": {1: "nesme", 2: "neste", 3: "ať nesou"}
        }
    },
    "psát": {
        "přítomný": {
            "j.č.": {1: "píšu", 2: "píšeš", 3: "píše"},
            "mn.č.": {1: "píšeme", 2: "píšete", 3: "píšou"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "psal jsem", 2: "psal jsi", 3: "psal"},
                "ž": {1: "psala jsem", 2: "psala jsi", 3: "psala"},
                "s": {1: "psalo jsem", 2: "psalo jsi", 3: "psalo"}
            },
            "mn.č.": {
                "m": {1: "psali jsme", 2: "psali jste", 3: "psali"},
                "ž": {1: "psaly jsme", 2: "psaly jste", 3: "psaly"},
                "s": {1: "psala jsme", 2: "psala jste", 3: "psala"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu psát", 2: "budeš psát", 3: "bude psát"},
            "mn.č.": {1: "budeme psát", 2: "budete psát", 3: "budou psát"}
        },
        "rozkazovací": {
            "j.č.": {2: "piš", 3: "ať píše"},
            "mn.č.": {1: "pišme", 2: "pište", 3: "ať píšou"}
        }
    }
}

verb_conjugations.update({
    "hrát": {  # -át vzor
        "přítomný": {
            "j.č.": {1: "hraju", 2: "hraješ", 3: "hraje"},
            "mn.č.": {1: "hrajeme", 2: "hrajete", 3: "hrají"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "hrál jsem", 2: "hrál jsi", 3: "hrál"},
                "ž": {1: "hrála jsem", 2: "hrála jsi", 3: "hrála"},
                "s": {1: "hrálo jsem", 2: "hrálo jsi", 3: "hrálo"}
            },
            "mn.č.": {
                "m": {1: "hráli jsme", 2: "hráli jste", 3: "hráli"},
                "ž": {1: "hrály jsme", 2: "hrály jste", 3: "hrály"},
                "s": {1: "hrála jsme", 2: "hrála jste", 3: "hrála"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu hrát", 2: "budeš hrát", 3: "bude hrát"},
            "mn.č.": {1: "budeme hrát", 2: "budete hrát", 3: "budou hrát"}
        },
        "rozkazovací": {
            "j.č.": {2: "hraj", 3: "ať hraje"},
            "mn.č.": {1: "hrajme", 2: "hrajte", 3: "ať hrají"}
        }
    },
    "umět": {  # -et vzor
        "přítomný": {
            "j.č.": {1: "umím", 2: "umíš", 3: "umí"},
            "mn.č.": {1: "umíme", 2: "umíte", 3: "umí"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "uměl jsem", 2: "uměl jsi", 3: "uměl"},
                "ž": {1: "uměla jsem", 2: "uměla jsi", 3: "uměla"},
                "s": {1: "umělo jsem", 2: "umělo jsi", 3: "umělo"}
            },
            "mn.č.": {
                "m": {1: "uměli jsme", 2: "uměli jste", 3: "uměli"},
                "ž": {1: "uměly jsme", 2: "uměly jste", 3: "uměly"},
                "s": {1: "uměla jsme", 2: "uměla jste", 3: "uměla"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu umět", 2: "budeš umět", 3: "bude umět"},
            "mn.č.": {1: "budeme umět", 2: "budete umět", 3: "budou umět"}
        },
        "rozkazovací": {
            "j.č.": {2: "uměj", 3: "ať umí"},
            "mn.č.": {1: "umějme", 2: "umějte", 3: "ať umí"}
        }
    },
    "pít": {  # -ít vzor, nepravidelný minulý čas
        "přítomný": {
            "j.č.": {1: "piju", 2: "piješ", 3: "pije"},
            "mn.č.": {1: "pijeme", 2: "pijete", 3: "pijí"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "pil jsem", 2: "pil jsi", 3: "pil"},
                "ž": {1: "pila jsem", 2: "pila jsi", 3: "pila"},
                "s": {1: "pilo jsem", 2: "pilo jsi", 3: "pilo"}
            },
            "mn.č.": {
                "m": {1: "pili jsme", 2: "pili jste", 3: "pili"},
                "ž": {1: "pily jsme", 2: "pily jste", 3: "pily"},
                "s": {1: "pila jsme", 2: "pila jste", 3: "pila"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu pít", 2: "budeš pít", 3: "bude pít"},
            "mn.č.": {1: "budeme pít", 2: "budete pít", 3: "budou pít"}
        },
        "rozkazovací": {
            "j.č.": {2: "pij", 3: "ať pije"},
            "mn.č.": {1: "pijme", 2: "pijte", 3: "ať pijí"}
        }
    },
    "minout": {  # -nout vzor
        "přítomný": {
            "j.č.": {1: "minu", 2: "mineš", 3: "mine"},
            "mn.č.": {1: "mineme", 2: "minete", 3: "minou"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "minul jsem", 2: "minul jsi", 3: "minul"},
                "ž": {1: "minula jsem", 2: "minula jsi", 3: "minula"},
                "s": {1: "minulo jsem", 2: "minulo jsi", 3: "minulo"}
            },
            "mn.č.": {
                "m": {1: "minuli jsme", 2: "minuli jste", 3: "minuli"},
                "ž": {1: "minuly jsme", 2: "minuly jste", 3: "minuly"},
                "s": {1: "minula jsme", 2: "minula jste", 3: "minula"}
            }
        },
        "budoucí": {  # dokonavé sloveso
            "j.č.": {1: "minu", 2: "mineš", 3: "mine"},
            "mn.č.": {1: "mineme", 2: "minete", 3: "minou"}
        },
        "rozkazovací": {
            "j.č.": {2: "min", 3: "ať mine"},
            "mn.č.": {1: "minme", 2: "miněte", 3: "ať minou"}
        }
    }
})

verb_conjugations.update({
    "kupovat": {  # -ovat vzor (nedokonavé)
        "přítomný": {
            "j.č.": {1: "kupuji", 2: "kupuješ", 3: "kupuje"},
            "mn.č.": {1: "kupujeme", 2: "kupujete", 3: "kupují"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "kupoval jsem", 2: "kupoval jsi", 3: "kupoval"},
                "ž": {1: "kupovala jsem", 2: "kupovala jsi", 3: "kupovala"},
                "s": {1: "kupovalo jsem", 2: "kupovalo jsi", 3: "kupovalo"}
            },
            "mn.č.": {
                "m": {1: "kupovali jsme", 2: "kupovali jste", 3: "kupovali"},
                "ž": {1: "kupovaly jsme", 2: "kupovaly jste", 3: "kupovaly"},
                "s": {1: "kupovala jsme", 2: "kupovala jste", 3: "kupovala"}
            }
        },
        "budoucí": {  # opisný
            "j.č.": {1: "budu kupovat", 2: "budeš kupovat", 3: "bude kupovat"},
            "mn.č.": {1: "budeme kupovat", 2: "budete kupovat", 3: "budou kupovat"}
        },
        "rozkazovací": {
            "j.č.": {2: "kupuj", 3: "ať kupuje"},
            "mn.č.": {1: "kupujme", 2: "kupujte", 3: "ať kupují"}
        }
    },
    "házet": {  # změna kmene z→ž
        "přítomný": {
            "j.č.": {1: "házím", 2: "házíš", 3: "hází"},
            "mn.č.": {1: "házíme", 2: "házíte", 3: "hází"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "házel jsem", 2: "házel jsi", 3: "házel"},
                "ž": {1: "házela jsem", 2: "házela jsi", 3: "házela"},
                "s": {1: "házelo jsem", 2: "házelo jsi", 3: "házelo"}
            },
            "mn.č.": {
                "m": {1: "házeli jsme", 2: "házeli jste", 3: "házeli"},
                "ž": {1: "házely jsme", 2: "házely jste", 3: "házely"},
                "s": {1: "házela jsme", 2: "házela jste", 3: "házela"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu házet", 2: "budeš házet", 3: "bude házet"},
            "mn.č.": {1: "budeme házet", 2: "budete házet", 3: "budou házet"}
        },
        "rozkazovací": {
            "j.č.": {2: "házej", 3: "ať hází"},
            "mn.č.": {1: "házejme", 2: "házejte", 3: "ať hází"}
        }
    },
    "mazat": {  # z→ž
        "přítomný": {
            "j.č.": {1: "mažu", 2: "mažeš", 3: "maže"},
            "mn.č.": {1: "mažeme", 2: "mažete", 3: "mažou"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "mazal jsem", 2: "mazal jsi", 3: "mazal"},
                "ž": {1: "mazala jsem", 2: "mazala jsi", 3: "mazala"},
                "s": {1: "mazalo jsem", 2: "mazalo jsi", 3: "mazalo"}
            },
            "mn.č.": {
                "m": {1: "mazali jsme", 2: "mazali jste", 3: "mazali"},
                "ž": {1: "mazaly jsme", 2: "mazaly jste", 3: "mazaly"},
                "s": {1: "mazala jsme", 2: "mazala jste", 3: "mazala"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu mazat", 2: "budeš mazat", 3: "bude mazat"},
            "mn.č.": {1: "budeme mazat", 2: "budete mazat", 3: "budou mazat"}
        },
        "rozkazovací": {
            "j.č.": {2: "maž", 3: "ať maže"},
            "mn.č.": {1: "mažme", 2: "mažte", 3: "ať mažou"}
        }
    },
    "prosit": {  # -it pravidelné
        "přítomný": {
            "j.č.": {1: "prosím", 2: "prosíš", 3: "prosí"},
            "mn.č.": {1: "prosíme", 2: "prosíte", 3: "prosí"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "prosil jsem", 2: "prosil jsi", 3: "prosil"},
                "ž": {1: "prosila jsem", 2: "prosila jsi", 3: "prosila"},
                "s": {1: "prosilo jsem", 2: "prosilo jsi", 3: "prosilo"}
            },
            "mn.č.": {
                "m": {1: "prosili jsme", 2: "prosili jste", 3: "prosili"},
                "ž": {1: "prosily jsme", 2: "prosily jste", 3: "prosily"},
                "s": {1: "prosila jsme", 2: "prosila jste", 3: "prosila"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu prosit", 2: "budeš prosit", 3: "bude prosit"},
            "mn.č.": {1: "budeme prosit", 2: "budete prosit", 3: "budou prosit"}
        },
        "rozkazovací": {
            "j.č.": {2: "pros", 3: "ať prosí"},
            "mn.č.": {1: "prosme", 2: "proste", 3: "ať prosí"}
        }
    }
})

verb_conjugations.update({
    "krýt": {  # -ýt, kolísání kmenů
        "přítomný": {
            "j.č.": {1: "kryji", 2: "kryješ", 3: "kryje"},
            "mn.č.": {1: "kryjeme", 2: "kryjete", 3: "kryjí"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "kryl jsem", 2: "kryl jsi", 3: "kryl"},
                "ž": {1: "kryla jsem", 2: "kryla jsi", 3: "kryla"},
                "s": {1: "krylo jsem", 2: "krylo jsi", 3: "krylo"}
            },
            "mn.č.": {
                "m": {1: "kryli jsme", 2: "kryli jste", 3: "kryli"},
                "ž": {1: "kryly jsme", 2: "kryly jste", 3: "kryly"},
                "s": {1: "kryla jsme", 2: "kryla jste", 3: "kryla"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu krýt", 2: "budeš krýt", 3: "bude krýt"},
            "mn.č.": {1: "budeme krýt", 2: "budete krýt", 3: "budou krýt"}
        },
        "rozkazovací": {
            "j.č.": {2: "kryj", 3: "ať kryje"},
            "mn.č.": {1: "kryjme", 2: "kryjte", 3: "ať kryjí"}
        }
    },
    "sázet": {  # z→ž a délka samohlásky
        "přítomný": {
            "j.č.": {1: "sázím", 2: "sázíš", 3: "sází"},
            "mn.č.": {1: "sázíme", 2: "sázíte", 3: "sázejí"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "sázel jsem", 2: "sázel jsi", 3: "sázel"},
                "ž": {1: "sázela jsem", 2: "sázela jsi", 3: "sázela"},
                "s": {1: "sázelo jsem", 2: "sázelo jsi", 3: "sázelo"}
            },
            "mn.č.": {
                "m": {1: "sázeli jsme", 2: "sázeli jste", 3: "sázeli"},
                "ž": {1: "sázely jsme", 2: "sázely jste", 3: "sázely"},
                "s": {1: "sázela jsme", 2: "sázela jste", 3: "sázela"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu sázet", 2: "budeš sázet", 3: "bude sázet"},
            "mn.č.": {1: "budeme sázet", 2: "budete sázet", 3: "budou sázet"}
        },
        "rozkazovací": {
            "j.č.": {2: "sázej", 3: "ať sází"},
            "mn.č.": {1: "sázejme", 2: "sázejte", 3: "ať sázejí"}
        }
    },
    "péct": {  # k→č
        "přítomný": {
            "j.č.": {1: "peču", 2: "pečeš", 3: "peče"},
            "mn.č.": {1: "pečeme", 2: "pečete", 3: "pečou"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "pekl jsem", 2: "pekl jsi", 3: "pekl"},
                "ž": {1: "pekla jsem", 2: "pekla jsi", 3: "pekla"},
                "s": {1: "peklo jsem", 2: "peklo jsi", 3: "peklo"}
            },
            "mn.č.": {
                "m": {1: "pekli jsme", 2: "pekli jste", 3: "pekli"},
                "ž": {1: "pekly jsme", 2: "pekly jste", 3: "pekly"},
                "s": {1: "pekla jsme", 2: "pekla jste", 3: "pekla"}
            }
        },
        "budoucí": {  # dokonavé
            "j.č.": {1: "upeču", 2: "učeš", 3: "upeče"},
            "mn.č.": {1: "upečeme", 2: "upečete", 3: "upečou"}
        },
        "rozkazovací": {
            "j.č.": {2: "peč", 3: "ať peče"},
            "mn.č.": {1: "pečme", 2: "pečte", 3: "ať pečou"}
        }
    },
    "brát": {  # á→e
        "přítomný": {
            "j.č.": {1: "beru", 2: "bereš", 3: "bere"},
            "mn.č.": {1: "bereme", 2: "berete", 3: "berou"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "bral jsem", 2: "bral jsi", 3: "bral"},
                "ž": {1: "brala jsem", 2: "brala jsi", 3: "brala"},
                "s": {1: "bralo jsem", 2: "bralo jsi", 3: "bralo"}
            },
            "mn.č.": {
                "m": {1: "brali jsme", 2: "brali jste", 3: "brali"},
                "ž": {1: "braly jsme", 2: "braly jste", 3: "braly"},
                "s": {1: "brala jsme", 2: "brala jste", 3: "brala"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu brát", 2: "budeš brát", 3: "bude brát"},
            "mn.č.": {1: "budeme brát", 2: "budete brát", 3: "budou brát"}
        },
        "rozkazovací": {
            "j.č.": {2: "ber", 3: "ať bere"},
            "mn.č.": {1: "berme", 2: "berte", 3: "ať berou"}
        }
    }
})

verb_conjugations.update({
    "tisknout": {  # vypouštění samohlásky v kmenu
        "přítomný": {
            "j.č.": {1: "tisknu", 2: "tiskneš", 3: "tiskne"},
            "mn.č.": {1: "tiskneme", 2: "tisknete", 3: "tisknou"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "tiskl jsem", 2: "tiskl jsi", 3: "tiskl"},
                "ž": {1: "tiskla jsem", 2: "tiskla jsi", 3: "tiskla"},
                "s": {1: "tisklo jsem", 2: "tisklo jsi", 3: "tisklo"}
            },
            "mn.č.": {
                "m": {1: "tiskli jsme", 2: "tiskli jste", 3: "tiskli"},
                "ž": {1: "tiskly jsme", 2: "tiskly jste", 3: "tiskly"},
                "s": {1: "tiskla jsme", 2: "tiskla jste", 3: "tiskla"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu tisknout", 2: "budeš tisknout", 3: "bude tisknout"},
            "mn.č.": {1: "budeme tisknout", 2: "budete tisknout", 3: "budou tisknout"}
        },
        "rozkazovací": {
            "j.č.": {2: "tiskni", 3: "ať tiskne"},
            "mn.č.": {1: "tiskněme", 2: "tiskněte", 3: "ať tisknou"}
        }
    },
    "růst": {  # změna ů→o v min. čase
        "přítomný": {
            "j.č.": {1: "rostu", 2: "rosteš", 3: "roste"},
            "mn.č.": {1: "rosteme", 2: "rostete", 3: "rostou"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "rostl jsem", 2: "rostl jsi", 3: "rostl"},
                "ž": {1: "rostla jsem", 2: "rostla jsi", 3: "rostla"},
                "s": {1: "rostlo jsem", 2: "rostlo jsi", 3: "rostlo"}
            },
            "mn.č.": {
                "m": {1: "rostli jsme", 2: "rostli jste", 3: "rostli"},
                "ž": {1: "rostly jsme", 2: "rostly jste", 3: "rostly"},
                "s": {1: "rostla jsme", 2: "rostla jste", 3: "rostla"}
            }
        },
        "budoucí": {
            "j.č.": {1: "porostu", 2: "porosteš", 3: "poroste"},
            "mn.č.": {1: "porosteme", 2: "porostete", 3: "porostou"}
        },
        "rozkazovací": {
            "j.č.": {2: "rost", 3: "ať roste"},
            "mn.č.": {1: "rostme", 2: "roste", 3: "ať rostou"}
        }
    },
    "myslet": {  # -et, změna kmene
        "přítomný": {
            "j.č.": {1: "myslím", 2: "myslíš", 3: "myslí"},
            "mn.č.": {1: "myslíme", 2: "myslíte", 3: "myslí"}
        },
        "minulý": {
            "j.č.": {
                "m": {1: "myslel jsem", 2: "myslel jsi", 3: "myslel"},
                "ž": {1: "myslela jsem", 2: "myslela jsi", 3: "myslela"},
                "s": {1: "myslelo jsem", 2: "myslelo jsi", 3: "myslelo"}
            },
            "mn.č.": {
                "m": {1: "mysleli jsme", 2: "mysleli jste", 3: "mysleli"},
                "ž": {1: "myslely jsme", 2: "myslely jste", 3: "myslely"},
                "s": {1: "myslela jsme", 2: "myslela jste", 3: "myslela"}
            }
        },
        "budoucí": {
            "j.č.": {1: "budu myslet", 2: "budeš myslet", 3: "bude myslet"},
            "mn.č.": {1: "budeme myslet", 2: "budete myslet", 3: "budou myslet"}
        },
        "rozkazovací": {
            "j.č.": {2: "mysli", 3: "ať myslí"},
            "mn.č.": {1: "mysleme", 2: "myslete", 3: "ať myslí"}
        }
    }
})