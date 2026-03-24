import json
import glob

FILES = glob.glob("backend/data/cards/**/*.json", recursive=True)

for path in FILES:
    with open(path) as f:
        card = json.load(f)

    if card["earn_rules"]:
        continue

    card["earn_rules"] = [{
        "category": "others",
        "reward_rate": 0.01,
        "reward_unit": card["reward_type"]
    }]

    with open(path, "w") as f:
        json.dump(card, f, indent=2)

print("Default rules added")
