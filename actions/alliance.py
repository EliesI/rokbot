import time
import pyautogui
from core.vision import click_template
from core.window import get_game_window_bounds

def help_alliance(threshold=0.85):
    """
    Appuie sur l'icône 'alliance_help' pour aider les alliés.
    """

    bounds = get_game_window_bounds("Rise")
    print("🔔 Recherche de l'icône d'aide d'alliance...")
    if click_template("assets/templates/alliance_help.png", bounds, threshold):
        print("✅ Aide envoyée à l'alliance !")
        time.sleep(1)
        return True
    else:
        print("❌ Icône d'aide d'alliance non trouvée.")
        return False

def alliance_help_loop(bounds, interval=60):
    """
    Boucle pour aider automatiquement l'alliance toutes les X secondes.
    """
    print("⏳ Démarrage de la boucle d'aide à l'alliance.")
    try:
        while True:
            help_alliance(bounds)
            print(f"⏸️ Pause de {interval} secondes avant la prochaine aide.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("🛑 Arrêt de la boucle d'aide à l'alliance.")
