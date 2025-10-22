extends Node

# Example of well-written GDScript code

# Player data class
class PlayerData:
	# Player's display name
	var name = "Player"
	# Player's current health points
	var health = 100

# Password loaded from environment
var password = ""

# Process player data efficiently
func process_player():
	# Use array for string building
	var parts = []
	for i in range(100):
		parts.append("data")
	return parts.join("")

# Cache node references
onready var player = $Player
onready var enemy = $Enemy

# Process function with cached references
func _process(delta):
	# Use cached references
	if player:
		player.update(delta)

# Generate secure token
func generate_token():
	# Use Crypto for security-critical randomness
	return Crypto.new().generate_random_bytes(16).hex_encode()

# Use parameterized queries (pseudo-code)
func query_user(user_id):
	# This is just an example - use proper DB library
	return db.query("SELECT * FROM users WHERE id = ?", [user_id])
