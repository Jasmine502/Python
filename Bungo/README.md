# AI Platformer Learning Project

This project demonstrates a simple reinforcement learning implementation where an AI agent learns to complete a platformer level using Q-learning.

## Project Structure
- `game.py`: Contains the main game logic and platformer mechanics
- `q_learning_agent.py`: Implements the Q-learning algorithm
- `requirements.txt`: Lists the project dependencies

## Setup
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python game.py
```

## How it Works
The AI agent learns through trial and error using a Q-learning algorithm. It receives:
- Positive rewards for moving right (towards the goal)
- Negative rewards for falling off platforms
- A large positive reward for reaching the goal

The agent's state is represented by its position and velocity, and it can perform actions like moving left, right, and jumping.

## Learning Process
1. The agent starts with no knowledge (Q-table initialized to zeros)
2. Through multiple episodes, it:
   - Explores the environment
   - Updates its Q-values based on rewards
   - Gradually learns the optimal path to the goal

Watch as the agent improves its performance over time! 