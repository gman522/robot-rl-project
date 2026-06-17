import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

# -------------------------
# RED NEURONAL
# -------------------------
class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 5)
        )

    def forward(self, x):
        return self.net(x)


# -------------------------
# MODELO
# -------------------------
model = DQN()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# -------------------------
# HYPERPARAMS
# -------------------------
gamma = 0.9

epsilon = 1.0
epsilon_min = 0.1
epsilon_decay = 0.995


# -------------------------
# UTIL
# -------------------------
def to_tensor(state):
    return torch.FloatTensor(state)


# -------------------------
# SELECCIÓN DE ACCIÓN
# -------------------------
def choose_action(state):

    global epsilon

    if random.random() < epsilon:
        return random.randint(0, 4)

    state = to_tensor(state)
    q_values = model(state)

    return torch.argmax(q_values).item()


# -------------------------
# ENTRENAMIENTO
# -------------------------
def update_q(state, action, reward, next_state):

    state = to_tensor(state)
    next_state = to_tensor(next_state)

    q_values = model(state)
    next_q_values = model(next_state)

    target = q_values.clone().detach()

    target[action] = reward + gamma * torch.max(next_q_values)

    loss = nn.MSELoss()(q_values, target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


# -------------------------
# DECAY EPSILON
# -------------------------
def decay():
    global epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)


# -------------------------
# RESET EPSILON
# -------------------------
def reset_epsilon():
    global epsilon
    epsilon = 1.0