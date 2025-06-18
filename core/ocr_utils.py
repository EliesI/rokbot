import pytesseract
from PIL import Image, ImageOps
import pyautogui
import re
import os
import cv2
import numpy as np


PYTESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(PYTESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH


def get_game_coords(bounds):
    x, y, w, h = bounds
    region = (x+195, y+20, 125, 30)  # Ajuste si besoin
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("debug_ocr_zone.png")
    text = pytesseract.image_to_string(screenshot, lang="eng", config="--psm 7")
    print("Texte OCR brut :", repr(text))
    match = re.search(r'#(\d+)\s*X[:=](\d+)\s*Y[:=](\d+)', text)
    if match:
        return {
            "zone": int(match.group(1)),
            "x": int(match.group(2)),
            "y": int(match.group(3))
        }
    return None

def get_timer_text(bounds):
    # Définir une zone relative au bouton MARCHE (à ajuster selon ta capture)
    x, y, w, h = bounds
    timer_region = (int(x + w / 2 + 175), int(y + h - 185), 75, 25)  # Tuple d'entiers
    print(f"🔍 Zone OCR : {timer_region}")
    screenshot = pyautogui.screenshot(region=timer_region)
    screenshot.save("debug_ocr_zone.png")
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Amélioration pour meilleure lecture OCR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh, config='--psm 7')
    print("Texte OCR brut :", repr(text))
    print("Texte OCR traité :", text.strip())
    return text.strip()
