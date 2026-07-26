from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pathlib import Path

Base = declarative_base()

DB_PATH = Path(__file__).parent / "rpg_items.sqlite3"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    item_type = Column(String, nullable=False)
    rarity = Column(String, nullable=False)
    value_gold = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)

    weapon_stats = relationship("WeaponStats", back_populates="item", uselist=False)
    armor_stats = relationship("ArmorStats", back_populates="item", uselist=False)
    healing_stats = relationship("HealingStats", back_populates="item", uselist=False)

class WeaponStats(Base):
    __tablename__ = "weapon_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    damage_dice = Column(String, nullable=False)
    damage_type = Column(String, nullable=False)
    crit_range = Column(Integer, nullable=False, default=20)

    item = relationship("Item", back_populates="weapon_stats")

class ArmorStats(Base):
    __tablename__ = "armor_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    armor_class = Column(Integer, nullable=False)
    armor_type = Column(String, nullable=False)

    item = relationship("Item", back_populates="armor_stats")

class HealingStats(Base):
    __tablename__ = "healing_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    heal_dice = Column(String, nullable=False)
    uses_remaining = Column(Integer, nullable=False)

    item = relationship("Item", back_populates="healing_stats")
