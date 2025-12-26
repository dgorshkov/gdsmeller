extends CharacterBody2D

# Player character controller
# Handles player movement, shooting, and health management

signal died
signal health_changed(new_health: int)
signal score_changed(new_score: int)

@export var speed := 300.0
@export var max_health := 100
@export var shoot_cooldown := 0.2

@onready var sprite = $Sprite2D
@onready var collision_shape = $CollisionShape2D
@onready var shoot_timer = $ShootTimer
@onready var invincibility_timer = $InvincibilityTimer

var health: int
var score: int = 0
var can_shoot := true
var invincible := false

# Initialize player state
func _ready() -> void:
	health = max_health
	shoot_timer.wait_time = shoot_cooldown

# Process player input each physics frame
func _physics_process(delta: float) -> void:
	var input_vector = _get_input_vector()
	velocity = input_vector * speed
	move_and_slide()
	
	_clamp_to_screen()
	_handle_shooting()

# Get the normalized input direction vector
func _get_input_vector() -> Vector2:
	var input_x = Input.get_axis("move_left", "move_right")
	var input_y = Input.get_axis("move_up", "move_down")
	return Vector2(input_x, input_y).normalized()

# Keep player within screen bounds
func _clamp_to_screen() -> void:
	var viewport_size = get_viewport_rect().size
	position.x = clamp(position.x, 0, viewport_size.x)
	position.y = clamp(position.y, 0, viewport_size.y)

# Handle shooting input
func _handle_shooting() -> void:
	if Input.is_action_pressed("shoot") and can_shoot:
		_shoot()

# Fire a bullet
func _shoot() -> void:
	can_shoot = false
	shoot_timer.start()
	
	var bullet_scene = preload("res://scenes/bullet.tscn")
	var bullet = bullet_scene.instantiate()
	bullet.position = global_position + Vector2(0, -20)
	bullet.direction = Vector2.UP
	get_parent().add_child(bullet)

# Apply damage to the player
func take_damage(amount: int) -> void:
	if invincible:
		return
	
	health -= amount
	health_changed.emit(health)
	
	if health <= 0:
		_die()
	else:
		_start_invincibility()

# Handle player death
func _die() -> void:
	died.emit()
	visible = false
	collision_shape.set_deferred("disabled", true)

# Start temporary invincibility after taking damage
func _start_invincibility() -> void:
	invincible = true
	invincibility_timer.start()
	_flash_sprite()

# Flash the sprite during invincibility
func _flash_sprite() -> void:
	var tween = create_tween()
	tween.set_loops(5)
	tween.tween_property(sprite, "modulate:a", 0.3, 0.1)
	tween.tween_property(sprite, "modulate:a", 1.0, 0.1)

# Add to player score
func add_score(points: int) -> void:
	score += points
	score_changed.emit(score)

# Timer callbacks
func _on_shoot_timer_timeout() -> void:
	can_shoot = true

func _on_invincibility_timer_timeout() -> void:
	invincible = false
	sprite.modulate.a = 1.0
