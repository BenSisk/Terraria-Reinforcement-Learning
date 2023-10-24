import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
from mss import mss
import time

from environment import GameEnvironment

# Define the DQN network
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Define the replay buffer to store experiences
class ReplayBuffer:
    def __init__(self, buffer_size):
        self.buffer = deque(maxlen=buffer_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def size(self):
        return len(self.buffer)


env = GameEnvironment()

# Define hyperparameters
input_dim = 2  # X and Y Coordinates of the the boss
output_dim = 4  # Assuming four possible keyboard movements
learning_rate = 0.01
gamma = 0.99  # Discount factor
epsilon = 0.1  # Epsilon-greedy exploration

# Initialize the DQN, target DQN, and optimizer
dqn = DQN(input_dim, output_dim)
dqn.load_state_dict(torch.load("King_Slime_300.pth")) # Uncomment this line to load a pre-trained DQN
target_dqn = DQN(input_dim, output_dim)
target_dqn.load_state_dict(dqn.state_dict())
optimizer = optim.Adam(dqn.parameters(), lr=learning_rate)

# Initialize the replay bufferdDD
buffer_size = 10000
replay_buffer = ReplayBuffer(buffer_size)

# Define the training loop
num_episodes = 50
batch_size = 8

time.sleep(2)

for episode in range(num_episodes):
    print(f"Episode {episode}")

    # Reset the environment and observe the initial state
    env.reset()
    state = np.array([-1, -1])

    done = False
    total_reward = 0

    while not done:
        # Epsilon-greedy action selection
        if random.random() < epsilon:
            q_value = torch.zeros(output_dim)
            for i in range(output_dim):
                q_value[i] = random.randint(0, 100)
            action = torch.argmax(q_value).item()
        else:
            q_value = dqn(torch.FloatTensor(state))
            action = torch.argmax(q_value).item()

        next_state, reward, done = env.step(q_value.tolist())

        replay_buffer.add((state, action, reward, next_state, done))

        state = next_state
        total_reward += reward

        # Sample a random batch from the replay buffer and perform a Q-learning update
        if replay_buffer.size() >= batch_size:
            batch = replay_buffer.sample(batch_size)
            states, actions, rewards, next_states, dones = zip(*batch)

            states = torch.FloatTensor(states)
            next_states = torch.FloatTensor(next_states)
            actions = torch.LongTensor(actions)
            rewards = torch.FloatTensor(rewards)
            dones = torch.FloatTensor(dones)

            # Compute Q-values and target Q-values
            q_valuess = dqn(states)
            target_q_values = target_dqn(next_states)
            max_target_q_values = torch.max(target_q_values, dim=1).values
            target_q_values = rewards + gamma * (1 - dones) * max_target_q_values

            # Compute the loss and update the DQN
            loss = nn.MSELoss()(q_valuess.gather(1, actions.view(-1, 1)), target_q_values.unsqueeze(1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    if episode % 10 == 0:
        # Update the target DQN every 10 episodes
        target_dqn.load_state_dict(dqn.state_dict())

    print(f"Episode {episode}, Total Reward: {total_reward}")
    # Save the trained DQN
    torch.save(dqn.state_dict(), "King_Slime.pth")