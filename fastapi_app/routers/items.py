from fastapi import APIRouter, HTTPException
import httpx

from shared.models import SessionLocal, Item

router = APIRouter()
MOCK_API_URL = "http://localhost:9000"


#Same implementation like in flask_app but a little different
@router.get("/")
def list_items():
    session = SessionLocal()
    try:
        items = session.query(Item).limit(20).all()
        return [
            {"id": i.id, "name": i.name, "item_type": i.item_type, "rarity": i.rarity}
            for i in items
        ]
    finally:
        session.close()

@router.get("/{item_id}")
def get_item(item_id: int):
    session = SessionLocal()
    try:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        stats = None
        if item.item_type == "weapon" and item.weapon_stats:
            stats = {
                "damage_dice": item.weapon_stats.damage_dice,
                "damage_type": item.weapon_stats.damage_type,
                "crit_range": item.weapon_stats.crit_range,
            }
        elif item.item_type == "armor" and item.armor_stats:
            stats = {
                "armor_class": item.armor_stats.armor_class,
                "armor_type": item.armor_stats.armor_type,
            }
        elif item.item_type == "healing" and item.healing_stats:
            stats = {
                "heal_dice": item.healing_stats.heal_dice,
                "uses_remaining": item.healing_stats.uses_remaining,
            }

        return {
            "id": item.id,
            "name": item.name,
            "item_type": item.item_type,
            "rarity": item.rarity,
            "value_gold": item.value_gold,
            "weight": item.weight,
            "stats": stats,
        }
    finally:
        session.close()

#Roll_Item is now async O_O
# WE WILL HAVE AN EVENT LOOP NOW
@router.get("/{item_id}/roll")
async def roll_item(item_id: int):
    session = SessionLocal()
    try:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        dice = None
        if item.item_type == "weapon" and item.weapon_stats:
            dice = item.weapon_stats.damage_dice
        elif item.item_type == "healing" and item.healing_stats:
            dice = item.healing_stats.heal_dice

        if dice is None:
            raise HTTPException(status_code=400, detail="This item type has no rollable dice")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{MOCK_API_URL}/roll/{dice}")
            roll_result = response.json()

        return {
            "item_id": item.id,
            "item_name": item.name,
            "dice": dice,
            "roll_result": roll_result["result"],
        }
    finally:
        session.close()
