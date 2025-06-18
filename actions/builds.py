import time
import json
import os
import pyautogui
from core.window import get_game_window_bounds

BUILDINGS_COORDS_FILE = "data/buildings_coords.json"

def click_building_button(building_id, button_name, bounds, delay=1.0):
    """
    Clique sur le bouton spécifié d'un bâtiment enregistré dans le JSON.
    """
    if not os.path.exists(BUILDINGS_COORDS_FILE):
        print("Aucune coordonnée de bâtiment enregistrée.")
        return False

    with open(BUILDINGS_COORDS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if building_id not in data or button_name not in data[building_id]:
        print(f"Bâtiment '{building_id}' ou bouton '{button_name}' non trouvé dans le JSON.")
        return False

    rel_x = data[building_id][button_name]["rel_x"]
    rel_y = data[building_id][button_name]["rel_y"]
    x, y, w, h = bounds
    abs_x = int(x + rel_x * w)
    abs_y = int(y + rel_y * h)
    print(f"🖱️ Clic sur '{building_id}' [{button_name}] à ({abs_x}, {abs_y})")
    pyautogui.moveTo(abs_x, abs_y, duration=0.3)
    pyautogui.click()
    time.sleep(delay)
    return True

def train_siege_units():
    """
    Ouvre l'atelier de siège et tente de lancer la formation de troupes.
    """
    bounds = get_game_window_bounds("Rise")
    if not bounds:
        print("Impossible de détecter la fenêtre du jeu.")
        return

    # Clique sur l'atelier de siège (siege_workshop)
    if not click_building_button("siege_workshop", "building", bounds):
        return

    # Clique sur le bouton "utiliser" (ou "former")
    time.sleep(1)
    if not click_building_button("siege_workshop", "use", bounds):
        return
    
    time.sleep(1)
    if not click_building_button("siege_workshop", "t1", bounds):
        return

    time.sleep(1)
    if not click_building_button("siege_workshop", "train", bounds):
        return
    time.sleep(1)

