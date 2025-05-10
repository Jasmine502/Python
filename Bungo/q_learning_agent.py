# q_learning_agent.py
import numpy as np
import random

class QLearningAgent:
    def __init__(self, state_size, action_size,
                 learning_rate=0.1, discount_factor=0.99,
                 exploration_rate=1.0, exploration_decay_rate=0.998, min_exploration_rate=0.1,
                 move_speed=4, jump_power=-15, gravity=0.8, # Game physics for state binning
                 x_pos_bins=40, y_pos_bins=30, vel_x_bins=5, vel_y_bins=5, # Bin counts
                 plat_prox_left_bins=2, plat_prox_right_bins=2, plat_prox_below_bins=2, # Platform bin counts
                 horizontal_sensor_range=40, vertical_sensor_range_sides=30, vertical_sensor_range_below=60 # Sensor ranges
                 ):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay_rate = exploration_decay_rate
        self.min_exploration_rate = min_exploration_rate
        
        self.q_table = np.zeros((state_size, action_size))

        # Store game physics and binning parameters for state discretization
        self.move_speed = move_speed
        self.jump_power = jump_power # Note: jump_power is negative
        self.gravity = gravity

        self.X_POS_BINS = x_pos_bins
        self.Y_POS_BINS = y_pos_bins
        self.VEL_X_BINS = vel_x_bins
        self.VEL_Y_BINS = vel_y_bins
        self.PLAT_PROX_LEFT_BINS = plat_prox_left_bins
        self.PLAT_PROX_RIGHT_BINS = plat_prox_right_bins
        self.PLAT_PROX_BELOW_BINS = plat_prox_below_bins
        
        self.POS_BIN_SIZE = 20 # Assuming window_width/X_POS_BINS or window_height/Y_POS_BINS

        self.HORIZONTAL_SENSOR_RANGE = horizontal_sensor_range
        self.VERTICAL_SENSOR_RANGE_SIDES = vertical_sensor_range_sides
        self.VERTICAL_SENSOR_RANGE_BELOW = vertical_sensor_range_below


    def get_action(self, state):
        if random.random() < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        else:
            # Exploit: Choose the best action from Q-table
            # If multiple actions have the same max Q-value, this picks one randomly.
            best_actions = np.flatnonzero(self.q_table[state] == np.max(self.q_table[state]))
            return random.choice(best_actions)

    def update(self, state, action, reward, next_state, done):
        if done:
            target = reward # No future rewards if terminal
        else:
            next_max_q = np.max(self.q_table[next_state])
            target = reward + self.discount_factor * next_max_q
        
        current_q = self.q_table[state, action]
        new_q = current_q + self.learning_rate * (target - current_q)
        self.q_table[state, action] = new_q
    
    def decay_exploration_rate(self):
        self.exploration_rate = max(
            self.min_exploration_rate,
            self.exploration_rate * self.exploration_decay_rate
        )
    
    def get_state_index(self, x, y, player_width, player_height, velocity_x, velocity_y, platforms):
        # Discretize player position
        x_bin = min(int(x / self.POS_BIN_SIZE), self.X_POS_BINS - 1)
        y_bin = min(int(y / self.POS_BIN_SIZE), self.Y_POS_BINS - 1)

        # Discretize velocities (monotonic)
        # Velocity X Bins:
        if velocity_x < -self.move_speed * 0.6: vx_bin = 0    # Strong left
        elif velocity_x < -0.1: vx_bin = 1                   # Weak left
        elif velocity_x <= 0.1: vx_bin = 2                   # Still X
        elif velocity_x <= self.move_speed * 0.6: vx_bin = 3 # Weak right
        else: vx_bin = 4                                     # Strong right

        # Velocity Y Bins (jump_power is negative):
        if velocity_y < self.jump_power * 0.6: vy_bin = 0     # Strong up (e.g. initial jump part)
        elif velocity_y < -0.1: vy_bin = 1                    # Weak up
        elif velocity_y <= 0.1: vy_bin = 2                    # Neutral Y (on ground or peak of jump)
        elif velocity_y <= self.gravity * 5: vy_bin = 3       # Weak down (starting to fall)
        else: vy_bin = 4                                      # Strong down (falling fast)

        # Platform proximity sensors
        platform_prox_left_bin = 0  # 0: No platform close left, 1: Platform close left
        platform_prox_right_bin = 0 # 0: No platform close right, 1: Platform close right
        platform_prox_below_bin = 0 # 0: No platform close below, 1: Platform close below

        for p in platforms:
            # Check for platform to the left
            # Player's left edge: x, Platform's right edge: p.x + p.width
            # Check if platform's right edge is within sensor range of player's left edge
            # And if there's vertical overlap within a tolerance
            if (p.x + p.width > x - self.HORIZONTAL_SENSOR_RANGE and # Platform's right is near/past player's left sensor start
                p.x + p.width < x and                               # Platform's right is before player's left edge
                abs((y + player_height / 2) - (p.y + p.height / 2)) < self.VERTICAL_SENSOR_RANGE_SIDES + p.height/2): # Vertical check
                platform_prox_left_bin = 1
            
            # Check for platform to the right
            # Player's right edge: x + player_width, Platform's left edge: p.x
            # Check if platform's left edge is within sensor range of player's right edge
            if (p.x < (x + player_width) + self.HORIZONTAL_SENSOR_RANGE and # Platform's left is near/before player's right sensor end
                p.x > (x + player_width) and                              # Platform's left is after player's right edge
                abs((y + player_height / 2) - (p.y + p.height / 2)) < self.VERTICAL_SENSOR_RANGE_SIDES + p.height/2): # Vertical check
                platform_prox_right_bin = 1

            # Check for platform below
            # Player's bottom edge: y + player_height, Platform's top edge: p.y
            # Check if platform's top is within sensor range below player's bottom
            # And if there's horizontal overlap
            if (p.y > y + player_height and                               # Platform is below player
                p.y < (y + player_height) + self.VERTICAL_SENSOR_RANGE_BELOW and # Platform is within vertical sensor range
                p.x < x + player_width and                                # Platform's left is before player's right
                p.x + p.width > x):                                       # Platform's right is after player's left
                platform_prox_below_bin = 1
            
            if platform_prox_left_bin and platform_prox_right_bin and platform_prox_below_bin: # Optimization: if all found, no need to check more platforms
                break
        
        # Calculate state index (order matters for consistency)
        state_index = x_bin
        state_index = state_index * self.Y_POS_BINS + y_bin
        state_index = state_index * self.VEL_X_BINS + vx_bin
        state_index = state_index * self.VEL_Y_BINS + vy_bin
        state_index = state_index * self.PLAT_PROX_LEFT_BINS + platform_prox_left_bin
        state_index = state_index * self.PLAT_PROX_RIGHT_BINS + platform_prox_right_bin
        state_index = state_index * self.PLAT_PROX_BELOW_BINS + platform_prox_below_bin
        
        return max(0, min(state_index, self.state_size - 1)) # Ensure within bounds

    def save_q_table(self, filename="q_table.npy"):
        np.save(filename, self.q_table)
        print(f"Q-table saved to {filename}")

    def load_q_table(self, filename="q_table.npy"):
        self.q_table = np.load(filename)
        print(f"Q-table loaded from {filename}")