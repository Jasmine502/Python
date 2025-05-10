import numpy as np
import random

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, exploration_rate=0.8):
        """
        Initialize the Q-learning agent
        
        Parameters:
        - state_size: Number of possible states (discretized)
        - action_size: Number of possible actions
        - learning_rate: How quickly the agent updates its Q-values (alpha)
        - discount_factor: How much future rewards are valued (gamma)
        - exploration_rate: Probability of taking random actions (epsilon)
        """
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        
        # Initialize Q-table with zeros
        # Q-table shape: (state_size, action_size)
        self.q_table = np.zeros((state_size, action_size))
        
    def get_action(self, state):
        """
        Choose an action using epsilon-greedy policy
        
        Parameters:
        - state: Current state of the agent
        
        Returns:
        - action: Chosen action (0: left, 1: right, 2: jump)
        """
        # Exploration: choose random action
        if random.random() < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        
        # Exploitation: choose best action from Q-table
        return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state):
        """
        Update Q-value using Q-learning formula:
        Q(s,a) = Q(s,a) + α[r + γ max(Q(s',a')) - Q(s,a)]
        
        Parameters:
        - state: Current state
        - action: Action taken
        - reward: Reward received
        - next_state: Next state after taking action
        """
        # Get the maximum Q-value for the next state
        next_max = np.max(self.q_table[next_state])
        
        # Current Q-value
        current_q = self.q_table[state, action]
        
        # Update Q-value using Q-learning formula
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * next_max - current_q
        )
        
        self.q_table[state, action] = new_q
    
    def decay_exploration_rate(self, decay_rate=0.99, min_exploration_rate=0.05):
        """
        Decay the exploration rate over time to favor exploitation
        
        Parameters:
        - decay_rate: How quickly exploration rate decreases
        - min_exploration_rate: Minimum exploration rate
        """
        self.exploration_rate = max(
            min_exploration_rate,
            self.exploration_rate * decay_rate
        )
    
    def get_state_index(self, x, y, velocity_x, velocity_y, platforms):
        """
        Convert continuous state space to discrete state index
        
        Parameters:
        - x, y: Agent position
        - velocity_x, velocity_y: Agent velocity
        - platforms: List of platform positions
        
        Returns:
        - state_index: Discrete state index for Q-table
        """
        # Discretize position and velocity
        x_bin = min(int(x / 20), 39)  # 800/20 = 40 bins
        y_bin = min(int(y / 20), 29)  # 600/20 = 30 bins
        vx_bin = 2 if velocity_x > 2 else (1 if velocity_x > 0 else (0 if velocity_x == 0 else (3 if velocity_x < -2 else 4)))
        vy_bin = 2 if velocity_y > 2 else (1 if velocity_y > 0 else (0 if velocity_y == 0 else (3 if velocity_y < -2 else 4)))
        # 5 bins for vx, 5 for vy
        # Calculate state index
        state_index = (x_bin * 30 * 5 * 5) + (y_bin * 5 * 5) + (vx_bin * 5) + vy_bin
        return state_index 