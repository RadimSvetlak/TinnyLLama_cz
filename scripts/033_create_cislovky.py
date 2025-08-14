cases = ["1. pád", "2. pád", "3. pád", "4. pád", "5. pád", "6. pád", "7. pád"]
# slovník základních a řadových číslovek
cislovky = {
    "jeden": {
        "zakladni": {
            "m_ziv":   ["jeden", "jednoho", "jednomu", "jednoho", "jeden", "jednom", "jedním"],
            "m_neziv": ["jeden", "jeden",  "jednomu", "jeden",  "jeden", "jednom", "jedním"],
            "z":       ["jedna", "jedné",  "jedné",   "jednu",  "jedna", "jedné",  "jednou"],
            "s":       ["jedno", "jednoho","jednomu", "jedno",  "jedno", "jednom", "jedním"]
        },
        "radove": {
            "m_ziv":   ["první", "prvního", "prvnímu", "prvního", "první", "prvním", "prvním"],
            "m_neziv": ["první", "prvního", "prvnímu", "první",   "první", "prvním", "prvním"],
            "z":       ["první", "první",   "první",   "první",   "první", "první",  "první"],
            "s":       ["první", "prvního", "prvnímu", "první",   "první", "prvním", "prvním"]
        }
    },
    "dva": {
        "zakladni": {
            "m_ziv":   ["dva", "dvou", "dvěma", "dva",   "dva",   "dvou",   "dvěma"],
            "m_neziv": ["dva", "dvou", "dvěma", "dva",   "dva",   "dvou",   "dvěma"],
            "z":       ["dvě", "dvou", "dvěma", "dvě",   "dvě",   "dvou",   "dvěma"],
            "s":       ["dvě", "dvou", "dvěma", "dvě",   "dvě",   "dvou",   "dvěma"]
        },
        "radove": {
            "m_ziv":   ["druhý", "druhého", "druhému", "druhého", "druhý", "druhém", "druhým"],
            "m_neziv": ["druhý", "druhého", "druhému", "druhý",   "druhý", "druhém", "druhým"],
            "z":       ["druhá", "druhé",   "druhé",   "druhou",  "druhá", "druhé",  "druhou"],
            "s":       ["druhé", "druhého", "druhému", "druhé",   "druhé", "druhém", "druhým"]
        }
    },
    "tři": {
        "zakladni": {
            "m_ziv":   ["tři",  "třech", "třem",  "tři",  "tři",  "třech", "třemi"],
            "m_neziv": ["tři",  "třech", "třem",  "tři",  "tři",  "třech", "třemi"],
            "z":       ["tři",  "třech", "třem",  "tři",  "tři",  "třech", "třemi"],
            "s":       ["tři",  "třech", "třem",  "tři",  "tři",  "třech", "třemi"]
        },
        "radove": {
            "m_ziv":   ["třetí", "třetího", "třetímu", "třetího", "třetí", "třetím", "třetím"],
            "m_neziv": ["třetí", "třetího", "třetímu", "třetí",   "třetí", "třetím", "třetím"],
            "z":       ["třetí", "třetí",   "třetí",   "třetí",   "třetí", "třetí",  "třetí"],
            "s":       ["třetí", "třetího", "třetímu", "třetí",   "třetí", "třetím", "třetím"]
        }
    },
    "čtyři": {
        "zakladni": {
            "m_ziv":   ["čtyři",   "čtyř",   "čtyřem",  "čtyři",   "čtyři",   "čtyřech", "čtyřmi"],
            "m_neziv": ["čtyři",   "čtyř",   "čtyřem",  "čtyři",   "čtyři",   "čtyřech", "čtyřmi"],
            "z":       ["čtyři",   "čtyř",   "čtyřem",  "čtyři",   "čtyři",   "čtyřech", "čtyřmi"],
            "s":       ["čtyři",   "čtyř",   "čtyřem",  "čtyři",   "čtyři",   "čtyřech", "čtyřmi"]
        },
        "radove": {
            "m_ziv":   ["čtvrtý",  "čtvrtého","čtvrtému","čtvrtého","čtvrtý","čtvrtém","čtvrtým"],
            "m_neziv": ["čtvrtý",  "čtvrtého","čtvrtému","čtvrtý",  "čtvrtý","čtvrtém","čtvrtým"],
            "z":       ["čtvrtá",  "čtvrté",  "čtvrté",  "čtvrtou", "čtvrtá","čtvrté", "čtvrtou"],
            "s":       ["čtvrté",  "čtvrtého","čtvrtému","čtvrté",  "čtvrté","čtvrtém","čtvrtým"]
        }
    }
}

cislovky.update({
    "pět": {
        "zakladni": {
            "vse": ["pět", "pěti", "pěti", "pět", "pět", "pěti", "pěti"]
        },
        "radove": {
            "m": ["pátý", "pátého", "pátému", "pátého", "pátý", "pátém", "pátým"],
            "z": ["pátá", "páté", "páté", "pátou", "pátá", "páté", "pátou"],
            "s": ["páté", "pátého", "pátému", "páté", "páté", "pátém", "pátým"]
        }
    },
    "šest": {
        "zakladni": {
            "vse": ["šest", "šesti", "šesti", "šest", "šest", "šesti", "šesti"]
        },
        "radove": {
            "m": ["šestý", "šestého", "šestému", "šestého", "šestý", "šestém", "šestým"],
            "z": ["šestá", "šesté", "šesté", "šestou", "šestá", "šesté", "šestou"],
            "s": ["šesté", "šestého", "šestému", "šesté", "šesté", "šestém", "šestým"]
        }
    },
    "sedm": {
        "zakladni": {
            "vse": ["sedm", "sedmi", "sedmi", "sedm", "sedm", "sedmi", "sedmi"]
        },
        "radove": {
            "m": ["sedmý", "sedmého", "sedmému", "sedmého", "sedmý", "sedmém", "sedmým"],
            "z": ["sedmá", "sedmé", "sedmé", "sedmou", "sedmá", "sedmé", "sedmou"],
            "s": ["sedmé", "sedmého", "sedmému", "sedmé", "sedmé", "sedmém", "sedmým"]
        }
    },
    "osm": {
        "zakladni": {
            "vse": ["osm", "osmi", "osmi", "osm", "osm", "osmi", "osmi"]
        },
        "radove": {
            "m": ["osmý", "osmého", "osmému", "osmého", "osmý", "osmém", "osmým"],
            "z": ["osmá", "osmé", "osmé", "osmou", "osmá", "osmé", "osmou"],
            "s": ["osmé", "osmého", "osmému", "osmé", "osmé", "osmém", "osmým"]
        }
    },
    "devět": {
        "zakladni": {
            "vse": ["devět", "devíti", "devíti", "devět", "devět", "devíti", "devíti"]
        },
        "radove": {
            "m": ["devátý", "devátého", "devátému", "devátého", "devátý", "devátém", "devátým"],
            "z": ["devátá", "deváté", "deváté", "devátou", "devátá", "deváté", "devátou"],
            "s": ["deváté", "devátého", "devátému", "deváté", "deváté", "devátém", "devátým"]
        }
    },
    "deset": {
        "zakladni": {
            "vse": ["deset", "deseti", "deseti", "deset", "deset", "deseti", "deseti"]
        },
        "radove": {
            "m": ["desátý", "desátého", "desátému", "desátého", "desátý", "desátém", "desátým"],
            "z": ["desátá", "desáté", "desáté", "desátou", "desátá", "desáté", "desátou"],
            "s": ["desáté", "desátého", "desátému", "desáté", "desáté", "desátém", "desátým"]
        }
    }
})

cislovky.update({
    "jedenact": {
        "zakladni": {
            "vse": ["jedenáct", "jedenácti", "jedenácti", "jedenáct", "jedenáct", "jedenácti", "jedenácti"]
        },
        "radove": {
            "m": ["jedenáctý", "jedenáctého", "jedenáctému", "jedenáctého", "jedenáctý", "jedenáctém", "jedenáctým"],
            "z": ["jedenáctá", "jedenácté", "jedenácté", "jedenáctou", "jedenáctá", "jedenácté", "jedenáctou"],
            "s": ["jedenácté", "jedenáctého", "jedenáctému", "jedenácté", "jedenácté", "jedenáctém", "jedenáctým"]
        }
    },
    "dvanact": {
        "zakladni": {
            "vse": ["dvanáct", "dvanácti", "dvanácti", "dvanáct", "dvanáct", "dvanácti", "dvanácti"]
        },
        "radove": {
            "m": ["dvanáctý", "dvanáctého", "dvanáctému", "dvanáctého", "dvanáctý", "dvanáctém", "dvanáctým"],
            "z": ["dvanáctá", "dvanácté", "dvanácté", "dvanáctou", "dvanáctá", "dvanácté", "dvanáctou"],
            "s": ["dvanácté", "dvanáctého", "dvanáctému", "dvanácté", "dvanácté", "dvanáctém", "dvanáctým"]
        }
    },
    "trinact": {
        "zakladni": {
            "vse": ["třináct", "třinácti", "třinácti", "třináct", "třináct", "třinácti", "třinácti"]
        },
        "radove": {
            "m": ["třináctý", "třináctého", "třináctému", "třináctého", "třináctý", "třináctém", "třináctým"],
            "z": ["třináctá", "třinácté", "třinácté", "třináctou", "třináctá", "třinácté", "třináctou"],
            "s": ["třinácté", "třináctého", "třináctému", "třinácté", "třinácté", "třináctém", "třináctým"]
        }
    },
    "ctrnact": {
        "zakladni": {
            "vse": ["čtrnáct", "čtrnácti", "čtrnácti", "čtrnáct", "čtrnáct", "čtrnácti", "čtrnácti"]
        },
        "radove": {
            "m": ["čtrnáctý", "čtrnáctého", "čtrnáctému", "čtrnáctého", "čtrnáctý", "čtrnáctém", "čtrnáctým"],
            "z": ["čtrnáctá", "čtrnácté", "čtrnácté", "čtrnáctou", "čtrnáctá", "čtrnácté", "čtrnáctou"],
            "s": ["čtrnácté", "čtrnáctého", "čtrnáctému", "čtrnácté", "čtrnácté", "čtrnáctém", "čtrnáctým"]
        }
    },
    "patnact": {
        "zakladni": {
            "vse": ["patnáct", "patnácti", "patnácti", "patnáct", "patnáct", "patnácti", "patnácti"]
        },
        "radove": {
            "m": ["patnáctý", "patnáctého", "patnáctému", "patnáctého", "patnáctý", "patnáctém", "patnáctým"],
            "z": ["patnáctá", "patnácté", "patnácté", "patnáctou", "patnáctá", "patnácté", "patnáctou"],
            "s": ["patnácté", "patnáctého", "patnáctému", "patnácté", "patnácté", "patnáctém", "patnáctým"]
        }
    },
    "sestnact": {
        "zakladni": {
            "vse": ["šestnáct", "šestnácti", "šestnácti", "šestnáct", "šestnáct", "šestnácti", "šestnácti"]
        },
        "radove": {
            "m": ["šestnáctý", "šestnáctého", "šestnáctému", "šestnáctého", "šestnáctý", "šestnáctém", "šestnáctým"],
            "z": ["šestnáctá", "šestnácté", "šestnácté", "šestnáctou", "šestnáctá", "šestnácté", "šestnáctou"],
            "s": ["šestnácté", "šestnáctého", "šestnáctému", "šestnácté", "šestnácté", "šestnáctém", "šestnáctým"]
        }
    }
})

cislovky.update({
    "sedmnact": {
        "zakladni": {
            "vse": ["sedmnáct", "sedmnácti", "sedmnácti", "sedmnáct", "sedmnáct", "sedmnácti", "sedmnácti"]
        },
        "radove": {
            "m": ["sedmnáctý", "sedmnáctého", "sedmnáctému", "sedmnáctého", "sedmnáctý", "sedmnáctém", "sedmnáctým"],
            "z": ["sedmnáctá", "sedmnácté", "sedmnácté", "sedmnáctou", "sedmnáctá", "sedmnácté", "sedmnáctou"],
            "s": ["sedmnácté", "sedmnáctého", "sedmnáctému", "sedmnácté", "sedmnácté", "sedmnáctém", "sedmnáctým"]
        }
    },
    "osmnact": {
        "zakladni": {
            "vse": ["osmnáct", "osmnácti", "osmnácti", "osmnáct", "osmnáct", "osmnácti", "osmnácti"]
        },
        "radove": {
            "m": ["osmnáctý", "osmnáctého", "osmnáctému", "osmnáctého", "osmnáctý", "osmnáctém", "osmnáctým"],
            "z": ["osmnáctá", "osmnácté", "osmnácté", "osmnáctou", "osmnáctá", "osmnácté", "osmnáctou"],
            "s": ["osmnácté", "osmnáctého", "osmnáctému", "osmnácté", "osmnácté", "osmnáctém", "osmnáctým"]
        }
    },
    "devatenact": {
        "zakladni": {
            "vse": ["devatenáct", "devatenácti", "devatenácti", "devatenáct", "devatenáct", "devatenácti", "devatenácti"]
        },
        "radove": {
            "m": ["devatenáctý", "devatenáctého", "devatenáctému", "devatenáctého", "devatenáctý", "devatenáctém", "devatenáctým"],
            "z": ["devatenáctá", "devatenácté", "devatenácté", "devatenáctou", "devatenáctá", "devatenácté", "devatenáctou"],
            "s": ["devatenácté", "devatenáctého", "devatenáctému", "devatenácté", "devatenácté", "devatenáctém", "devatenáctým"]
        }
    },
    "dvacet": {
        "zakladni": {
            "vse": ["dvacet", "dvaceti", "dvaceti", "dvacet", "dvacet", "dvaceti", "dvaceti"]
        },
        "radove": {
            "m": ["dvacátý", "dvacátého", "dvacátému", "dvacátého", "dvacátý", "dvacátém", "dvacátým"],
            "z": ["dvacátá", "dvacáté", "dvacáté", "dvacátou", "dvacátá", "dvacáté", "dvacátou"],
            "s": ["dvacáté", "dvacátého", "dvacátému", "dvacáté", "dvacáté", "dvacátém", "dvacátým"]
        }
    },
    "dvacet_jedna": {
        "zakladni": {
            "vse": ["dvacet jedna", "dvaceti jedné", "dvaceti jedné", "dvacet jednu", "dvacet jedna", "dvaceti jedné", "dvaceti jednou"]
        },
        "radove": {
            "m": ["dvacátý první", "dvacátého prvního", "dvacátému prvnímu", "dvacátého prvního", "dvacátý první", "dvacátém prvním", "dvacátým prvním"],
            "z": ["dvacátá první", "dvacáté první", "dvacáté první", "dvacátou první", "dvacátá první", "dvacáté první", "dvacátou první"],
            "s": ["dvacáté první", "dvacátého prvního", "dvacátému prvnímu", "dvacáté první", "dvacáté první", "dvacátém prvním", "dvacátým prvním"]
        }
    }
})

cislovky.update({
    "dvacet_dve": {
        "zakladni": {
            "vse": ["dvacet dvě", "dvaceti dvou", "dvaceti dvěma", "dvacet dvě", "dvacet dvě", "dvaceti dvou", "dvaceti dvěma"]
        },
        "radove": {
            "m": ["dvacátý druhý", "dvacátého druhého", "dvacátému druhému", "dvacátého druhého", "dvacátý druhý", "dvacátém druhém", "dvacátým druhým"],
            "z": ["dvacátá druhá", "dvacáté druhé", "dvacáté druhé", "dvacátou druhou", "dvacátá druhá", "dvacáté druhé", "dvacátou druhou"],
            "s": ["dvacáté druhé", "dvacátého druhého", "dvacátému druhému", "dvacáté druhé", "dvacáté druhé", "dvacátém druhém", "dvacátým druhým"]
        }
    },
    "dvacet_sedm": {
        "zakladni": {
            "vse": ["dvacet sedm", "dvaceti sedmi", "dvaceti sedmi", "dvacet sedm", "dvacet sedm", "dvaceti sedmi", "dvaceti sedmi"]
        },
        "radove": {
            "m": ["dvacátý sedmý", "dvacátého sedmého", "dvacátému sedmému", "dvacátého sedmého", "dvacátý sedmý", "dvacátém sedmém", "dvacátým sedmým"],
            "z": ["dvacátá sedmá", "dvacáté sedmé", "dvacáté sedmé", "dvacátou sedmou", "dvacátá sedmá", "dvacáté sedmé", "dvacátou sedmou"],
            "s": ["dvacáté sedmé", "dvacátého sedmého", "dvacátému sedmému", "dvacáté sedmé", "dvacáté sedmé", "dvacátém sedmém", "dvacátým sedmým"]
        }
    },
    "tricet_jedna": {
        "zakladni": {
            "vse": ["třicet jedna", "třiceti jedné", "třiceti jedné", "třicet jednu", "třicet jedna", "třiceti jedné", "třiceti jednou"]
        },
        "radove": {
            "m": ["třicátý první", "třicátého prvního", "třicátému prvnímu", "třicátého prvního", "třicátý první", "třicátém prvním", "třicátým prvním"],
            "z": ["třicátá první", "třicáté první", "třicáté první", "třicátou první", "třicátá první", "třicáté první", "třicátou první"],
            "s": ["třicáté první", "třicátého prvního", "třicátému prvnímu", "třicáté první", "třicáté první", "třicátém prvním", "třicátým prvním"]
        }
    },
    "tricet_ctyri": {
        "zakladni": {
            "vse": ["třicet čtyři", "třiceti čtyř", "třiceti čtyřem", "třicet čtyři", "třicet čtyři", "třiceti čtyřech", "třiceti čtyřmi"]
        },
        "radove": {
            "m": ["třicátý čtvrtý", "třicátého čtvrtého", "třicátému čtvrtému", "třicátého čtvrtého", "třicátý čtvrtý", "třicátém čtvrtém", "třicátým čtvrtým"],
            "z": ["třicátá čtvrtá", "třicáté čtvrté", "třicáté čtvrté", "třicátou čtvrtou", "třicátá čtvrtá", "třicáté čtvrté", "třicátou čtvrtou"],
            "s": ["třicáté čtvrté", "třicátého čtvrtého", "třicátému čtvrtému", "třicáté čtvrté", "třicáté čtvrté", "třicátém čtvrtém", "třicátým čtvrtým"]
        }
    },
    "ctyricet_dve": {
        "zakladni": {
            "vse": ["čtyřicet dvě", "čtyřiceti dvou", "čtyřiceti dvěma", "čtyřicet dvě", "čtyřicet dvě", "čtyřiceti dvou", "čtyřiceti dvěma"]
        },
        "radove": {
            "m": ["čtyřicátý druhý", "čtyřicátého druhého", "čtyřicátému druhému", "čtyřicátého druhého", "čtyřicátý druhý", "čtyřicátém druhém", "čtyřicátým druhým"],
            "z": ["čtyřicátá druhá", "čtyřicáté druhé", "čtyřicáté druhé", "čtyřicátou druhou", "čtyřicátá druhá", "čtyřicáté druhé", "čtyřicátou druhou"],
            "s": ["čtyřicáté druhé", "čtyřicátého druhého", "čtyřicátému druhému", "čtyřicáté druhé", "čtyřicáté druhé", "čtyřicátém druhém", "čtyřicátým druhým"]
        }
    },
    "padesat_pet": {
        "zakladni": {
            "vse": ["padesát pět", "padesáti pěti", "padesáti pěti", "padesát pět", "padesát pět", "padesáti pěti", "padesáti pěti"]
        },
        "radove": {
            "m": ["padesátý pátý", "padesátého pátého", "padesátému pátému", "padesátého pátého", "padesátý pátý", "padesátém pátém", "padesátým pátým"],
            "z": ["padesátá pátá", "padesáté páté", "padesáté páté", "padesátou pátou", "padesátá pátá", "padesáté páté", "padesátou pátou"],
            "s": ["padesáté páté", "padesátého pátého", "padesátému pátému", "padesáté páté", "padesáté páté", "padesátém pátém", "padesátým pátým"]
        }
    },
    "sedesat_tri": {
        "zakladni": {
            "vse": ["šedesát tři", "šedesáti tří", "šedesáti třem", "šedesát tři", "šedesát tři", "šedesáti třech", "šedesáti třemi"]
        },
        "radove": {
            "m": ["šedesátý třetí", "šedesátého třetího", "šedesátému třetímu", "šedesátého třetího", "šedesátý třetí", "šedesátém třetím", "šedesátým třetím"],
            "z": ["šedesátá třetí", "šedesáté třetí", "šedesáté třetí", "šedesátou třetí", "šedesátá třetí", "šedesáté třetí", "šedesátou třetí"],
            "s": ["šedesáté třetí", "šedesátého třetího", "šedesátému třetímu", "šedesáté třetí", "šedesáté třetí", "šedesátém třetím", "šedesátým třetím"]
        }
    },
    "sedmdesat_ctyri": {
        "zakladni": {
            "vse": ["sedmdesát čtyři", "sedmdesáti čtyř", "sedmdesáti čtyřem", "sedmdesát čtyři", "sedmdesát čtyři", "sedmdesáti čtyřech", "sedmdesáti čtyřmi"]
        },
        "radove": {
            "m": ["sedmdesátý čtvrtý", "sedmdesátého čtvrtého", "sedmdesátému čtvrtému", "sedmdesátého čtvrtého", "sedmdesátý čtvrtý", "sedmdesátém čtvrtém", "sedmdesátým čtvrtým"],
            "z": ["sedmdesátá čtvrtá", "sedmdesáté čtvrté", "sedmdesáté čtvrté", "sedmdesátou čtvrtou", "sedmdesátá čtvrtá", "sedmdesáté čtvrté", "sedmdesátou čtvrtou"],
            "s": ["sedmdesáté čtvrté", "sedmdesátého čtvrtého", "sedmdesátému čtvrtému", "sedmdesáté čtvrté", "sedmdesáté čtvrté", "sedmdesátém čtvrtém", "sedmdesátým čtvrtým"]
        }
    },
    "osmdesat_osm": {
        "zakladni": {
            "vse": ["osmdesát osm", "osmdesáti osmi", "osmdesáti osmi", "osmdesát osm", "osmdesát osm", "osmdesáti osmi", "osmdesáti osmi"]
        },
        "radove": {
            "m": ["osmdesátý osmý", "osmdesátého osmého", "osmdesátému osmému", "osmdesátého osmého", "osmdesátý osmý", "osmdesátém osmém", "osmdesátým osmým"],
            "z": ["osmdesátá osmá", "osmdesáté osmé", "osmdesáté osmé", "osmdesátou osmou", "osmdesátá osmá", "osmdesáté osmé", "osmdesátou osmou"],
            "s": ["osmdesáté osmé", "osmdesátého osmého", "osmdesátému osmému", "osmdesáté osmé", "osmdesáté osmé", "osmdesátém osmém", "osmdesátým osmým"]
        }
    },
    "devadesat_devet": {
        "zakladni": {
            "vse": ["devadesát devět", "devadesáti devíti", "devadesáti devíti", "devadesát devět", "devadesát devět", "devadesáti devíti", "devadesáti devíti"]
        },
        "radove": {
            "m": ["devadesátý devátý", "devadesátého devátého", "devadesátému devátému", "devadesátého devátého", "devadesátý devátý", "devadesátém devátém", "devadesátým devátým"],
            "z": ["devadesátá devátá", "devadesáté deváté", "devadesáté deváté", "devadesátou devátou", "devadesátá devátá", "devadesáté deváté", "devadesátou devátou"],
            "s": ["devadesáté deváté", "devadesátého devátého", "devadesátému devátému", "devadesáté deváté", "devadesáté deváté", "devadesátém devátém", "devadesátým devátým"]
        }
    }
})



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

# -*- coding: utf-8 -*-
import json
import random
from collections import Counter

# -----------------------------------------------------------
# Základní nastavení
# -----------------------------------------------------------

CASES = ["1. pád", "2. pád", "3. pád", "4. pád", "5. pád", "6. pád", "7. pád"]
CASE_INDEXES = list(range(7))

# Předložky podle pádu pro přirozené kontexty (můžeš rozšířit)
PREP_BY_CASE = {
    1: [],  # Nominativ
    2: ["bez", "od", "u", "do", "z"],
    3: ["k", "proti", "naproti"],
    4: ["na", "pro", "přes", "za"],
    5: [],  # Vokativ
    6: ["o", "na", "po", "při"],
    7: ["s", "za", "před", "pod", "nad", "mezi"]
}

# Šablony vět dle pádu (stručné, přehledné pro malé LLM)
CASE_TEMPLATES = {
    0: ["{phrase} dnes začíná.", "{phrase} je připraveno.", "{phrase} dorazilo včas."],
    1: ["Bez {phrase} to nepůjde.", "Kolem {phrase} bylo rušno.", "Uprostřed {phrase} bylo ticho."],
    2: ["K {phrase} jsme dorazili pozdě.", "Proti {phrase} nic nenamítal.", "Naproti {phrase} stojí stan."],
    3: ["Vidím {phrase} na ulici.", "Potkal jsem {phrase} včera.", "Přinesl jsem {phrase} domů."],
    4: ["{phrase}, pojď sem!", "{phrase}, prosím, počkej!", "{phrase}, slyšíš mě?"],
    5: ["O {phrase} jsme mluvili celý den.", "Na {phrase} záleží nejvíc.", "Po {phrase} následuje přestávka."],
    6: ["S {phrase} to půjde lépe.", "Před {phrase} jsme se zastavili.", "Za {phrase} se skrývá pravda."]
}

# -----------------------------------------------------------
# Pomocné utilitky
# -----------------------------------------------------------

def set_seed(seed=42):
    random.seed(seed)

def case_label(p_idx: int) -> str:
    return f"{p_idx}. pád" if 0 < p_idx < 7 else f"{p_idx}"

def normalize_completion(s: str) -> str:
    s = " ".join(s.strip().split())
    if not s:
        return s
    s = s[0].upper() + s[1:]
    if s[-1] not in ".?!":
        s += "."
    return s

def unique_key(*parts) -> str:
    return "|".join(map(str, parts))

def pick_template_for_case(pad_idx: int) -> str:
    return random.choice(CASE_TEMPLATES.get(pad_idx, ["{phrase}."]))

# -----------------------------------------------------------
# Heuristiky a bezpečné čtení tvarů
# -----------------------------------------------------------

def choose_cardinal_gender_key(zakladni_dict, noun_rod: str) -> str:
    # preferuj 'vse', jinak přesný rod, jinak první dostupný
    if "vse" in zakladni_dict:
        return "vse"
    if noun_rod in zakladni_dict:
        return noun_rod
    return next(iter(zakladni_dict.keys()))

def choose_ordinal_gender_key(radove_dict, noun_rod: str) -> str:
    # mapuj m_ziv/m_neziv na 'm', pokud není přesný klíč
    if noun_rod in radove_dict:
        return noun_rod
    if noun_rod in ("m_ziv", "m_neziv") and "m" in radove_dict:
        return "m"
    # fallback: první klíč
    return next(iter(radove_dict.keys()))

def is_singular_cardinal_key(cislo_key: str) -> bool:
    # singulár pro 'jeden' a složeniny s 'jedna' (např. dvacet_jedna)
    if cislo_key == "jeden":
        return True
    return "jedna" in cislo_key

def safe_get_noun_form(nouns, rod, lemma, cislo, pad_idx):
    try:
        return nouns[rod][lemma][cislo][pad_idx]
    except KeyError:
        return None

def safe_get_cislovka_form(cislovky, cislo_key, druh, rod_key, pad_idx):
    try:
        return cislovky[cislo_key][druh][rod_key][pad_idx]
    except KeyError:
        return None

def build_cardinal_phrase(cislovky, nouns, cislo_key, noun_rod, noun_lemma, pad_idx):
    if "zakladni" not in cislovky.get(cislo_key, {}):
        return None
    zak = cislovky[cislo_key]["zakladni"]
    rod_key = choose_cardinal_gender_key(zak, noun_rod)
    num_form = safe_get_cislovka_form(cislovky, cislo_key, "zakladni", rod_key, pad_idx)
    if not num_form:
        return None
    noun_num = "sg" if is_singular_cardinal_key(cislo_key) else "pl"
    noun_form = safe_get_noun_form(nouns, noun_rod, noun_lemma, noun_num, pad_idx)
    if not noun_form:
        return None
    return f"{num_form} {noun_form}", noun_num

def build_ordinal_phrase(cislovky, nouns, cislo_key, noun_rod, noun_lemma, noun_num, pad_idx):
    if "radove" not in cislovky.get(cislo_key, {}):
        return None
    rad = cislovky[cislo_key]["radove"]
    rod_key = choose_ordinal_gender_key(rad, noun_rod)
    ord_form = safe_get_cislovka_form(cislovky, cislo_key, "radove", rod_key, pad_idx)
    if not ord_form:
        return None
    noun_form = safe_get_noun_form(nouns, noun_rod, noun_lemma, noun_num, pad_idx)
    if not noun_form:
        return None
    return f"{ord_form} {noun_form}"

def phrase_to_sentence(phrase: str, pad_idx: int) -> str:
    return normalize_completion(pick_template_for_case(pad_idx).format(phrase=phrase))

# -----------------------------------------------------------
# Generátory úloh pro ČÍSLOVKY (ve stylu tvých funkcí)
# -----------------------------------------------------------

def generate_numeral_cardinal_tasks_balanced(cislovky, nouns, num_per_combo: int = 1):
    tasks = []
    seen = set()
    stats = Counter()
    for rod in nouns.keys():
        for lemma in nouns[rod].keys():
            for cislo_key in cislovky.keys():
                if "zakladni" not in cislovky[cislo_key]:
                    continue
                for pad_idx in CASE_INDEXES:
                    for _ in range(num_per_combo):
                        built = build_cardinal_phrase(cislovky, nouns, cislo_key, rod, lemma, pad_idx)
                        if not built:
                            continue
                        phrase, noun_num = built
                        key = unique_key("cardinal", cislo_key, rod, lemma, noun_num, pad_idx)
                        if key in seen:
                            continue
                        seen.add(key)

                        prompt = (
                            f"Napiš krátkou větu, ve které použiješ spojení '{phrase}'. "
                            f"Použij {pad_idx+1}. pád, rod {rod}."
                        )
                        completion = phrase_to_sentence(phrase, pad_idx)
                        tasks.append({"prompt": prompt, "completion": completion})
                        stats[("cardinal", pad_idx)] += 1
    return tasks, stats


def generate_numeral_ordinal_tasks_balanced(cislovky, nouns, num_per_combo: int = 1):
    tasks = []
    seen = set()
    stats = Counter()
    for rod in nouns.keys():
        for lemma in nouns[rod].keys():
            for cislo_key in cislovky.keys():
                if "radove" not in cislovky[cislo_key]:
                    continue
                for cislo_n in ["sg", "pl"]:
                    for pad_idx in CASE_INDEXES:
                        for _ in range(num_per_combo):
                            phrase = build_ordinal_phrase(cislovky, nouns, cislo_key, rod, lemma, cislo_n, pad_idx)
                            if not phrase:
                                continue
                            key = unique_key("ordinal", cislo_key, rod, lemma, cislo_n, pad_idx)
                            if key in seen:
                                continue
                            seen.add(key)

                            prompt = (
                                f"Napiš krátkou větu, ve které použiješ spojení '{phrase}'. "
                                f"Použij {pad_idx+1}. pád, {cislo_n} číslo, rod {rod}."
                            )
                            completion = phrase_to_sentence(phrase, pad_idx)
                            tasks.append({"prompt": prompt, "completion": completion})
                            stats[("ordinal", pad_idx)] += 1
    return tasks, stats


def generate_numeral_only_prompts(cislovky, num: int = 300):
    """
    „Only“ úlohy pro základní číslovky – použij izolovaný tvar číslovky ve větě (bez substantiva).
    Umožní modelu vidět i samostatné použití: 'Pět je málo.' / 'O třech se nemluvilo.'
    """
    prompts = []
    stats = Counter()
    for _ in range(num):
        cislo_key = random.choice(list(cislovky.keys()))
        if "zakladni" not in cislovky[cislo_key]:
            continue
        rod_key = random.choice(list(cislovky[cislo_key]["zakladni"].keys()))
        pad_idx = random.choice(CASE_INDEXES)
        num_form = safe_get_cislovka_form(cislovky, cislo_key, "zakladni", rod_key, pad_idx)
        if not num_form:
            continue

        prompt = f"Použij číslovku '{num_form}' v krátké české větě."
        # šablony bez substantiva
        templates = {
            0: [f"{num_form} stačí.", f"{num_form} je správně."],
            1: [f"Bez {num_form} to nepůjde.", f"Kolem {num_form} se točí debata."],
            2: [f"K {num_form} se přidali další.", f"Proti {num_form} nic nenamítal."],
            3: [f"Potřebuji {num_form}.", f"Vidím {num_form} před sebou."],
            4: [f"{num_form}, pojď dál!", f"{num_form}, počkej chvilku!"],
            5: [f"O {num_form} se mluvilo.", f"Na {num_form} záleží."],
            6: [f"S {num_form} to zvládneme.", f"Před {num_form} jsme se zastavili."]
        }
        completion = normalize_completion(random.choice(templates.get(pad_idx, [f"{num_form}."])))
        prompts.append({"prompt": prompt, "completion": completion})
        stats[("num_only", pad_idx)] += 1
    return prompts, stats


def generate_case_transform_prompts_cislovky(cislovky, nouns, num: int = 600):
    """
    Transformace pádů pro číslovky (míchá základní i řadové).
    Prompt dá zdrojové spojení a cílový pád; completion je věta s cílovým tvarem.
    """
    prompts = []
    stats = Counter()
    for _ in range(num):
        cislo_key = random.choice(list(cislovky.keys()))
        use_ordinal = "radove" in cislovky[cislo_key] and random.random() < 0.5
        src_idx, tgt_idx = random.sample(CASE_INDEXES, 2)

        # vyber substantivum
        rod = random.choice(list(nouns.keys()))
        lemma = random.choice(list(nouns[rod].keys()))

        if use_ordinal:
            cislo_n = random.choice(["sg", "pl"])
            src_phrase = build_ordinal_phrase(cislovky, nouns, cislo_key, rod, lemma, cislo_n, src_idx)
            tgt_phrase = build_ordinal_phrase(cislovky, nouns, cislo_key, rod, lemma, cislo_n, tgt_idx)
            typ = "řadovou číslovkou"
        else:
            built_src = build_cardinal_phrase(cislovky, nouns, cislo_key, rod, lemma, src_idx)
            built_tgt = build_cardinal_phrase(cislovky, nouns, cislo_key, rod, lemma, tgt_idx)
            if not built_src or not built_tgt:
                continue
            src_phrase, cislo_n = built_src
            tgt_phrase, _ = built_tgt
            typ = "základní číslovkou"

        if not src_phrase or not tgt_phrase:
            continue

        prompt = (
            f"Převeď '{src_phrase}' do {tgt_idx+1}. pádu a napiš krátkou českou větu s {typ}."
        )
        completion = phrase_to_sentence(tgt_phrase, tgt_idx)
        prompts.append({"prompt": prompt, "completion": completion})
        stats[("transform_num", tgt_idx)] += 1
    return prompts, stats


def generate_prep_sentence_prompts_cislovky(cislovky, nouns, num: int = 500):
    """
    Předložkový kontext pro číslovky (bez vokativu).
    """
    out = []
    stats = Counter()
    for _ in range(num):
        rod = random.choice(list(nouns.keys()))
        lemma = random.choice(list(nouns[rod].keys()))
        cislo_key = random.choice(list(cislovky.keys()))
        pad_idx = random.choice(CASE_INDEXES)
        if pad_idx == 4:  # vokativ přeskočíme
            continue
        preps = PREP_BY_CASE.get(pad_idx + 1, [])
        if not preps:
            continue
        prep = random.choice(preps)

        # zkus nejdřív řadové (adjektivní shoda), pak základní
        phrase = None
        if "radove" in cislovky[cislo_key] and random.random() < 0.5:
            cislo_n = random.choice(["sg", "pl"])
            phrase = build_ordinal_phrase(cislovky, nouns, cislo_key, rod, lemma, cislo_n, pad_idx)
        if not phrase and "zakladni" in cislovky[cislo_key]:
            built = build_cardinal_phrase(cislovky, nouns, cislo_key, rod, lemma, pad_idx)
            if built:
                phrase, _ = built
        if not phrase:
            continue

        prompt = f"Napiš větu, která začíná '{prep}' a pokračuje spojením '{phrase}'."
        completion = normalize_completion(f"{prep} {phrase} se konala schůzka.")
        out.append({"prompt": prompt, "completion": completion})
        stats[("prep_ctx_num", pad_idx)] += 1
    return out, stats


def generate_ab_choice_prompts_cislovky(cislovky, nouns, num: int = 300):
    """
    Výběrové úlohy A/B: správná vs. chybná shoda/pád/číslo.
    """
    out = []
    stats = Counter()
    for _ in range(num):
        rod = random.choice(list(nouns.keys()))
        lemma = random.choice(list(nouns[rod].keys()))
        cislo_key = random.choice(list(cislovky.keys()))
        pad_idx = random.choice(CASE_INDEXES)

        # rozhodni typ číslovky
        use_ordinal = "radove" in cislovky[cislo_key] and random.random() < 0.5

        if use_ordinal:
            cislo_n = random.choice(["sg", "pl"])
            correct_phrase = build_ordinal_phrase(cislovky, nouns, cislo_key, rod, lemma, cislo_n, pad_idx)
            if not correct_phrase:
                continue

            # špatná varianta: jiný pád nebo jiné číslo
            wrong = None
            wrong_pad = (pad_idx + random.choice([1, 2, 3])) % 7
            wrong = build_ordinal_phrase(cislovky, nouns, cislo_key, rod, lemma, cislo_n, wrong_pad)
            if not wrong:
                alt_num = "pl" if cislo_n == "sg" else "sg"
                wrong = build_ordinal_phrase(cislovky, nouns, cislo_key, rod, lemma, alt_num, pad_idx)
            if not wrong:
                continue
        else:
            built = build_cardinal_phrase(cislovky, nouns, cislo_key, rod, lemma, pad_idx)
            if not built:
                continue
            correct_phrase, noun_num = built

            wrong = None
            wrong_pad = (pad_idx + random.choice([1, 2, 3])) % 7
            wrong_built = build_cardinal_phrase(cislovky, nouns, cislo_key, rod, lemma, wrong_pad)
            if wrong_built:
                wrong, _ = wrong_built
            if not wrong:
                # zkuste změnit číslo substantiva (méně přirozené, ale odliší)
                alt_num = "pl" if noun_num == "sg" else "sg"
                wrong_form = safe_get_noun_form(nouns, rod, lemma, alt_num, pad_idx)
                zak = cislovky[cislo_key]["zakladni"]
                rod_key = choose_cardinal_gender_key(zak, rod)
                num_form = safe_get_cislovka_form(cislovky, cislo_key, "zakladni", rod_key, pad_idx)
                if num_form and wrong_form:
                    wrong = f"{num_form} {wrong_form}"
            if not wrong:
                continue

        options = [normalize_completion(correct_phrase), normalize_completion(wrong)]
        correct_is = random.choice([0, 1])
        if correct_is == 1:
            options.reverse()
        correct_letter = "A" if correct_is == 0 else "B"

        prompt = (
            f"Vyber správné spojení číslovky a podstatného jména pro {pad_idx+1}. pád, rod {rod}. "
            f"A: '{options[0]}', B: '{options[1]}'"
        )
        out.append({"prompt": prompt, "completion": correct_letter})
        stats[("choice_num", pad_idx)] += 1
    return out, stats

# -----------------------------------------------------------
# Export a reporting
# -----------------------------------------------------------

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
        if isinstance(p, int) and 0 <= p < 7:
            by_case[p] += n
    print("— Podle typu:")
    for t, n in by_type.most_common():
        print(f"   {t:>16}: {n}")
    print("— Podle pádu (index 0..6):")
    for p in range(7):
        print(f"   {p} -> {by_case.get(p, 0)}")

# -----------------------------------------------------------
# Hlavní běh: poskládání všech sad
# -----------------------------------------------------------

if __name__ == "__main__":
    set_seed(42)

    # POZN.: Očekává se, že:
    #  - proměnná `cislovky` je dostupná (např. import z tvého souboru),
    #  - proměnná `nouns` je dostupná (tvůj slovník tvarů podst. jmen).
    # Zde si je pouze importuj/načti dle tvého projektu, např.:
    #
    # from cislovky_data import cislovky
    # import json
    # nouns = json.load(open("nouns.json", "r", encoding="utf-8"))

    try:
        cislovky
    except NameError:
        raise RuntimeError("Proměnná `cislovky` není definovaná. Importuj ji z původního skriptu.")

    try:
        nouns
    except NameError:
        raise RuntimeError("Proměnná `nouns` není definovaná. Načti svůj slovník podstatných jmen.")

    all_tasks = []
    all_stats = Counter()

    # Základní číslovky – větné užití se správným pádem a číslem substantiva
    tasks1, stats1 = generate_numeral_cardinal_tasks_balanced(cislovky, nouns, num_per_combo=1)
    all_tasks += tasks1
    all_stats += stats1

    # Řadové číslovky – adjektivní shoda v různých pádech a číslech
    tasks2, stats2 = generate_numeral_ordinal_tasks_balanced(cislovky, nouns, num_per_combo=1)
    all_tasks += tasks2
    all_stats += stats2

    # Pouze číslovka ve větě (bez substantiva) – rozšíření kontextu
    tasks3, stats3 = generate_numeral_only_prompts(cislovky, num=300)
    all_tasks += tasks3
    all_stats += stats3

    # Transformace mezi pády (základní i řadové)
    tasks4, stats4 = generate_case_transform_prompts_cislovky(cislovky, nouns, num=600)
    all_tasks += tasks4
    all_stats += stats4

    # Předložkový kontext (bez vokativu)
    tasks5, stats5 = generate_prep_sentence_prompts_cislovky(cislovky, nouns, num=500)
    all_tasks += tasks5
    all_stats += stats5

    # Výběrové A/B
    tasks6, stats6 = generate_ab_choice_prompts_cislovky(cislovky, nouns, num=400)
    all_tasks += tasks6
    all_stats += stats6

    # Export
    write_jsonl("Cislovky_dataset.jsonl", all_tasks)
    print_report(all_stats)