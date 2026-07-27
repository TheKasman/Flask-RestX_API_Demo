from flask_restx import Namespace, Resource
from shared.models import SessionLocal, Item
import requests

ns = Namespace("items", description="RPG item opeerations")
MOCK_API_URL = "http://localhost:9000"

@ns.route("/<int:item_id>/roll")
class ItemRoll(Resource):
    def get(self, item_id):
        import time as time_module
        print(f"[FLASK] Request received at {time_module.time():.2f}")

        session = SessionLocal()
        try:
            item = session.query(Item).filter(Item.id == item_id).first()
            if item is None:
                return {"error": "Item not found"}, 404

            dice = None
            if item.item_type == "weapon" and item.weapon_stats:
                dice = item.weapon_stats.damage_dice
            elif item.item_type == "healing" and item.healing_stats:
                dice = item.healing_stats.heal_dice

            if dice is None:
                return {"error": "This item type has no rollable dice"}, 400

            response = requests.get(f"{MOCK_API_URL}/roll/{dice}")
            roll_result = response.json()

            return {
                "item_id": item.id,
                "item_name": item.name,
                "dice": dice,
                "roll_result": roll_result["result"],
            }
        finally:
            session.close()

@ns.route("/")
class ItemList(Resource):
    def get(self):
        session = SessionLocal()
        try:
            items = session.query(Item).limit(20).all()
            return [
                {"id": i.id, "name": i.name, "item_type": i.item_type, "rarity": i.rarity}
                for i in items
            ]
        finally:
            session.close()

@ns.route("/<int:item_id>")
class ItemDetail(Resource):
    def get(self, item_id):
        session = SessionLocal()
        try:
            # GIVE ME THE THING PLEASE
            item = session.query(Item).filter(Item.id == item_id).first()
            if item is None:
                return {"error": "Item not found"}, 404

            stats = None

            # FORMAT NICELY PLEASE. THE USE OF ALL CAPS IS DEFINITELY NOT PASSIVE AGGRESSIVE
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
