# ============================================================
# Vidhi-AI | IPC-to-BNS Deterministic Mapping
# ============================================================
# Comprehensive mapping of Indian Penal Code (1860) section numbers
# to their Bharatiya Nyaya Sanhita (2023) equivalents.
# This replaces unreliable semantic search for IPC number lookups.
# Source: Ministry of Law & Justice gazette notifications.
# ============================================================

import re


# ── IPC-to-BNS Deterministic Mapping ────────────────────────────────
IPC_TO_BNS = {
    # Chapter II - General Explanations (IPC 6-52 → BNS 2-22)
    # Chapter III - Punishments (IPC 53-75 → BNS 4-16)
    # Chapter IV - General Exceptions (IPC 76-106 → BNS 14-44)
    # Chapter V - Abetment (IPC 107-120)
    "107": "45", "108": "46", "109": "47", "110": "48",
    "111": "49", "112": "50", "113": "51", "114": "52",
    "115": "53", "116": "54", "117": "55", "118": "56",
    "119": "57", "120": "58",
    # Criminal Conspiracy
    "120A": "60", "120B": "61",
    # Chapter VI - Offences against the State (IPC 121-130)
    "121": "147", "121A": "148", "122": "149", "123": "150",
    "124": "151", "124A": "152", "125": "153", "126": "154",
    "127": "154", "128": "155", "129": "155", "130": "156",
    # Chapter VII - Army/Navy/Air Force (IPC 131-140)
    "131": "157", "132": "158", "133": "159", "134": "160",
    "135": "161", "136": "162", "137": "163", "138": "164",
    "139": "165", "140": "166",
    # Chapter VIII - Offences Against Public Tranquillity
    "141": "189", "142": "189", "143": "189", "144": "190",
    "145": "191", "146": "191", "147": "191", "148": "192",
    "149": "190", "150": "193", "151": "194", "152": "195",
    "153": "196", "153A": "196", "153B": "197", "154": "194",
    "155": "193", "156": "194", "157": "194", "158": "194",
    "159": "195", "160": "198",
    # Chapter IX - Offences by Public Servants (IPC 161-171)
    "161": "199", "162": "199", "163": "199", "164": "199",
    "165": "199", "165A": "200", "166": "200", "166A": "200",
    "166B": "201", "167": "202", "168": "203", "169": "204",
    "170": "205", "171": "206",
    # Chapter IXA - Elections (IPC 171A-171I)
    "171A": "169", "171B": "170", "171C": "171", "171D": "172",
    "171E": "173", "171F": "174", "171G": "175", "171H": "176",
    "171I": "177",
    # Chapter X - Contempts of Courts (IPC 172-190)
    "172": "207", "173": "208", "174": "209", "174A": "210",
    "175": "211", "176": "212", "177": "213", "178": "214",
    "179": "215", "180": "216", "181": "217", "182": "218",
    "183": "219", "184": "220", "186": "221", "187": "222",
    "188": "223", "189": "224", "190": "225",
    # Chapter XI - False Evidence (IPC 191-229)
    "191": "229", "192": "230", "193": "232", "194": "233",
    "195": "234", "195A": "235", "196": "236", "197": "236",
    "198": "237", "199": "237", "200": "238", "201": "239",
    "202": "240", "203": "241", "204": "242", "205": "243",
    "206": "244", "207": "245", "208": "246", "209": "247",
    "210": "248", "211": "250", "212": "251", "213": "252",
    "214": "253", "215": "254", "216": "255", "216A": "256",
    "216B": "256", "217": "257", "218": "258", "219": "259",
    "220": "260", "221": "261", "222": "261", "223": "262",
    "224": "260", "225": "261", "225A": "262", "225B": "263",
    "226": "264", "227": "264", "228": "265", "228A": "72",
    "229": "266",
    # Chapter XII - Coin & Stamps (IPC 230-263A)
    "230": "178", "231": "178", "232": "178", "233": "179",
    "234": "179", "235": "180", "236": "180", "237": "180",
    "238": "181", "239": "181", "240": "181", "241": "181",
    "242": "181", "243": "181", "244": "182", "245": "182",
    "246": "182", "247": "183", "248": "183", "249": "183",
    "250": "184", "251": "184", "252": "185", "253": "185",
    "254": "186", "255": "186", "256": "187", "257": "187",
    "258": "188", "259": "188", "260": "188", "261": "188",
    "262": "188", "263": "188", "263A": "188",
    # Chapter XIV - Public Health/Safety (IPC 268-294)
    "268": "270", "269": "271", "270": "272", "271": "273",
    "272": "274", "273": "275", "274": "276", "275": "277",
    "276": "278", "277": "279", "278": "280", "279": "281",
    "280": "282", "281": "283", "282": "284", "283": "285",
    "284": "286", "285": "287", "286": "288", "287": "289",
    "288": "290", "289": "291", "290": "292", "291": "293",
    "292": "294", "293": "295", "294": "296",
    # Chapter XV - Offences Relating to Religion (IPC 295-298)
    "295": "297", "295A": "299", "296": "298", "297": "300",
    "298": "301",
    # Chapter XVI - Offences Affecting Life (IPC 299-377)
    "299": "100", "300": "101", "301": "102", "302": "103",
    "303": "103", "304": "105", "304A": "106", "304B": "80",
    "305": "107", "306": "108", "307": "109", "308": "110",
    "309": "226",
    # Causing Miscarriage (IPC 312-318)
    "312": "88", "313": "89", "314": "90", "315": "91",
    "316": "92", "317": "93", "318": "94",
    # Hurt (IPC 319-338)
    "319": "114", "320": "114", "321": "115", "322": "117",
    "323": "115", "324": "118", "325": "117", "326": "118",
    "326A": "124", "326B": "125",
    "327": "119", "328": "123", "329": "120", "330": "121",
    "331": "122", "332": "121", "333": "122", "334": "115",
    "335": "117", "336": "125", "337": "125", "338": "126",
    # Wrongful Restraint & Confinement (IPC 339-348)
    "339": "127", "340": "127", "341": "127", "342": "127",
    "343": "128", "344": "129", "345": "130", "346": "131",
    "347": "132", "348": "133",
    # Criminal Force & Assault (IPC 349-358)
    "349": "130", "350": "131", "351": "132", "352": "133",
    "353": "132", "354": "74", "354A": "75", "354B": "76",
    "354C": "77", "354D": "78", "355": "134", "356": "133",
    "357": "135", "358": "133",
    # Kidnapping & Abduction (IPC 359-374)
    "359": "136", "360": "136", "361": "136", "362": "136",
    "363": "137", "363A": "141", "364": "138", "364A": "140",
    "365": "137", "366": "139", "366A": "139", "366B": "139",
    "367": "142", "368": "138", "369": "137",
    "370": "143", "371": "144", "372": "145", "373": "146",
    "374": "144",
    # Sexual Offences (IPC 375-376E)
    "375": "63", "376": "64", "376A": "66", "376AB": "65",
    "376B": "67", "376C": "68", "376D": "70", "376DA": "70",
    "376DB": "70", "376E": "71",
    # Theft (IPC 378-382)
    "378": "303", "379": "303", "380": "305", "381": "305",
    "382": "305",
    # Extortion (IPC 383-389)
    "383": "308", "384": "308", "385": "308", "386": "308",
    "387": "308", "388": "308", "389": "308",
    # Robbery & Dacoity (IPC 390-402)
    "390": "309", "391": "310", "392": "309", "393": "309",
    "394": "309", "395": "310", "396": "310", "397": "311",
    "398": "312", "399": "312", "400": "313", "401": "314",
    "402": "315",
    # Criminal Misappropriation & Breach of Trust (IPC 403-409)
    "403": "316", "404": "316", "405": "316", "406": "316",
    "407": "316", "408": "316", "409": "316",
    # Stolen Property (IPC 410-414)
    "410": "317", "411": "317", "412": "317", "413": "317",
    "414": "317",
    # Cheating (IPC 415-424)
    "415": "318", "416": "319", "417": "318", "418": "318",
    "419": "319", "420": "318", "421": "320", "422": "321",
    "423": "322", "424": "323",
    # Mischief (IPC 425-440)
    "425": "324", "426": "324", "427": "324", "428": "325",
    "429": "325", "430": "326", "431": "326", "432": "326",
    "433": "326", "434": "326", "435": "326", "436": "327",
    "437": "327", "438": "328", "439": "328", "440": "328",
    # Criminal Trespass (IPC 441-462)
    "441": "329", "442": "330", "443": "330", "444": "330",
    "445": "331", "446": "332", "447": "329", "448": "331",
    "449": "332", "450": "333", "451": "333", "452": "333",
    "453": "334", "454": "334", "455": "335", "456": "335",
    "457": "331", "458": "332", "459": "333", "460": "334",
    "461": "335", "462": "335",
    # Forgery (IPC 463-489E)
    "463": "336", "464": "337", "465": "338", "466": "338",
    "467": "338", "468": "338", "469": "339", "470": "340",
    "471": "340", "472": "341", "473": "341", "474": "342",
    "475": "343", "476": "344", "477": "344", "477A": "345",
    "478": "346", "479": "346", "480": "347", "481": "347",
    "482": "348", "483": "349", "484": "349", "485": "349",
    "486": "349", "487": "350", "488": "350", "489": "350",
    "489A": "178", "489B": "179", "489C": "180", "489D": "181",
    "489E": "182",
    # Marriage Offences (IPC 493-498A)
    "493": "81", "494": "82", "495": "83", "496": "84",
    "497": "84", "498": "84", "498A": "85",
    # Defamation (IPC 499-502)
    "499": "356", "500": "356", "501": "357", "502": "358",
    # Criminal Intimidation & Insult (IPC 503-510)
    "503": "351", "504": "352", "505": "353", "506": "351",
    "507": "351", "508": "352", "509": "79", "510": "355",
    # Attempt (IPC 511)
    "511": "62",
}


# ── IPC Section Names ───────────────────────────────────────────────
IPC_NAMES = {
    "107": "Abetment", "120B": "Criminal Conspiracy",
    "124A": "Sedition", "141": "Unlawful Assembly",
    "147": "Rioting", "153A": "Promoting Enmity",
    "171B": "Bribery at Elections",
    "182": "False Information to Public Servant",
    "191": "False Evidence", "193": "Punishment for False Evidence",
    "201": "Causing Disappearance of Evidence",
    "279": "Rash Driving", "292": "Obscene Material",
    "295A": "Outraging Religious Feelings",
    "299": "Culpable Homicide", "300": "Murder",
    "302": "Punishment for Murder", "304": "Culpable Homicide Punishment",
    "304A": "Death by Negligence", "304B": "Dowry Death",
    "306": "Abetment of Suicide", "307": "Attempt to Murder",
    "308": "Attempt to Culpable Homicide",
    "309": "Attempt to Suicide",
    "319": "Hurt", "320": "Grievous Hurt",
    "323": "Voluntarily Causing Hurt",
    "324": "Hurt by Dangerous Weapons",
    "326": "Grievous Hurt by Dangerous Weapons",
    "326A": "Acid Attack", "354": "Assault on Woman",
    "354A": "Sexual Harassment", "354D": "Stalking",
    "363": "Kidnapping", "364A": "Kidnapping for Ransom",
    "370": "Trafficking", "375": "Rape",
    "376": "Punishment for Rape", "376D": "Gang Rape",
    "378": "Theft", "379": "Punishment for Theft",
    "380": "Theft in Dwelling House",
    "383": "Extortion", "384": "Punishment for Extortion",
    "390": "Robbery", "391": "Dacoity",
    "392": "Punishment for Robbery",
    "395": "Punishment for Dacoity",
    "397": "Robbery/Dacoity with Attempt to Cause Death",
    "403": "Dishonest Misappropriation",
    "405": "Criminal Breach of Trust",
    "406": "Punishment for Criminal Breach of Trust",
    "409": "CBT by Public Servant",
    "411": "Receiving Stolen Property",
    "415": "Cheating", "417": "Punishment for Cheating",
    "420": "Cheating and Dishonestly Inducing Delivery",
    "425": "Mischief", "435": "Mischief by Fire",
    "436": "Mischief by Fire to Destroy House",
    "441": "Criminal Trespass", "447": "Punishment for Trespass",
    "448": "House-Trespass",
    "463": "Forgery", "465": "Punishment for Forgery",
    "467": "Forgery of Valuable Security",
    "468": "Forgery for Purpose of Cheating",
    "471": "Using Forged Document",
    "477A": "Falsification of Accounts",
    "489A": "Counterfeiting Currency",
    "494": "Bigamy", "498A": "Cruelty by Husband/Relatives",
    "499": "Defamation", "500": "Punishment for Defamation",
    "503": "Criminal Intimidation",
    "504": "Insult to Provoke Breach of Peace",
    "505": "Public Mischief",
    "506": "Punishment for Criminal Intimidation",
    "509": "Insult to Modesty of Woman",
    "511": "Attempt to Commit Offences",
}


def lookup_ipc_to_bns(ipc_num: str, csv_rows: list) -> list:
    """Given an IPC section number, find the corresponding BNS
    section(s) using the deterministic mapping table, then fetch
    full details from the CSV data.

    Returns a list of matched row dicts (with full descriptions).
    Falls back to empty list if IPC number not in mapping.
    """
    bns_num = IPC_TO_BNS.get(ipc_num)
    if not bns_num:
        # Try without trailing letter for alphanumeric (e.g. 304A)
        # Already handled — alphanumeric keys are in the dict
        return []

    matched = []
    for row in csv_rows:
        if row["section"] == bns_num:
            matched.append(row)

    # If exact match not found, try startswith (for sub-sections)
    if not matched:
        for row in csv_rows:
            if row["section"].startswith(bns_num):
                matched.append(row)

    return matched


def get_ipc_section_name(ipc_num: str) -> str:
    """Return a human-readable name for common IPC sections."""
    return IPC_NAMES.get(ipc_num, f"IPC Section {ipc_num}")


def contextual_rerank(query: str, rows: list) -> list:
    """Re-rank matched BNS rows by checking if contextual keywords
    from the user query appear in Section_name or Description.

    Keywords like 'attempt', 'conspiracy', 'abetment', 'negligence',
    'grievous', 'culpable', 'dowry', 'kidnapping', 'extortion' etc.
    are checked. Rows containing those words are boosted to the top.
    """
    # Contextual keywords that commonly cause retrieval overlap
    CONTEXT_KEYWORDS = [
        "attempt", "conspiracy", "abetment", "abet",
        "negligence", "negligent", "grievous", "culpable",
        "dowry", "kidnapping", "kidnap", "extortion",
        "robbery", "dacoity", "forgery", "fraud",
        "cheating", "theft", "assault", "hurt",
        "mischief", "trespass", "defamation", "sedition",
        "rioting", "affray", "bribery", "corruption",
    ]

    query_lower = query.lower()
    # Find which context keywords appear in the user query
    active_keywords = [
        kw for kw in CONTEXT_KEYWORDS
        if re.search(r'\b' + re.escape(kw) + r'\b', query_lower)
    ]

    if not active_keywords:
        return rows  # No contextual filtering needed

    def keyword_score(row):
        """Count how many active keywords appear in section name
        and description."""
        text = (
            row.get("section_name", "") + " " +
            row.get("description", "")
        ).lower()
        hits = 0
        for kw in active_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                hits += 1
        return hits

    # Sort: rows with more keyword hits come first, then preserve
    # original order (which is by relevance score) as tiebreaker
    return sorted(rows, key=lambda r: keyword_score(r), reverse=True)
