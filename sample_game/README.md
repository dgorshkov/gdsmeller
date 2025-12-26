# Space Shooter Sample

A small but realistic sample Godot 4.x game for testing [gdsmeller](https://github.com/dgorshkov/gdsmeller).

## Purpose

This sample game demonstrates a typical game project structure with:
- Multiple GDScript files following common game development patterns
- A mix of well-written code and intentional code smells for testing gdsmeller

## Game Structure

```
sample_game/
├── project.godot          # Godot project configuration
├── scripts/
│   ├── main.gd           # Main game scene controller
│   ├── player.gd         # Player character controller
│   ├── enemy.gd          # Enemy AI
│   ├── bullet.gd         # Projectile behavior
│   ├── hud.gd            # Heads-up display
│   ├── game_manager.gd   # Global game state (contains code smells)
│   ├── spawner.gd        # Enemy/powerup spawner (contains code smells)
│   ├── powerup.gd        # Collectible powerups
│   ├── audio_manager.gd  # Audio system
│   ├── menu.gd           # Main menu
│   └── utils.gd          # Utility functions
└── README.md
```

## Intentional Code Smells

The following files contain intentional code smells for testing gdsmeller:

### game_manager.gd
- **S001**: Hardcoded password (`db_password = "supersecretpwd123"`)
- **S003**: SQL injection risk (string concatenation in query)
- **S004**: Insecure random for session token generation (`session_token = str(randi())`)
- **P004**: get_node in `_process` function
- **R003**: Missing function docstrings

### spawner.gd
- **S001**: Hardcoded password (`password = "admin123"`)
- **S004**: Insecure random for token generation (`secret_token = str(randi())`)
- **P001**: Expensive operations in loop within `_process`
- **P002**: String concatenation in loop
- **P004**: get_node in `_process` function
- **R003**: Missing function docstrings

## Testing with gdsmeller

Run gdsmeller on this sample game:

```bash
# From the repository root
python -m gdsmeller.main --path sample_game/ --output-format text

# JSON output
python -m gdsmeller.main --path sample_game/ --output-format json

# GitHub Actions format
python -m gdsmeller.main --path sample_game/ --output-format github
```

## Expected Results

When running gdsmeller on this sample game, you should see approximately:
- **3 Errors**: Hardcoded passwords and SQL injection
- **6 Warnings**: Insecure random usage, performance issues in `_process`
- **20 Info**: Missing function docstrings across various files

Example output:
```
Found 29 issue(s):

sample_game/scripts/game_manager.gd:
  ✗ Line 13: [S001] Hardcoded password detected. Use environment variables or secure storage instead
  ⚠ Line 59: [S004] Using insecure random function for security-critical purpose
  ⚠ Line 71: [P004] get_node() or $ called in _process(). Cache the reference in _ready()
  ✗ Line 78: [S003] Potential SQL injection risk. Use parameterized queries

sample_game/scripts/spawner.gd:
  ✗ Line 14: [S001] Hardcoded password detected
  ⚠ Line 24: [P001] Expensive operation in loop within _process() function
  ⚠ Line 24: [P004] get_node() or $ called in _process()
  ⚠ Line 54: [S004] Using insecure random function for security-critical purpose
  ⚠ Line 61: [P002] String concatenation in loop detected

Summary:
  Total issues: 29
  Errors: 3
  Warnings: 6
  Info: 20
```
