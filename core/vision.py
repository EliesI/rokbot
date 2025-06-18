import cv2
import pyautogui
import numpy as np
import time
import os

def find_template(template_path, bounds, threshold=0.9):
    """
    Cherche le template dans la région et retourne les coordonnées du centre si trouvé, sinon None.
    """
    if not os.path.exists(template_path):
        print(f"❌ [VISION] Template non trouvé : {template_path}")
        return None

    x, y, w, h = bounds
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)
    if template is None:
        print(f"❌ [VISION] Erreur chargement template : {template_path}")
        return None

    w_t, h_t = template.shape[::-1]
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, val, _, loc = cv2.minMaxLoc(res)
    print(f"📊 [VISION] Score match : {val:.4f}")

    if val >= threshold:
        center = (loc[0] + w_t // 2 + x, loc[1] + h_t // 2 + y)
        print(f"✅ {template_path} détecté : x = {center[0]}, y = {center[1]} , theshold = {val:.2f}")
        return center
    else:
        print(f"❌ {template_path} non détecté.")
        print(f"💡 [VISION] Score {val:.4f} < seuil {threshold}")
        return None

def do_click(center, delay=1.0):
    """
    Déplace la souris et clique sur les coordonnées données.
    """
    if center is None:
        return False
    print(f"🖱️ [VISION] Déplacement souris vers {center}...")
    pyautogui.moveTo(center[0], center[1], duration=0.3)
    print(f"👆 [VISION] Clic...")
    pyautogui.click()
    if delay > 0:
        print(f"⏳ [VISION] Attente {delay}s...")
        time.sleep(delay)
    return True

def click_template(template_path, bounds, threshold=0.9, delay=1.0):
    """
    Combine la détection et le clic.
    """
    center = find_template(template_path, bounds, threshold)
    return do_click(center, delay)


def check_marchs_full(bounds):
    template_path = "assets/templates/marchs_full1.png"
    print(f"🔍 [VISION] Vérification de l'état des marches...")
    return find_template(template_path, bounds, threshold=0.8)

