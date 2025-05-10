# game.py
import pygame
import sys
import time
import math
from q_learning_agent import QLearningAgent # Assuming q_learning_agent.py is in the same directory
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60 # Set to 0 for max speed during headless training, or a value like 60 for visualization

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game settings
GRAVITY = 0.8
JUMP_POWER = -15
MOVE_SPEED = 4
MAX_JUMP_TIME = 0.3
EPISODE_TIMEOUT = 5 # User changed this
NUM_AGENTS = 12

# Q-learning agent specific parameters for state discretization
X_POS_BINS = 40  # WINDOW_WIDTH / 20
Y_POS_BINS = 30  # WINDOW_HEIGHT / 20
VEL_X_BINS = 5
VEL_Y_BINS = 5
PLATFORM_PROX_LEFT_BINS = 2
PLATFORM_PROX_RIGHT_BINS = 2
PLATFORM_PROX_BELOW_BINS = 2

# Sensor ranges for platform detection (in pixels)
HORIZONTAL_SENSOR_RANGE = 40
VERTICAL_SENSOR_RANGE_SIDES = 30 # Approx player height
VERTICAL_SENSOR_RANGE_BELOW = 60

class Player:
    def __init__(self, x, y, alpha=255):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.jump_time = 0
        self.animation_frame = 0
        self.animation_timer = 0
        self.blink_timer = 0
        self.blink_state = False
        self.squish = 1.0
        self.last_on_ground = False
        self.visual_x = x
        self.visual_y = y
        self.alpha = alpha

    def move(self, action):
        if action == 0:  # Left
            self.velocity_x = -MOVE_SPEED
        elif action == 1:  # Right
            self.velocity_x = MOVE_SPEED
        elif action == 2:  # Jump
            if self.on_ground:
                self.velocity_y = JUMP_POWER
                self.on_ground = False
                self.jump_time = time.time()
            elif time.time() - self.jump_time < MAX_JUMP_TIME: # Allow jump extension
                self.velocity_y = JUMP_POWER * 0.8
    
    def update(self, platforms):
        self.velocity_y += GRAVITY
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_x = 0 # Reset horizontal velocity each frame unless move action is taken
        
        self.on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                if self.velocity_y > 0: # Moving downwards
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0: # Moving upwards
                    self.y = platform.y + platform.height
                    self.velocity_y = 0 # Bonked head
        
        if self.x < 0: self.x = 0
        elif self.x > WINDOW_WIDTH - self.width: self.x = WINDOW_WIDTH - self.width
        
        # Animation and visual fluff (can be disabled for speed)
        if FPS > 0:
            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 4
            
            if not self.last_on_ground and self.on_ground: self.squish = 0.7
            elif self.squish < 1.0:
                self.squish += 0.05
                if self.squish > 1.0: self.squish = 1.0
            self.last_on_ground = self.on_ground
            
            interp_speed = 0.4
            self.visual_x += (self.x - self.visual_x) * interp_speed
            self.visual_y += (self.y - self.visual_y) * interp_speed
        else: # If headless, snap visuals to actual position
            self.visual_x = self.x
            self.visual_y = self.y

    def check_collision(self, platform):
        return (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y)
    
    def draw(self, screen):
        # Drawing is skipped if FPS is 0 (headless mode)
        if FPS == 0:
            return

        shadow_base_alpha = 80
        actual_shadow_alpha = int(shadow_base_alpha * (self.alpha / 255.0))
        
        if actual_shadow_alpha > 5:
            shadow_color_tuple = (50, 50, 50, actual_shadow_alpha)
            shadow_width_val = int(self.width * 0.8)
            shadow_height_val = 8
            shadow_x_pos = self.visual_x + (self.width - shadow_width_val) // 2
            shadow_y_pos = self.visual_y + self.height - 2 
            shadow_surface = pygame.Surface((shadow_width_val, shadow_height_val), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, shadow_color_tuple, (0, 0, shadow_width_val, shadow_height_val))
            screen.blit(shadow_surface, (shadow_x_pos, shadow_y_pos))

        squish_h = int(self.height * self.squish)
        player_surface_width = self.width + 4 
        player_surface_height = self.height + 4 + 10 # Extra space for legs
        player_surface = pygame.Surface((player_surface_width, player_surface_height), pygame.SRCALPHA)
        player_surface.fill((0,0,0,0)) # Transparent background

        # Body
        pygame.draw.rect(player_surface, BLACK, (0, 0, self.width + 4, squish_h + 4), border_radius=6) # Outline
        pygame.draw.rect(player_surface, RED, (2, 2, self.width, squish_h), border_radius=4) # Fill

        # Eye
        self.blink_timer += 1
        if self.blink_timer > 120 and not self.blink_state: # Try to blink every ~2 seconds
            if random.random() < 0.03: self.blink_state = True; self.blink_timer = 0
        if self.blink_state and self.blink_timer > 8: # Blink duration
            self.blink_state = False; self.blink_timer = 0
        
        eye_x_on_surface = 2 + self.width - 10 # Position eye on the player surface
        eye_y_on_surface = 2 + 10
        if not self.blink_state:
            pygame.draw.circle(player_surface, WHITE, (int(eye_x_on_surface), int(eye_y_on_surface)), 5)
        else:
            pygame.draw.line(player_surface, WHITE, (int(eye_x_on_surface - 3), int(eye_y_on_surface)), (int(eye_x_on_surface + 3), int(eye_y_on_surface)), 2)

        # Legs
        leg_phase = self.animation_frame * 0.5 # Controls leg swing based on animation frame
        leg_swing = int(5 * math.sin(leg_phase)) # Calculate swing amount
        leg_attach_y_on_surface = squish_h + 4 # Attach legs below the body
        pygame.draw.line(player_surface, BLACK, (2 + 7, leg_attach_y_on_surface), (2 + 7 + leg_swing, leg_attach_y_on_surface + 10), 3)
        pygame.draw.line(player_surface, BLACK, (2 + self.width - 7, leg_attach_y_on_surface), (2 + self.width - 7 - leg_swing, leg_attach_y_on_surface + 10), 3)

        player_surface.set_alpha(self.alpha) # Apply transparency
        
        # Position the player surface considering squish
        squish_y_abs = self.visual_y + (self.height - squish_h) 
        blit_x = self.visual_x - 2 # Adjust blit position for outline
        blit_y = squish_y_abs - 2
        screen.blit(player_surface, (blit_x, blit_y))

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x; self.y = y; self.width = width; self.height = height

class Game:
    def __init__(self):
        if FPS > 0:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Bungo Simulation")
        self.clock = pygame.time.Clock()
        
        self.platforms = [
            Platform(80, WINDOW_HEIGHT - 120, 160, 20),
            Platform(300, WINDOW_HEIGHT - 200, 160, 20),
            Platform(520, WINDOW_HEIGHT - 280, 160, 20),
            Platform(600, WINDOW_HEIGHT - 440, 160, 20), # Goal platform
            Platform(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40), # Ground/Lava
        ]
        
        self.num_agents = NUM_AGENTS
        self.players = []
        self.agents = []
        self.previous_xs = [0.0] * self.num_agents
        self.last_actions = [0] * self.num_agents # Store last action for timeout update
        self.platform_rewards_list = [] # To track if intermediate platform rewards were given

        # Calculate state size based on bin definitions
        self.state_size = (X_POS_BINS * Y_POS_BINS * VEL_X_BINS * VEL_Y_BINS *
                           PLATFORM_PROX_LEFT_BINS * PLATFORM_PROX_RIGHT_BINS *
                           PLATFORM_PROX_BELOW_BINS)
        self.action_size = 3 # Left, Right, Jump
        
        player_start_x_default = 100
        player_start_y_default = WINDOW_HEIGHT - 150 # Start on the ground initially

        for i in range(self.num_agents):
            alpha_val = int(255 * 0.10) if i < self.num_agents - 1 else 255 # Highlight one agent
            self.players.append(Player(player_start_x_default, player_start_y_default, alpha=alpha_val))
            self.agents.append(QLearningAgent(
                state_size=self.state_size,
                action_size=self.action_size,
                learning_rate=0.1, # Standard LR
                discount_factor=0.99, # Prioritize future rewards
                exploration_rate=1.0, # Start with full exploration
                exploration_decay_rate=0.998, # Slower decay for larger state space
                min_exploration_rate=0.1,
                # Pass game physics and discretization parameters
                move_speed=MOVE_SPEED,
                jump_power=JUMP_POWER,
                gravity=GRAVITY,
                x_pos_bins=X_POS_BINS,
                y_pos_bins=Y_POS_BINS,
                vel_x_bins=VEL_X_BINS,
                vel_y_bins=VEL_Y_BINS,
                plat_prox_left_bins=PLATFORM_PROX_LEFT_BINS,
                plat_prox_right_bins=PLATFORM_PROX_RIGHT_BINS,
                plat_prox_below_bins=PLATFORM_PROX_BELOW_BINS,
                horizontal_sensor_range=HORIZONTAL_SENSOR_RANGE,
                vertical_sensor_range_sides=VERTICAL_SENSOR_RANGE_SIDES,
                vertical_sensor_range_below=VERTICAL_SENSOR_RANGE_BELOW
            ))
            self.platform_rewards_list.append([False] * (len(self.platforms) - 1)) # Exclude ground
            self.previous_xs[i] = player_start_x_default
        
        self.episode = 0
        # self.max_episodes = 1000 # REMOVED: No longer limiting episodes
        self.goal_x = 600 + 80 # Center of the goal platform
        self.goal_y = WINDOW_HEIGHT - 440 - 10 # Slightly above the goal platform
        self.episode_start_time = time.time()

        # Visuals for lava (can be skipped if FPS=0)
        self.lava_bubbles = []
        if FPS > 0:
            self.lava_bubbles = [{'x': random.randint(0, WINDOW_WIDTH), 'y': WINDOW_HEIGHT - 40 + random.randint(10, 35), 'r': random.randint(4, 10), 't': random.uniform(0, 2 * math.pi)} for _ in range(18)]
        self.lava_anim_frame = 0
    
    def get_reward(self, player_idx):
        player = self.players[player_idx]
        prev_x = self.previous_xs[player_idx]
        player_platform_rewards = self.platform_rewards_list[player_idx]

        reward = -0.05  # Small penalty per step to encourage efficiency

        # Reward for moving right (towards the goal)
        if player.x > prev_x:
            reward += 0.02
        
        # Reward for landing on intermediate platforms (once per platform per episode)
        for i, platform in enumerate(self.platforms[:-1]): # Exclude ground/lava
            if not player_platform_rewards[i] and \
               player.check_collision(platform) and player.on_ground and \
               abs(player.y + player.height - platform.y) < 1: # Ensure landed on top
                # Check if this is the goal platform (platform index 3)
                if i == 3: # Assuming the goal platform is the 4th in the list (index 3)
                    # This reward is now handled by the goal check below
                    pass
                else:
                    reward += 10 
                player_platform_rewards[i] = True 
        
        # Penalty for falling into lava (ground platform)
        ground_platform = self.platforms[-1]
        if player.y + player.height >= ground_platform.y and \
           player.x + player.width > ground_platform.x and \
           player.x < ground_platform.x + ground_platform.width:
            return True, -200 # Terminal state: fell in lava
        
        # Penalty for falling out of bounds (bottom of screen)
        if player.y > WINDOW_HEIGHT:
            return True, -100 # Terminal state: fell off screen
        
        # Reward for reaching the goal
        goal_platform_idx = 3 # The goal platform is the 4th one (index 3)
        goal_platform_obj = self.platforms[goal_platform_idx]
        if (player.x + player.width > goal_platform_obj.x and
            player.x < goal_platform_obj.x + goal_platform_obj.width and
            abs(player.y + player.height - goal_platform_obj.y) < 1 and player.on_ground):
            return True, 200 # Terminal state: reached goal

        return False, reward # Not a terminal state, continue episode
    
    def reset_episode(self):
        player_start_x_default = 100
        player_start_y_default = WINDOW_HEIGHT - 150 
        for i in range(self.num_agents):
            preserved_alpha = self.players[i].alpha # Keep visual distinction
            self.players[i] = Player(player_start_x_default, player_start_y_default, alpha=preserved_alpha)
            self.previous_xs[i] = self.players[i].x
            self.platform_rewards_list[i] = [False] * (len(self.platforms) - 1)
        self.episode_start_time = time.time()
    
    def run(self):
        while True: # MODIFIED: Run indefinitely until manually closed
            self.reset_episode()
            episode_is_done_for_all_agents = False # Track if episode should end for ML logic
            active_agents_this_episode = [True] * self.num_agents # Track which agents are still active
            
            # Exploration rate boost at certain episodes
            if (150 < self.episode < 350 or self.episode % 150 == 0 and self.episode > 0):
                 for agent in self.agents:
                    agent.exploration_rate = max(agent.exploration_rate, 0.25)

            current_episode_step_count = 0
            while not episode_is_done_for_all_agents:
                current_episode_step_count +=1
                if FPS > 0: # Only handle events if visualizing
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                # Check for timeout
                timed_out = time.time() - self.episode_start_time > EPISODE_TIMEOUT
                if timed_out:
                    episode_is_done_for_all_agents = True

                # If all agents have reached a terminal state individually
                if not any(active_agents_this_episode):
                    episode_is_done_for_all_agents = True

                if episode_is_done_for_all_agents:
                    break

                for i in range(self.num_agents):
                    if not active_agents_this_episode[i]:
                        continue # Skip agents that have finished their part of the episode

                    player = self.players[i]; agent = self.agents[i]
                    
                    current_state = agent.get_state_index(
                        player.x, player.y, player.width, player.height, 
                        player.velocity_x, player.velocity_y, self.platforms
                    )
                    action = agent.get_action(current_state)
                    self.last_actions[i] = action # Store action for timeout update

                    player.move(action)
                    player.update(self.platforms)
                    
                    player_reached_terminal_state, reward = self.get_reward(i)

                    if player_reached_terminal_state:
                        active_agents_this_episode[i] = False # This agent is done

                    next_state = agent.get_state_index(
                        player.x, player.y, player.width, player.height,
                        player.velocity_x, player.velocity_y, self.platforms
                    )
                    agent.update(current_state, action, reward, next_state, player_reached_terminal_state)
                    self.previous_xs[i] = player.x
                
                # --- Drawing Start (skipped if FPS=0) ---
                if FPS > 0:
                    self.screen.fill(WHITE) # Clear screen
                    # Background gradient
                    for i_bg in range(WINDOW_HEIGHT):
                        color_val = (int(180 + 40 * (i_bg/WINDOW_HEIGHT)), int(220 - 60 * (i_bg/WINDOW_HEIGHT)), int(255 - 80 * (i_bg/WINDOW_HEIGHT)))
                        pygame.draw.line(self.screen, color_val, (0, i_bg), (WINDOW_WIDTH, i_bg))

                    # Draw platforms
                    for idx, platform in enumerate(self.platforms):
                        plat_shadow = pygame.Surface((platform.width, 8), pygame.SRCALPHA); pygame.draw.ellipse(plat_shadow, (50,50,50,60), (0,0,platform.width,8)); self.screen.blit(plat_shadow, (platform.x, platform.y+platform.height-2))
                        if idx == len(self.platforms) - 1: # Lava platform
                            pygame.draw.rect(self.screen, (220, 60, 20), (platform.x, platform.y, platform.width, platform.height))
                            for x_lava in range(platform.x, platform.x + platform.width, 20):
                                wave_y = platform.y + 20 + int(8 * math.sin(self.lava_anim_frame*0.1 + x_lava*0.05)); pygame.draw.ellipse(self.screen, (255,120,40), (x_lava,wave_y,20,12))
                            for bubble in self.lava_bubbles:
                                bubble['y'] -= 0.7 + 0.5*math.sin(self.lava_anim_frame*0.1 + bubble['t'])
                                if bubble['y'] < platform.y+5: bubble['x']=random.randint(platform.x,platform.x+platform.width); bubble['y']=platform.y+platform.height-random.randint(0,10); bubble['r']=random.randint(4,10); bubble['t']=random.uniform(0,2*math.pi)
                                pygame.draw.circle(self.screen, (255,200,80), (int(bubble['x']),int(bubble['y'])), bubble['r'])
                            pygame.draw.rect(self.screen, (255,180,80), (platform.x,platform.y,platform.width,8)); pygame.draw.rect(self.screen, (100,30,10), (platform.x,platform.y,platform.width,platform.height),3,border_radius=6)
                        else: # Normal platforms
                            plat_color=(110,90,60); grass_color=(60,180,60); pygame.draw.rect(self.screen, plat_color, (platform.x,platform.y,platform.width,platform.height),border_radius=6); pygame.draw.rect(self.screen, grass_color, (platform.x,platform.y,platform.width,8),border_radius=6); pygame.draw.rect(self.screen, (180,160,100), (platform.x,platform.y+platform.height-6,platform.width,6),border_radius=6); pygame.draw.rect(self.screen, (60,40,20), (platform.x,platform.y,platform.width,platform.height),2,border_radius=6)
                    
                    # Draw players
                    for p_obj in self.players: p_obj.draw(self.screen)
                    
                    # Draw goal visual
                    goal_platform_obj = self.platforms[3] # Goal platform
                    goal_center_x = goal_platform_obj.x + goal_platform_obj.width / 2
                    goal_center_y = goal_platform_obj.y - 15 # Visual above platform
                    gem_surface=pygame.Surface((32,32),pygame.SRCALPHA); pygame.draw.polygon(gem_surface,(80,255,180,220),[(16,0),(32,8),(28,32),(4,32),(0,8)]); pygame.draw.polygon(gem_surface,(180,255,255,180),[(16,4),(28,10),(25,28),(7,28),(4,10)]); pygame.draw.ellipse(gem_surface,(255,255,255,120),(8,6,8,6)); self.screen.blit(gem_surface,(goal_center_x-16,goal_center_y-16))
                    if(self.lava_anim_frame//20)%2==0: pygame.draw.ellipse(self.screen,(255,255,255,90),(goal_center_x-7,goal_center_y-13,14,8))
                    pygame.draw.polygon(self.screen,(0,80,60),[(goal_center_x,goal_center_y-16),(goal_center_x+16,goal_center_y-8),(goal_center_x+12,goal_center_y+16),(goal_center_x-12,goal_center_y+16),(goal_center_x-16,goal_center_y-8)],2)
                    
                    # UI Text (Episode, Time)
                    font=pygame.font.Font(None,40); time_left=max(0,EPISODE_TIMEOUT-(time.time()-self.episode_start_time)); text_str=f"Ep: {self.episode} St: {current_episode_step_count} T: {time_left:.1f}s"; text_render=font.render(text_str,True,(255,220,80)); outline_render=font.render(text_str,True,(60,40,20))
                    for dx_o,dy_o in[(-2,0),(2,0),(0,-2),(0,2)]: self.screen.blit(outline_render,(12+dx_o,12+dy_o))
                    self.screen.blit(text_render,(12,12))
                    
                    pygame.display.flip()
                    self.lava_anim_frame+=1
                # --- Drawing End ---
                
                if FPS > 0:
                    self.clock.tick(FPS)
            
            # Post-episode processing (e.g., for timeouts)
            if timed_out:
                for i in range(self.num_agents):
                    if active_agents_this_episode[i]: # If agent was still active when timeout occurred
                        player = self.players[i]; agent = self.agents[i]
                        # Calculate distance to goal as a heuristic for timeout penalty
                        dist_to_goal = math.sqrt((player.x - self.goal_x)**2 + (player.y - self.goal_y)**2)
                        penalty = -min(50, int(dist_to_goal / 10)) # Scaled penalty, capped
                        
                        timeout_state = agent.get_state_index(
                            player.x, player.y, player.width, player.height,
                            player.velocity_x, player.velocity_y, self.platforms
                        )
                        # Update Q-table using the last action that led to this timeout state
                        agent.update(timeout_state, self.last_actions[i], penalty, timeout_state, True) # True for terminal
            
            self.episode += 1
            for agent in self.agents: 
                agent.decay_exploration_rate() # Decay exploration rate for all agents
            
            if self.episode % 10 == 0:
                avg_exp_rate = sum(ag.exploration_rate for ag in self.agents) / self.num_agents
                print(f"Episode: {self.episode}, Avg Exploration Rate: {avg_exp_rate:.2f}")
                # Optional: Save Q-tables periodically
                # for idx, ag in enumerate(self.agents):
                #     if idx == self.num_agents -1 : # Save only the "main" agent
                #         ag.save_q_table(f"q_table_agent_main_ep{self.episode}.npy")

if __name__ == "__main__":
    game = Game()
    game.run()