import pyautogui
import time

pyautogui.PAUSE = 0.01


def hold_key(key, duration):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)


def forward(duration=1.5):
    hold_key('d', duration)


def left(duration=0.8):
    hold_key('w', duration)


def right(duration=0.8):
    hold_key('s', duration)


def back(duration=1.2):
    hold_key('a', duration)


def stop():
    pass


ACTIONS = [
    forward,
    left,
    right,
    back,
    stop
]