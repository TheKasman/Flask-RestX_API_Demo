CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  item_type TEXT NOT NULL CHECK(item_type IN ('weapon', 'armor', 'healing', 'misc')),
  rarity TEXT NOT NULL CHECK(rarity IN ('common', 'uncommon', 'rare', 'epic', 'legendary')),
  value_gold INTEGER NOT NULL,
  weight REAL NOT NULL
);

CREATE TABLE weapon_stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  damage_dice TEXT NOT NULL,
  damage_type TEXT NOT NULL,
  crit_range INTEGER NOT NULL DEFAULT 20,
  FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE armor_stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  armor_class INTEGER NOT NULL,
  armor_type TEXT NOT NULL CHECK(armor_type IN ('light', 'medium', 'heavy')),
  FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE healing_stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  heal_dice TEXT NOT NULL,
  uses_remaining INTEGER NOT NULL,
  FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE INDEX idx_items_type ON items(item_type);
