extends Node2D

# Main game scene controller
# Handles game initialization and core game loop

@onready var player = $Player
@onready var enemy_container = $EnemyContainer
@onready var hud = $CanvasLayer/HUD
@onready var spawn_timer = $SpawnTimer

var game_running := false
var current_level := 1

# Initialize the game
func _ready() -> void:
	randomize()
	_start_game()

# Start or restart the game
func _start_game() -> void:
	game_running = true
	current_level = 1
	spawn_timer.start()
	hud.update_level(current_level)

# Handle global input events
func _input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		_toggle_pause()
	
	if event.is_action_pressed("restart") and not game_running:
		_start_game()

# Toggle game pause state
func _toggle_pause() -> void:
	get_tree().paused = not get_tree().paused

# Spawn enemies based on current level
func _on_spawn_timer_timeout() -> void:
	if not game_running:
		return
	
	var enemy_count = min(current_level + 2, 10)
	for i in range(enemy_count):
		_spawn_enemy()

# Create a new enemy instance
func _spawn_enemy() -> void:
	var enemy_scene = preload("res://scenes/enemy.tscn")
	var enemy = enemy_scene.instantiate()
	enemy.position = _get_random_spawn_position()
	enemy.target = player
	enemy_container.add_child(enemy)

# Calculate a random spawn position outside the viewport
func _get_random_spawn_position() -> Vector2:
	var viewport_size = get_viewport_rect().size
	var side = randi() % 4
	match side:
		0:  # Top
			return Vector2(randf() * viewport_size.x, -50)
		1:  # Right
			return Vector2(viewport_size.x + 50, randf() * viewport_size.y)
		2:  # Bottom
			return Vector2(randf() * viewport_size.x, viewport_size.y + 50)
		3:  # Left
			return Vector2(-50, randf() * viewport_size.y)
	return Vector2.ZERO

# Handle player death
func _on_player_died() -> void:
	game_running = false
	spawn_timer.stop()
	_clear_enemies()
	hud.show_game_over()

# Remove all enemies from the scene
func _clear_enemies() -> void:
	for enemy in enemy_container.get_children():
		enemy.queue_free()

# Progress to the next level
func advance_level() -> void:
	current_level += 1
	hud.update_level(current_level)
	spawn_timer.wait_time = max(0.5, 2.0 - (current_level * 0.1))
