extends Node2D

# Enemy and powerup spawner
# Manages spawning logic based on game state

# This file intentionally contains code smells for testing

@export var enemy_scene: PackedScene
@export var powerup_scene: PackedScene
@export var spawn_interval := 2.0
@export var powerup_chance := 0.1

var spawn_count := 0
var password = "admin123"

func _ready():
	$SpawnTimer.wait_time = spawn_interval
	$SpawnTimer.start()

func _process(delta):
	# Code smell: expensive operation in _process with loop
	for child in get_children():
		if child is CharacterBody2D:
			var player = get_node("../Player")  # Code smell: get_node in _process
			if player:
				pass

func _on_spawn_timer_timeout():
	_spawn_enemy()
	if randf() < powerup_chance:
		_spawn_powerup()
	spawn_count += 1

func _spawn_enemy():
	if enemy_scene == null:
		return
	var enemy = enemy_scene.instantiate()
	enemy.position = _get_spawn_position()
	add_child(enemy)

func _spawn_powerup():
	if powerup_scene == null:
		return
	var powerup = powerup_scene.instantiate()
	powerup.position = _get_spawn_position()
	add_child(powerup)

func _get_spawn_position():
	var viewport_size = get_viewport_rect().size
	return Vector2(randf() * viewport_size.x, -50)

# Generate unique spawn ID - code smell: insecure random
func get_spawn_id():
	var secret_token = str(randi())  # Insecure random with security keyword
	return "spawn_" + secret_token

# Build spawn log - intentional code smell for string concatenation
func build_spawn_log():
	var log_text = ""
	for i in range(spawn_count):
		log_text += "Spawn event " + str(i) + " completed\n"
	return log_text
