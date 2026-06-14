import numpy as np
import random

# -------------------------
# Q TABLE
# -------------------------
Q = {}

# -------------------------
# HIPERPARÁMETROS
# -------------------------
alpha = 0.1
gamma = 0.9

epsilon = 1.0
epsilon_min = 0.1
epsilon_decay = 0.995


# -------------------------
# NORMALIZAR ESTADO
# -------------------------
def normalize_state(state):
    return tuple(int(x) for x in state)


# -------------------------
# INICIALIZAR / OBTENER Q
# -------------------------
def get_q(state):

    state = normalize_state(state)

    if state not in Q:
        Q[state] = np.zeros(5)  # 5 acciones

    return Q[state]


# -------------------------
# ELEGIR ACCIÓN (ε-greedy)
# -------------------------
def choose_action(state):

    global epsilon

    state = normalize_state(state)

    # exploración
    if random.random() < epsilon:
        return random.randint(0, 4)

    # explotación
    q_values = get_q(state)
    return int(np.argmax(q_values))


# -------------------------
# ACTUALIZAR Q-LEARNING
# -------------------------
def update_q(state, action, reward, next_state):

    state = normalize_state(state)
    next_state = normalize_state(next_state)

    q_state = get_q(state)
    q_next = get_q(next_state)

    best_next = np.max(q_next)

    q_state[action] += alpha * (
        reward + gamma * best_next - q_state[action]
    )


# -------------------------
# DECAY EPSILON
# -------------------------
def decay():

    global epsilon

    epsilon = max(epsilon_min, epsilon * epsilon_decay)


# -------------------------
# RESET EPSILON (por episodio)
# -------------------------
def reset_epsilon():

    global epsilon

    epsilon = 1.0