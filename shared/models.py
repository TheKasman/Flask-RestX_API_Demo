from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, realtionship, sessionmaker
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

    weapon_stats = realtionship("WeaponStats", back_populates="item", uselist=False)
    armor_stats = realtionship("ArmorStats", back_populates="item", uselist=False)
    healing_stats = realtionship("HealingStats", back_populates="item", uselist=False)
