# backend/workers/duplicate_card_detector.py

import os
import json
import difflib
import re


DATA_PATH = "backend/data/cards"


# -------------------------
# normalize card name
# -------------------------

def normalize_name(name: str):

    name = name.lower()

    name = re.sub(r"\bcredit card\b", "", name)

    name = re.sub(r"\bcard\b", "", name)

    name = re.sub(r"\bbank\b", "", name)

    name = re.sub(r"\bcc\b", "", name)

    name = re.sub(r"\d+", "", name)

    name = re.sub(r"\s+", " ", name)

    return name.strip()


# -------------------------
# similarity
# -------------------------

def similarity(a, b):

    return difflib.SequenceMatcher(

        None,

        a,

        b

    ).ratio()


# -------------------------
# load cards
# -------------------------

def load_all_cards():

    cards = []

    for issuer in os.listdir(DATA_PATH):

        issuer_path = os.path.join(

            DATA_PATH,

            issuer

        )

        if not os.path.isdir(issuer_path):

            continue

        for file in os.listdir(issuer_path):

            if not file.endswith(".json"):

                continue

            path = os.path.join(

                issuer_path,

                file

            )

            with open(path) as f:

                card = json.load(f)

            cards.append({

                "card_id": card["card_id"],

                "card_name": card["card_name"],

                "issuer": card["issuer"],

                "path": path

            })

    return cards


# -------------------------
# ignore low quality names
# -------------------------

def is_generic(name):

    generic_words = [

        "test",

        "sample",

        "demo",

        "card"

    ]

    return any(

        word in name.lower()

        for word in generic_words

    )


# -------------------------
# find duplicates
# -------------------------

def find_duplicates(threshold=0.93):

    cards = load_all_cards()

    duplicates = []

    for i in range(len(cards)):

        for j in range(i+1, len(cards)):

            c1 = cards[i]

            c2 = cards[j]

            # skip test issuer
            if c1["issuer"] == "test":
                continue

            if c2["issuer"] == "test":
                continue

            name1 = normalize_name(c1["card_name"])

            name2 = normalize_name(c2["card_name"])

            # skip generic names
            if is_generic(name1) or is_generic(name2):
                continue

            # only compare same issuer
            if c1["issuer"] != c2["issuer"]:
                continue

            score = similarity(name1, name2)

            if score >= threshold:

                duplicates.append({

                    "card_1": c1["card_id"],

                    "card_2": c2["card_id"],

                    "similarity": round(score, 3)

                })

    return duplicates
