from core.window import get_game_window_bounds
from core.ocr_utils import get_game_coords,get_timer_text
from core.vision import check_marchs_full

if __name__ == "__main__":
    bounds = get_game_window_bounds("Rise")
    if bounds:
           check_marchs_full(bounds)
    else:
        print("Impossible de détecter la fenêtre du jeu.")