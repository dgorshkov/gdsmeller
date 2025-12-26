extends Area2D

# Projectile that damages enemies on contact

@export var speed := 500.0
@export var damage := 10
@export var lifetime := 2.0

var direction := Vector2.UP

# Initialize bullet
func _ready() -> void:
	var timer = get_tree().create_timer(lifetime)
	timer.timeout.connect(_on_lifetime_expired)

# Move the bullet each frame
func _process(delta: float) -> void:
	position += direction * speed * delta

# Handle collision with enemies
func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("enemies"):
		body.take_damage(damage)
		queue_free()

# Remove bullet when it expires
func _on_lifetime_expired() -> void:
	queue_free()
