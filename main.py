import time
import pyautogui
import keyboard
import cv2

from rl_agent import choose_action, update_q, decay, reset_epsilon
from robot_controller import ACTIONS
from vision import detect_walls


# ----------------------------
# CONFIG
# ----------------------------
CAM_X = 700
CAM_Y = 500

running = False
cap = cv2.VideoCapture(0)

last_toggle_time = 0


def log(msg):
    print(msg)


def focus_app():
    pyautogui.moveTo(CAM_X, CAM_Y, duration=0.2)
    pyautogui.click()
    time.sleep(0.5)


def get_state():
    ret, frame = cap.read()
    if not ret:
        return (0, 0, 0, 0)

    left, center, right = detect_walls(frame)

    return (int(left), int(center), int(right), 0)


print("F8 = START / STOP | ESC = SALIR")

state = get_state()

while True:

    # ----------------------------
    # SALIR
    # ----------------------------
    if keyboard.is_pressed("esc"):
        print("Saliendo...")
        break

    # ----------------------------
    # START / STOP
    # ----------------------------
    if keyboard.is_pressed("f8"):
        current_time = time.time()

        if current_time - last_toggle_time > 0.5:
            running = not running
            last_toggle_time = current_time

            print("RUNNING =", running)

            if running:
                focus_app()
                reset_epsilon()
                state = get_state()

        time.sleep(0.1)

    # ----------------------------
    # LOOP RL
    # ----------------------------
    if running:

        action = choose_action(state)

        log(f"STATE={state} ACTION={action}")

        # ejecutar acción (con duración interna del robot_controller)
        ACTIONS[action]()

        # esperar a que el movimiento termine + estabilización cámara
        time.sleep(1.0)

        next_state = get_state()

        # ----------------------------
        # REWARD INTELIGENTE (CLAVE)
        # ----------------------------
        left, center, right, _ = state

        reward = -1  # base exploración

        # ❌ castigo fuerte: intentar avanzar con pared delante
        if center == 1 and action == 0:
            reward = -100

        # ❌ castigo medio: chocar lateralmente o mala dirección
        if (left == 1 and action == 1) or (right == 1 and action == 2):
            reward = -10

        # ✔ recompensa leve: avanzar en zona libre
        if center == 0 and action == 0:
            reward = 2

        update_q(state, action, reward, next_state)

        state = next_state

        decay()

    time.sleep(0.05)