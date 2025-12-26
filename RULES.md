# GDSmeller Rules Reference

This document provides a comprehensive reference for all rules implemented in GDSmeller.

## Table of Contents

- [Readability Rules (R-series)](#readability-rules)
- [Security Rules (S-series)](#security-rules)
- [Performance Rules (P-series)](#performance-rules)

---

## Readability Rules

### R001: Line Too Long

**Severity:** Warning  
**Category:** Readability

**Description:**
Lines should not exceed the configured maximum length (default: 100 characters). Long lines make code harder to read, especially on smaller screens or in side-by-side diff views.

**Good Example:**
```gdscript
var player_name = get_player_name()
var player_position = get_player_position()
```

**Bad Example:**
```gdscript
var player_data = {"name": get_player_name(), "position": get_player_position(), "health": get_player_health(), "mana": get_player_mana()}
```

**Configuration:**
You can adjust the maximum line length in your `.gdsmeller.json`:
```json
{
  "max_line_length": 120
}
```

---

### R002: Missing Class Docstring

**Severity:** Info  
**Category:** Readability

**Description:**
Classes should have documentation comments explaining their purpose and usage.

**Good Example:**
```gdscript
# Manages player state and behavior
class PlayerController:
    var health = 100
```

**Bad Example:**
```gdscript
class PlayerController:
    var health = 100
```

---

### R003: Missing Function Docstring

**Severity:** Info  
**Category:** Readability

**Description:**
Public functions (not starting with `_`) should have documentation comments. This helps other developers understand the purpose and usage of functions.

**Good Example:**
```gdscript
# Calculates damage based on attack power and defense
func calculate_damage(attack, defense):
    return max(0, attack - defense)
```

**Bad Example:**
```gdscript
func calculate_damage(attack, defense):
    return max(0, attack - defense)
```

**Note:** Private functions (starting with `_`) are exempt from this rule.

---

### R004: Inconsistent Indentation

**Severity:** Error  
**Category:** Readability

**Description:**
Mixing tabs and spaces for indentation leads to inconsistent formatting and potential syntax issues.

**Good Example:**
```gdscript
func _ready():
    var x = 1
    var y = 2
```

**Bad Example:**
```gdscript
func _ready():
    var x = 1
	var y = 2  # This line uses tabs
```

---

## Security Rules

### S001: Hardcoded Password

**Severity:** Error  
**Category:** Security

**Description:**
Hardcoding passwords or other sensitive credentials in source code is a serious security vulnerability. Credentials should be stored in environment variables or secure configuration systems.

**Good Example:**
```gdscript
var password = OS.get_environment("DB_PASSWORD")
# Or load from secure config
var password = config.get_value("credentials", "password")
```

**Bad Example:**
```gdscript
var password = "mysecret123"
```

---

### S002: Unsafe Eval/Execute

**Severity:** Warning  
**Category:** Security

**Description:**
Using `Expression.parse()` or similar dynamic execution with untrusted input can lead to code injection vulnerabilities.

**Good Example:**
```gdscript
# Validate and sanitize input before parsing
func evaluate_safe_expression(expr_string):
    if validate_expression(expr_string):
        return Expression.parse(expr_string)
    return null
```

**Bad Example:**
```gdscript
# Directly parsing user input
func evaluate_user_input(user_input):
    return Expression.parse(user_input).execute()
```

---

### S003: SQL Injection Risk

**Severity:** Error  
**Category:** Security

**Description:**
Building SQL queries through string concatenation can lead to SQL injection vulnerabilities. Always use parameterized queries.

**Good Example:**
```gdscript
# Using parameterized query (pseudo-code)
func get_user(user_id):
    return db.query("SELECT * FROM users WHERE id = ?", [user_id])
```

**Bad Example:**
```gdscript
func get_user(user_id):
    var query = "SELECT * FROM users WHERE id = " + str(user_id)
    return db.query(query)
```

---

### S004: Insecure Random

**Severity:** Warning  
**Category:** Security

**Description:**
Functions like `randi()` and `randf()` are not cryptographically secure. For security-critical purposes (tokens, keys, passwords), use `Crypto.generate_random_bytes()`.

**Good Example:**
```gdscript
func generate_session_token():
    var crypto = Crypto.new()
    return crypto.generate_random_bytes(32).hex_encode()
```

**Bad Example:**
```gdscript
func generate_session_token():
    return str(randi()) + str(randi())
```

---

## Performance Rules

### P001: Process in Loop

**Severity:** Warning  
**Category:** Performance

**Description:**
Expensive operations (like `get_node()`, `instance()`, etc.) inside loops within `_process()` or `_physics_process()` can cause performance issues. Cache results outside loops.

**Good Example:**
```gdscript
onready var enemies = get_tree().get_nodes_in_group("enemies")

func _process(delta):
    for enemy in enemies:
        enemy.update(delta)
```

**Bad Example:**
```gdscript
func _process(delta):
    for i in range(10):
        var enemy = get_node("Enemy" + str(i))
        enemy.update(delta)
```

---

### P002: String Concatenation in Loop

**Severity:** Warning  
**Category:** Performance

**Description:**
String concatenation in loops creates many temporary string objects, causing poor performance. Use arrays and `join()` instead.

**Good Example:**
```gdscript
func build_string():
    var parts = []
    for i in range(100):
        parts.append("part" + str(i))
    return parts.join("")
```

**Bad Example:**
```gdscript
func build_string():
    var result = ""
    for i in range(100):
        result += "part" + str(i)
    return result
```

---

### P003: Signal Not Disconnected

**Severity:** Info  
**Category:** Performance

**Description:**
Signals connected with `connect()` should be disconnected in cleanup functions (like `_exit_tree()`) to prevent memory leaks.

**Good Example:**
```gdscript
func _ready():
    some_signal.connect("event", self, "_on_event")

func _exit_tree():
    some_signal.disconnect("event", self, "_on_event")
```

**Bad Example:**
```gdscript
func _ready():
    some_signal.connect("event", self, "_on_event")
# No disconnect call anywhere
```

---

### P004: Get Node in Process

**Severity:** Warning  
**Category:** Performance

**Description:**
Calling `get_node()` or using the `$` operator in `_process()` or `_physics_process()` every frame is inefficient. Cache node references in `_ready()` or use `onready`.

**Good Example:**
```gdscript
onready var player = $Player

func _process(delta):
    player.update(delta)
```

**Bad Example:**
```gdscript
func _process(delta):
    var player = get_node("Player")
    player.update(delta)
```

---

## Disabling Rules

To disable specific rules, add them to your `.gdsmeller.json`:

```json
{
  "disabled_rules": ["R003", "P003"]
}
```

## Custom Rules

For information on creating custom rules, see the main README.md file.
