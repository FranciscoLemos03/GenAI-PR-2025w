import os

# Path to genai/data folder
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "genai", "data")
)

os.makedirs(BASE_DIR, exist_ok=True)


def get_room_db_path(room_id: str) -> str:
    safe_room = room_id.replace("/", "_")
    return os.path.join(BASE_DIR, f"{safe_room}-database.json")