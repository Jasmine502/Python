import pygame
import sys
import time
import math
from q_learning_agent import QLearningAgent
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game settings
GRAVITY = 0.8
JUMP_POWER = -15
MOVE_SPEED = 4
MAX_JUMP_TIME = 0.3  # Maximum time jump can be held
EPISODE_TIMEOUT = 5  # Maximum seconds per episode

class Player:
    def __init__(self, x, y):
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
        self.eye_offset = self.width - 10  # Always right side
        self.visual_x = x
        self.visual_y = y
    
    def move(self, action):
        """
        Move the player based on the AI's action
        
        Parameters:
        - action: 0 (left), 1 (right), or 2 (jump)
        """
        if action == 0:  # Left
            self.velocity_x = -MOVE_SPEED
        elif action == 1:  # Right
            self.velocity_x = MOVE_SPEED
        elif action == 2:  # Jump
            if self.on_ground:
                self.velocity_y = JUMP_POWER
                self.on_ground = False
                self.jump_time = time.time()
            elif time.time() - self.jump_time < MAX_JUMP_TIME:
                # Variable jump height based on how long jump is held
                self.velocity_y = JUMP_POWER * 0.8
    
    def update(self, platforms):
        """
        Update player position and handle collisions
        """
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Reset horizontal velocity
        self.velocity_x = 0
        
        # Check platform collisions
        self.on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                # Collision from above
                if self.velocity_y > 0:
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                # Collision from below
                elif self.velocity_y < 0:
                    self.y = platform.y + platform.height
                    self.velocity_y = 0
        
        # Keep player in bounds horizontally
        if self.x < 0:
            self.x = 0
        elif self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width
        
        # Update animation
        self.animation_timer += 1
        if self.animation_timer >= 5:  # Change animation frame every 5 game frames
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
        
        # Squish effect when landing
        if not self.last_on_ground and self.on_ground:
            self.squish = 0.7  # Squish when landing
        elif self.squish < 1.0:
            self.squish += 0.05  # Recover squish
            if self.squish > 1.0:
                self.squish = 1.0
        self.last_on_ground = self.on_ground
        
        # Smooth visual position (does not affect physics or AI)
        interp_speed = 0.4  # 0 < interp_speed <= 1, higher is snappier
        self.visual_x += (self.x - self.visual_x) * interp_speed
        self.visual_y += (self.y - self.visual_y) * interp_speed
    
    def check_collision(self, platform):
        """
        Check collision with a platform
        """
        return (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y)
    
    def draw(self, screen):
        """
        Draw the player with animation, outline, shadow, and blinking eye
        """
        # Draw shadow
        shadow_width = int(self.width * 0.8)
        shadow_height = 8
        shadow_x = self.visual_x + (self.width - shadow_width) // 2
        shadow_y = self.visual_y + self.height - 2
        shadow_color = (50, 50, 50, 80)
        shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, shadow_color, (0, 0, shadow_width, shadow_height))
        screen.blit(shadow_surface, (shadow_x, shadow_y))

        # Draw squished body with black outline
        squish_h = int(self.height * self.squish)
        squish_y = self.visual_y + (self.height - squish_h)
        outline_rect = pygame.Rect(self.visual_x-2, squish_y-2, self.width+4, squish_h+4)
        pygame.draw.rect(screen, BLACK, outline_rect, border_radius=6)
        pygame.draw.rect(screen, RED, (self.visual_x, squish_y, self.width, squish_h), border_radius=4)

        # Eye blinking logic
        self.blink_timer += 1
        if self.blink_timer > 120 and not self.blink_state:
            if random.random() < 0.03:
                self.blink_state = True
                self.blink_timer = 0
        if self.blink_state:
            if self.blink_timer > 8:
                self.blink_state = False
                self.blink_timer = 0

        # Draw eye (blinks)
        if not self.blink_state:
            eye_x = self.visual_x + self.width - 10
            pygame.draw.circle(screen, WHITE, (int(eye_x), int(squish_y + 10)), 5)
        else:
            # Draw closed eye (line)
            eye_x = self.visual_x + self.width - 10
            pygame.draw.line(screen, WHITE, (int(eye_x-3), int(squish_y+10)), (int(eye_x+3), int(squish_y+10)), 2)

        # Draw legs (animated swinging)
        leg_phase = self.animation_frame * 0.5
        leg_swing = int(5 * math.sin(leg_phase))
        # Left leg
        pygame.draw.line(screen, BLACK, 
                        (self.visual_x + 7, squish_y + squish_h),
                        (self.visual_x + 7 + leg_swing, squish_y + squish_h + 10), 3)
        # Right leg
        pygame.draw.line(screen, BLACK,
                        (self.visual_x + self.width - 7, squish_y + squish_h),
                        (self.visual_x + self.width - 7 - leg_swing, squish_y + squish_h + 10), 3)

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Bungo")
        self.clock = pygame.time.Clock()
        
        # Create staggered platforms (left to right, bottom to top)
        self.platforms = [
            Platform(80, WINDOW_HEIGHT - 120, 160, 20),   # 1st platform (player start)
            Platform(300, WINDOW_HEIGHT - 200, 160, 20),  # 2nd
            Platform(520, WINDOW_HEIGHT - 280, 160, 20),  # 3rd
            Platform(300, WINDOW_HEIGHT - 360, 160, 20),  # 4th
            Platform(520, WINDOW_HEIGHT - 440, 160, 20),  # 5th (goal)
            Platform(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40),  # Ground
        ]
        
        # Create player on the first platform
        self.player = Player(100, WINDOW_HEIGHT - 150)
        
        # Create AI agent with higher learning rate and discount factor
        self.state_size = 30000  # Number of possible states (matches discretization)
        self.action_size = 3   # Number of possible actions (left, right, jump)
        self.agent = QLearningAgent(self.state_size, self.action_size, learning_rate=0.2, discount_factor=0.99, exploration_rate=0.8)
        
        # Training parameters
        self.episode = 0
        self.max_episodes = 1000
        # Goal is on the last platform
        self.goal_x = 520 + 80  # Center of last platform
        self.goal_y = WINDOW_HEIGHT - 440 - 10  # On top of last platform
        
        # Track which platforms have been reached for intermediate rewards
        self.platform_rewards = [False] * (len(self.platforms) - 1)  # Exclude ground
        
        # For lava bubble animation
        self.lava_bubbles = [
            {'x': random.randint(0, WINDOW_WIDTH), 'y': WINDOW_HEIGHT - 40 + random.randint(10, 35), 'r': random.randint(4, 10), 't': random.uniform(0, 2 * math.pi)}
            for _ in range(18)
        ]
        self.lava_anim_frame = 0
    
    def get_reward(self):
        """
        Calculate reward based on player's position and state
        """
        # Reward for moving right
        reward = 0.1 * (self.player.x - self.previous_x)
        
        # Intermediate rewards for reaching new platforms (excluding ground)
        for i, platform in enumerate(self.platforms[:-1]):  # Exclude ground
            if (not self.platform_rewards[i] and
                self.player.x + self.player.width > platform.x and
                self.player.x < platform.x + platform.width and
                abs(self.player.y + self.player.height - platform.y) < 10):
                reward += 10  # Small positive reward for new platform
                self.platform_rewards[i] = True
        
        # Heavy penalty for touching the bottom ground
        ground = self.platforms[-1]
        if (self.player.y + self.player.height >= ground.y and
            self.player.x + self.player.width > ground.x and
            self.player.x < ground.x + ground.width):
            reward = -200
            return True, reward
        
        # Penalty for falling off the screen
        if self.player.y > WINDOW_HEIGHT:
            reward = -100
            return True, reward
        
        # Reward for reaching goal (on last platform)
        if (self.player.x >= self.goal_x - 20 and 
            self.player.x <= self.goal_x + 20 and
            self.player.y >= self.goal_y - 20 and
            self.player.y <= self.goal_y + 20):
            reward = 200  # Increased reward for reaching the goal
            return True, reward
        
        # Penalty for ending episode far from the goal (left or too far right)
        # This is only applied if the episode times out (handled in run())
        return False, reward
    
    def reset_episode(self):
        """
        Reset the game state for a new episode
        """
        self.player = Player(100, WINDOW_HEIGHT - 150)  # Start on first platform
        self.previous_x = self.player.x
        self.episode_start_time = time.time()
        self.platform_rewards = [False] * (len(self.platforms) - 1)
    
    def run(self):
        """
        Main game loop with AI training
        """
        while self.episode < self.max_episodes:
            self.reset_episode()
            done = False
            timed_out = False
            
            # TEMPORARY EXPLORATION BOOST (moved earlier)
            if 150 < self.episode < 350:
                self.agent.exploration_rate = 0.2
            
            while not done:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                # Check episode timeout
                if time.time() - self.episode_start_time > EPISODE_TIMEOUT:
                    done = True
                    timed_out = True
                    continue
                
                # Get current state
                current_state = self.agent.get_state_index(
                    self.player.x, self.player.y,
                    self.player.velocity_x, self.player.velocity_y,
                    self.platforms
                )
                
                # Get action from AI
                action = self.agent.get_action(current_state)
                
                # Move player
                self.player.move(action)
                self.player.update(self.platforms)
                
                # Calculate reward
                done, reward = self.get_reward()
                
                # Get next state
                next_state = self.agent.get_state_index(
                    self.player.x, self.player.y,
                    self.player.velocity_x, self.player.velocity_y,
                    self.platforms
                )
                
                # Update AI
                self.agent.update(current_state, action, reward, next_state)
                
                # Update previous position
                self.previous_x = self.player.x
                
                # Draw everything
                self.screen.fill(WHITE)
                
                # Draw background (sky gradient)
                for i in range(WINDOW_HEIGHT):
                    color = (
                        int(180 + 40 * (i / WINDOW_HEIGHT)),
                        int(220 - 60 * (i / WINDOW_HEIGHT)),
                        int(255 - 80 * (i / WINDOW_HEIGHT))
                    )
                    pygame.draw.line(self.screen, color, (0, i), (WINDOW_WIDTH, i))

                # Draw platforms
                for idx, platform in enumerate(self.platforms):
                    # Draw soft shadow under platform
                    plat_shadow = pygame.Surface((platform.width, 8), pygame.SRCALPHA)
                    pygame.draw.ellipse(plat_shadow, (50,50,50,60), (0,0,platform.width,8))
                    self.screen.blit(plat_shadow, (platform.x, platform.y+platform.height-2))
                    # Thematic platform visuals
                    if idx == len(self.platforms) - 1:
                        # Bottom ground (lava)
                        # Draw lava base
                        pygame.draw.rect(self.screen, (220, 60, 20), (platform.x, platform.y, platform.width, platform.height))
                        # Draw lava waves
                        for x in range(platform.x, platform.x + platform.width, 20):
                            wave_y = platform.y + 20 + int(8 * math.sin(self.lava_anim_frame * 0.1 + x * 0.05))
                            pygame.draw.ellipse(self.screen, (255, 120, 40), (x, wave_y, 20, 12))
                        # Draw animated bubbles
                        for bubble in self.lava_bubbles:
                            bubble['y'] -= 0.7 + 0.5 * math.sin(self.lava_anim_frame * 0.1 + bubble['t'])
                            if bubble['y'] < platform.y + 5:
                                bubble['x'] = random.randint(platform.x, platform.x + platform.width)
                                bubble['y'] = platform.y + platform.height - random.randint(0, 10)
                                bubble['r'] = random.randint(4, 10)
                                bubble['t'] = random.uniform(0, 2 * math.pi)
                            pygame.draw.circle(self.screen, (255, 200, 80), (int(bubble['x']), int(bubble['y'])), bubble['r'])
                        # Draw lava highlight
                        pygame.draw.rect(self.screen, (255, 180, 80), (platform.x, platform.y, platform.width, 8))
                        # Draw dark outline
                        pygame.draw.rect(self.screen, (100, 30, 10), (platform.x, platform.y, platform.width, platform.height), 3, border_radius=6)
                    else:
                        # Rocky/grassy platforms
                        plat_color = (110, 90, 60)
                        grass_color = (60, 180, 60)
                        # Platform base
                        pygame.draw.rect(self.screen, plat_color, (platform.x, platform.y, platform.width, platform.height), border_radius=6)
                        # Grass top
                        pygame.draw.rect(self.screen, grass_color, (platform.x, platform.y, platform.width, 8), border_radius=6)
                        # Platform highlight
                        pygame.draw.rect(self.screen, (180, 160, 100), (platform.x, platform.y+platform.height-6, platform.width, 6), border_radius=6)
                        # Platform outline
                        pygame.draw.rect(self.screen, (60, 40, 20), (platform.x, platform.y, platform.width, platform.height), 2, border_radius=6)
                
                # Draw player
                self.player.draw(self.screen)
                
                # Draw goal (glowing gem with shine and pulse)
                goal_center = (self.goal_x, self.goal_y)
                # Draw gem (fixed size, with inner gleam)
                gem_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
                pygame.draw.polygon(gem_surface, (80, 255, 180, 220), [(16,0),(32,8),(28,32),(4,32),(0,8)])
                pygame.draw.polygon(gem_surface, (180, 255, 255, 180), [(16,4),(28,10),(25,28),(7,28),(4,10)])
                pygame.draw.ellipse(gem_surface, (255,255,255,120), (8,6,8,6))
                self.screen.blit(gem_surface, (goal_center[0]-16, goal_center[1]-16))
                # Gem shine
                if (self.lava_anim_frame//20)%2 == 0:
                    pygame.draw.ellipse(self.screen, (255,255,255,90), (goal_center[0]-7, goal_center[1]-13, 14, 8))
                # Gem outline
                pygame.draw.polygon(self.screen, (0,80,60), [
                    (goal_center[0], goal_center[1]-16),
                    (goal_center[0]+16, goal_center[1]-8),
                    (goal_center[0]+12, goal_center[1]+16),
                    (goal_center[0]-12, goal_center[1]+16),
                    (goal_center[0]-16, goal_center[1]-8)
                ], 2)
                
                # Draw episode info and timer with themed text
                font = pygame.font.Font(None, 40)
                time_left = max(0, EPISODE_TIMEOUT - (time.time() - self.episode_start_time))
                text_str = f"Episode: {self.episode}   Time: {time_left:.1f}s"
                # Gold/yellow text with dark outline
                text = font.render(text_str, True, (255, 220, 80))
                outline = font.render(text_str, True, (60, 40, 20))
                # Draw outline by blitting slightly offset in 4 directions
                for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                    self.screen.blit(outline, (12+dx, 12+dy))
                self.screen.blit(text, (12, 12))
                
                pygame.display.flip()
                self.clock.tick(FPS)
                self.lava_anim_frame += 1
            
            # End of episode
            # If episode timed out, penalize for distance from goal
            if timed_out:
                dist = abs(self.player.x - self.goal_x) + abs(self.player.y - self.goal_y)
                # Normalize distance to a penalty (max penalty -100, min 0)
                penalty = -min(100, int(dist / 3))
                # Update Q-table with penalty for last state/action
                self.agent.update(
                    self.agent.get_state_index(self.player.x, self.player.y, self.player.velocity_x, self.player.velocity_y, self.platforms),
                    0,  # No action, just penalize
                    penalty,
                    self.agent.get_state_index(self.player.x, self.player.y, self.player.velocity_x, self.player.velocity_y, self.platforms)
                )
            self.episode += 1
            self.agent.decay_exploration_rate()
            
            # Print progress
            if self.episode % 10 == 0:
                print(f"Episode: {self.episode}, Exploration Rate: {self.agent.exploration_rate:.2f}")

if __name__ == "__main__":
    game = Game()
    game.run() 