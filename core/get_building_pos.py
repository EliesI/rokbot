import json
import os
from pynput import mouse

BUILDINGS_FILE = "data/buildings_coords.json"
BUILDINGS_LIST_FILE = "data/buildings_list.json"

def load_buildings_list():
    with open(BUILDINGS_LIST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def choose_building(buildings):
    print("Sélectionnez le bâtiment à enregistrer :")
    for idx, b in enumerate(buildings):
        print(f"{idx+1}. {b['label']} ({b['id']})")
    while True:
        try:
            choice = int(input("Numéro du bâtiment : "))
            if 1 <= choice <= len(buildings):
                return buildings[choice-1]
        except ValueError:
            pass
        print("Choix invalide.")

def choose_button(building_type):
    boutons = ["building", "upgrade", "use"]
    if building_type == "military":
        boutons += ["t1", "t2", "t3", "t4", "train"]
    print("Quel bouton veux-tu enregistrer ?")
    for idx, b in enumerate(boutons):
        print(f"{idx+1}. {b}")
    while True:
        try:
            choice = int(input("Numéro du bouton : "))
            if 1 <= choice <= len(boutons):
                return boutons[choice-1]
        except ValueError:
            pass
        print("Choix invalide.")

def save_building_coord(building_name, button_name, bounds, click_x, click_y):
    x, y, w, h = bounds
    rel_x = (click_x - x) / w
    rel_y = (click_y - y) / h

    if os.path.exists(BUILDINGS_FILE):
        with open(BUILDINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    if building_name not in data:
        data[building_name] = {}

    data[building_name][button_name] = {"rel_x": rel_x, "rel_y": rel_y}

    with open(BUILDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Coordonnées relatives enregistrées pour {building_name} [{button_name}] : ({rel_x:.3f}, {rel_y:.3f})")

def wait_for_click():
    print("Cliquez sur le bouton à enregistrer...")

    pos = []

    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            pos.append((x, y))
            return False  # Stop listener

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    return pos[0]

def main():
    from window import get_game_window_bounds
    buildings = load_buildings_list()
    building = choose_building(buildings)
    building_id = building["id"]
    building_type = building.get("type", "")
    button_name = choose_button(building_type)
    bounds = get_game_window_bounds("Rise")
    if not bounds:
        print("Impossible de détecter la fenêtre du jeu.")
        return
    click_x, click_y = wait_for_click()
    save_building_coord(building_id, button_name, bounds, click_x, click_y)

if __name__ == "__main__":
    main()

