extends CharacterBody2D

# Basic enemy AI
# Chases the player and deals damage on contact

signal destroyed(points: int)

@export var speed := 150.0
@export var health := 30
@export var damage := 10
@export var point_value := 100

var target: Node2D = null

# Initialize enemy
func _ready() -> void:
	add_to_group("enemies")

# Move towards the target each physics frame
func _physics_process(delta: float) -> void:
	if target == null or not is_instance_valid(target):
		return
	
	var direction = (target.global_position - global_position).normalized()
	velocity = direction * speed
	move_and_slide()
	
	_rotate_towards_target()

# Rotate to face the target
func _rotate_towards_target() -> void:
	if target:
		look_at(target.global_position)

# Apply damage to the enemy
func take_damage(amount: int) -> void:
	health -= amount
	_flash_on_hit()
	
	if health <= 0:
		_die()

# Visual feedback when hit
func _flash_on_hit() -> void:
	var tween = create_tween()
	tween.tween_property($Sprite2D, "modulate", Color.RED, 0.05)
	tween.tween_property($Sprite2D, "modulate", Color.WHITE, 0.05)

# Handle enemy death
func _die() -> void:
	destroyed.emit(point_value)
	_spawn_explosion()
	queue_free()

# Create explosion effect on death
func _spawn_explosion() -> void:
	var explosion_scene = preload("res://scenes/explosion.tscn")
	var explosion = explosion_scene.instantiate()
	explosion.position = global_position
	get_parent().add_child(explosion)

# Deal damage on collision with player
func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.take_damage(damage)
