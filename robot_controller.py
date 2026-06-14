import pyautogui
import time

# Pequeño delay para que pyautogui sea estable
pyautogui.PAUSE = 0.05

def forward():
    pyautogui.press('d')

def left():
    pyautogui.press('w')

def right():
    pyautogui.press('s')

def back():
    pyautogui.press('a')

def stop():
    pass


# Mapa de acciones (IMPORTANTE para RL)
ACTIONS = [
    forward,
    left,
    right,
    back,
    stop
]