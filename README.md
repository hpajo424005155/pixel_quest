# pixel_quest

# Pixel Quest: The Last Coin

**Author:** HARVEY PAJO

**Course:** Final Project — Game Development with Pygame

**Date:** May 22, 2026

## How to Run the Game

1. **Install Python 3.12** from python.org
2. **Install Pygame:** `pip install pygame-ce`
3. **Navigate to game folder:** `cd pixel_quest`
4. **Run the game:** `python main.py`

## Game Controls

| Action | Keys |
|--------|------|
| Move Left | ← Arrow or A |
| Move Right | → Arrow or D |
| Move Up | ↑ Arrow or W |
| Move Down | ↓ Arrow or S |
| Restart (after game over/win) | SPACE |
| Quit Game | Close window or Ctrl+C |

## Game Features

- **3-frame player walking animation** (cycles when moving left/right)
- **Idle frame** when standing still (Mario-style)
- **Collect coins** for +10 points each
- **Avoid red enemies** - each touch costs 1 life
- **Invincibility frames** after getting hit (brief blinking)
- **Win condition:** Collect 15 coins
- **Lose condition:** Run out of 3 lives
- **Background music** (looping)
- **Sound effects** for collecting, getting hurt, and victory
- **Enemies bounce off walls** creating unpredictable movement

## Technical Requirements Met

- Game loop at 60 FPS (`clock.tick(60)`)
- Continuous keyboard input (`pygame.key.get_pressed()`)
- Boundary detection (player cannot leave screen)
- Enemies and collectible coins
- Sprite collision detection (`spritecollide`)
- Real-time scoring system
- Win condition AND game over condition
- 3+ player animation frames
- Visible background image
- On-screen UI (score, lives)
- Sound effects (3 different sounds)
- Looping background music
- Proper mixer initialization
- Balanced volume levels

## Reflection Questions

### 1. What was the hardest part of developing your game, and how did you solve it?

The hardest part was getting the file paths to work correctly because Pygame couldn't find my images and sounds. I solved this by using os.path.dirname(os.path.abspath(__file__)) to get the correct folder location, which made the game work no matter where it was installed. I also struggled with enemy collision detection, but I fixed it by adding invincibility frames so the player doesn't lose all lives instantly when touching an enemy.

### 2. How did adding sound effects and animations improve the player experience?

Adding sound effects made the game feel more rewarding because every coin collected plays a satisfying "collect" sound, and getting hurt plays a clear warning sound. The walking animation made the player character feel alive and responsive, while the idle frame when standing still made the game feel more polished like professional games such as Mario. The background music also set the mood and kept players engaged throughout the gameplay.

### 3. What feature are you most proud of, and why?

I am most proud that I got the entire game to run without crashing. Getting the player movement, enemy bouncing, coin collection, scoring system, and win/lose conditions all working together was challenging, but seeing everything work at the end felt rewarding.

### 4. If you had two more weeks, what would you add or improve?

If I had two more weeks, I would add a main menu screen with a Start button and a high score system that saves the best score to a file. I would also add power-ups like a speed boost or temporary shield, and a pause function when pressing the 'P' key. Finally, I would add multiple enemy types with different speeds and movement patterns to make the game more challenging as the score increases.
