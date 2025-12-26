extends Area2D

# Collectible power-up
# Provides temporary buffs to the player

enum PowerupType {
	HEALTH,
	SPEED,
	DAMAGE,
	SHIELD
}

@export var type: PowerupType = PowerupType.HEALTH
@export var duration := 5.0
@export var effect_value := 25

@onready var sprite = $Sprite2D
@onready var animation_player = $AnimationPlayer

var collected := false

# Initialize powerup
func _ready() -> void:
	_set_appearance()
	animation_player.play("float")

# Set visual appearance based on type
func _set_appearance() -> void:
	match type:
		PowerupType.HEALTH:
			sprite.modulate = Color.GREEN
		PowerupType.SPEED:
			sprite.modulate = Color.YELLOW
		PowerupType.DAMAGE:
			sprite.modulate = Color.RED
		PowerupType.SHIELD:
			sprite.modulate = Color.BLUE

# Handle collection by player
func _on_body_entered(body: Node2D) -> void:
	if collected:
		return
	
	if body.is_in_group("player"):
		collected = true
		_apply_effect(body)
		_play_collect_effect()

# Apply the powerup effect to the player
func _apply_effect(player: Node2D) -> void:
	match type:
		PowerupType.HEALTH:
			if player.has_method("heal"):
				player.heal(effect_value)
		PowerupType.SPEED:
			if player.has_method("boost_speed"):
				player.boost_speed(effect_value, duration)
		PowerupType.DAMAGE:
			if player.has_method("boost_damage"):
				player.boost_damage(effect_value, duration)
		PowerupType.SHIELD:
			if player.has_method("activate_shield"):
				player.activate_shield(duration)

# Visual and audio feedback for collection
func _play_collect_effect() -> void:
	# Disable collision
	$CollisionShape2D.set_deferred("disabled", true)
	
	# Animate and remove
	var tween = create_tween()
	tween.parallel().tween_property(self, "scale", Vector2(1.5, 1.5), 0.2)
	tween.parallel().tween_property(sprite, "modulate:a", 0.0, 0.2)
	tween.tween_callback(queue_free)
