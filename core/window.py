import pygetwindow as gw
import time

def get_game_window_bounds(window_title="Rise"):
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print("❌ Fenêtre non trouvée.")
        return None
    win = windows[0]
    print(f"🖥️ Fenêtre détectée : {win.title}")
    print(f"📍 Position : x={win.left}, y={win.top}")
    print(f"📐 Taille : width={win.width}, height={win.height}")
    return (win.left, win.top, win.width, win.height)

def focus_game_window(window_title="Rise"):
    """Focus sur la fenêtre du jeu"""
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            print("❌ Impossible de trouver la fenêtre du jeu")
            return False
        
        game_window = windows[0]
        game_window.activate()
        time.sleep(0.5)
        print(f"✅ Fenêtre '{game_window.title}' mise au premier plan")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du focus de la fenêtre: {e}")
        return False

if __name__ == "__main__":
    get_game_window_bounds()


