# Space Dodge

A simple and fun space dodging game made with Python and Pygame.

Dodge falling asteroids for as long as you can!

## Features

- 3 lives system
- High score saving
- Random backgrounds (up to 10)
- Different asteroid types (small/fast, medium, big/slow)
- Support for custom ship & asteroid images
- Clean start screen and game over screen

## Requirements

- Python 3
- Pygame

```bash
pip install pygame
```

## How to Run

```bash
python main.py
```

## Controls

| Key        | Action                  |
| ---------- | ----------------------- |
| ← → or A D | Move                    |
| SPACE      | Start game              |
| R          | Restart after game over |

## Optional Images

Place these files in the same folder for better graphics:

- `ship.png` – player spaceship
- `asteroid1.png` – small asteroid
- `asteroid2.png` – medium asteroid
- `asteroid3.png` – big asteroid
- `bg1.jpeg` to `bg10.jpeg` – different backgrounds

If images are missing, the game uses built-in fallback graphics.
