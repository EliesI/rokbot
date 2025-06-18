import time
import pyautogui
from core.memory import load_memory, add_node, is_node_collected
from core.ocr_utils import get_game_coords
from core.vision import click_template
from datetime import datetime, timedelta

from core.window import focus_game_window, get_game_window_bounds


def balayage_gemmes(bounds, lignes=5, delay=1.0, threshold=0.85):
    x_left = bounds[0] + 150
    x_right = bounds[0] + bounds[2] - 200
    y = bounds[1] + bounds[3] // 2  # Ligne horizontale fixe
    y1 = bounds[1] + 100
    y2 = bounds[3] - 100


    print(f"🔍 Balayage de la carte de {x_left} à {x_right} à y = {y}")
    print(f"  Dimensions de la fenêtre : {bounds[2]}x{bounds[3]}")
    print(f"  Nombre de lignes à balayer : {lignes}")
    print(f"  Y1 = {bounds[1]}, Y2 = {bounds[3]}")


    y_precedent = bounds[1] + bounds[3] // 2  # y initial au centre

    for i in range(lignes):
        # Alterne entre y1 (haut) et y2 (bas)
        y = y1 if i % 2 == 0 else y2
        print(f"🔄 Balayage horizontal {i+1} à y = {y}")

        # Sens du balayage horizontal
        if i % 2 == 0:
            start_x, end_x = x_right, x_left
        else:
            start_x, end_x = x_left, x_right

        # ↕ Drag vertical vers le haut uniquement quand on va sur y1
        x_centre = bounds[0] + bounds[2] // 2
        print(f"  ↕ Drag vertical de y = {y2} vers y = {y1} (x = {x_centre})")
        pyautogui.moveTo(x_centre, y1)
        pyautogui.mouseDown()
        pyautogui.moveTo(x_centre, y2, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(1.5)

        # 🔍 Recherche de l’icône de ressource
        print("🔎 Recherche de ressources...")
        if click_template("assets/templates/gem_rss.png", bounds, threshold, delay=0.5):
            print("✅ Ressource détectée, exécution du farming...")
            time.sleep(5)  # Pause pour stabiliser l'icône
            # OCR coordonnées
            coords = get_game_coords(bounds)
            memory = load_memory()
            if coords and is_node_collected(coords, memory):
                print(f"⏩ Node déjà collectée à {coords}, on passe.")
                for _ in range(3):
                    print("SCROLLING DOWN...")
                    pyautogui.scroll(-10000)
                    time.sleep(0.2)
                continue  # Passe à la suivante

            time.sleep(2)  # Pause pour laisser le temps à l'icône de se stabiliser

            # Étape 2 : Cliquer sur la node de la gemme
            if not click_template("assets/templates/gem_node.png", bounds,  0.8):
                return False

            time.sleep(2)

            # Étape 3 : Cliquer sur "Collecter"
            if not click_template("assets/templates/collect_button.png", bounds,  0.8):
                if coords:
                    add_node(coords, memory, status="impossible")
                    print("❌ Bouton 'Marche' non trouvé, node marquée comme impossible.")
                    return False

            time.sleep(2)

            # Étape 4 : Cliquer sur "Nouvelle troupe"
            if not click_template("assets/templates/new_troop.png", bounds, 0.8):
                return False

            time.sleep(2)

            # Étape 5 : Cliquer sur "Marche"
            if not click_template("assets/templates/march_button.png", bounds,  0.8):
                if coords:
                    add_node(coords, memory, status="impossible")
                    print("❌ Bouton 'Marche' non trouvé, node marquée comme impossible.")
                    return False
            time.sleep(5)


            # Ajoute la node à la mémoire
            if coords:
                add_node(coords, memory)
            return True

        # ↔ Drag horizontal
        for _ in range(2):  # Deux balayages horizontaux
            print(f"  ↔ Drag horizontal de x = {end_x} vers x = {start_x} à y = {y}")
            pyautogui.moveTo(end_x, y)
            pyautogui.mouseDown()
            pyautogui.moveTo(start_x, y, duration=0.7)
            pyautogui.mouseUp()
            time.sleep(1.5)

        # 🔍 Recherche de l’icône de ressource
            print("🔎 Recherche de ressources...")
            if click_template("assets/templates/resource_icon.png", bounds, threshold, delay=0.5):
                print("✅ Ressource détectée, exécution du farming...")
                time.sleep(5)  # Pause pour stabiliser l'icône

                # OCR coordonnées
                coords = get_game_coords(bounds)
                memory = load_memory()
                if coords and is_node_collected(coords, memory):
                    print(f"⏩ Node déjà collectée à {coords}, on passe.")
                    for _ in range(3):
                        print("SCROLLING DOWN...")
                        pyautogui.scroll(-10000)
                        time.sleep(0.2)
                    continue  # Passe à la suivante

                time.sleep(2)  # Pause pour laisser le temps à l'icône de se stabiliser

                # Étape 2 : Cliquer sur la node de la gemme
                if not click_template("assets/templates/gem_node.png", bounds,  0.8):
                    return False

                time.sleep(2)

                # Étape 3 : Cliquer sur "Collecter"
                if not click_template("assets/templates/collect_button.png", bounds,  0.8):
                    return False

                time.sleep(2)

                # Étape 4 : Cliquer sur "Nouvelle troupe"
                if not click_template("assets/templates/new_troop.png", bounds, 0.8):
                    return False

                time.sleep(2)

                # Étape 5 : Cliquer sur "Marche"
                click_template("assets/templates/march_button.png", bounds,  0.8)

                # Ajoute la node à la mémoire
                if coords:
                    add_node(coords, memory)
                return True

    print("❌ Aucune ressource détectée après balayage.")
    return False


def find_and_execute_gem_chain(threshold=0.9):
    if not focus_game_window("Rise"):
        print("❌ Impossible de mettre la fenêtre du jeu au premier plan.")
        return

    bounds = get_game_window_bounds("Rise")
    if bounds is None:
        return

    # Recentrage souris
    center_x = bounds[0] + (bounds[2] - bounds[0]) // 2
    center_y = bounds[1] + (bounds[3] - bounds[1]) // 2
    pyautogui.moveTo(center_x, center_y)

    # Zoom arrière
    pyautogui.press("space")
    time.sleep(1)
    for _ in range(3):
        print("SCROLLING DOWN...")
        pyautogui.scroll(-10000)
        time.sleep(0.2)

    # Balayage + détection + actions
    success = balayage_gemmes(bounds, lignes=10, delay=1.2, threshold=threshold)
    time.sleep(1)

    if not success:
        print("⛔ Aucun camp exploitable trouvé.")

    pyautogui.press("space")
    return success



def farming_gem_loop(max_marches=4, delay_between_marches=900, check_interval=30, threshold=0.85):
    march_queue = []  
    while True:
        now = datetime.now()

        march_queue = [t for t in march_queue if now - t < timedelta(seconds=delay_between_marches)]

        print(f"\n📦 Marches actives : {len(march_queue)}/{max_marches}")

        if len(march_queue) < max_marches:
            print("🚀 Envoi d'une nouvelle troupe...")
            success = find_and_execute_gem_chain(threshold)
            if success:
                march_queue.append(datetime.now())
            else:
                print("⚠️ Aucun camp trouvé à cette itération.")
        else:
            print("🕒 Toutes les marches sont utilisées. En attente...")

        time.sleep(check_interval)