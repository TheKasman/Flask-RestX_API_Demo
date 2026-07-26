import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).parent / "rpg_items.sqlite3"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"
NUM_ITEMS = 300

WEAPON_PREFIXES = [
    "Rusty",
    "Iron",
    "Steel",
    "Silver",
    "Enchanted",
    "Ancient",
    "Cursed",
    "Blessed",
]
WEAPON_NAMES = ["Sword", "Axe", "Dagger", "Mace", "Spear", "Bow", "Warhammer", "Flail"]
ARMOR_PREFIXES = ["Tattered", "Leather", "Chainmail", "Plated", "Reinforced", "Royal"]
ARMOR_NAMES = ["Helmet", "Chestplate", "Gauntlets", "Boots", "Shield", "Greaves"]
HEALING_NAMES = ["Potion", "Mega Potion", "X-Potion", "Elixir"]
RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]
DAMAGE_TYPES = ["Slashing", "Piercing", "Impact", "Fire", "Cold"]
ARMOR_TYPES = ["light", "medium", "heavy"]


def build_database():
    if DB_PATH.exists():
        DB_PATH.unlink()  # FRESH BUILD EVERY TIME.

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(SCHEMA_PATH.read_text())

    for _ in range(NUM_ITEMS):
        # Randomise the item type
        item_type = random.choices(
            ["weapon", "armor", "healing", "misc"], weights=[35, 35, 20, 10]
        )[0]
        rarity = random.choice(RARITIES)
        value = random.randint(5, 5000)
        weight = round(random.uniform(0.1, 25.0), 2)

        if item_type == "weapon":
            name = f"{random.choice(WEAPON_PREFIXES)} {random.choice(WEAPON_NAMES)}"
        elif item_type == "armor":
            name = f"{random.choice(ARMOR_PREFIXES)} {random.choice(ARMOR_NAMES)}"
        elif item_type == "healing":
            name = random.choice(HEALING_NAMES)
        else:
            name = "Mysterious Trinket"

        # Slap the item and its randomly generated properties together, ready to be written to the database
        cur.execute(
            "INSERT INTO items (name, item_type, rarity, value_gold, weight) VALUES (?, ?, ?, ?, ?)",
            (
                name, item_type, rarity, value, weight
            )
        )
        item_id = cur.lastrowid

        if item_type == "weapon":
            dice = random.choice(["1d4", "1d6", "1d8", "1d10", "2d6"])
            cur.execute(
                "INSERT INTO weapon_stats (item_id, damage_dice, damage_type, crit_range) VALUES (?, ?, ?, ?)",
                (
                    item_id,
                    dice,
                    random.choice(DAMAGE_TYPES),
                    random.choice([18, 19, 20]),
                ),
            )
        elif item_type == "armor":
            ac = random.randint(10, 20)
            cur.execute(
                "INSERT INTO armor_stats (item_id, armor_class, armor_type) VALUES (?, ?, ?)",
                (
                    item_id,
                    ac,
                    random.choice(ARMOR_TYPES),
                ),
            )
        elif item_type == "healing":
            heal_dice = random.choice(["1d4+1", "2d4", "2d4+2", "4d4+4"])
            cur.execute(
                "INSERT INTO healing_stats (item_id, heal_dice, uses_remaining) VALUES (?, ?, ?)",
                (item_id, heal_dice, random.randint(1, 3)),
            )
    # Write it to the database
    conn.commit()
    conn.close()

    # ALL DONE!
    print(f"Seeded {NUM_ITEMS} items into {DB_PATH}")


if __name__ == "__main__":
    build_database()
