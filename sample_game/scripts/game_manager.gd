extends Node

# Game Manager Singleton
# Handles global game state, saves, and settings

# This file intentionally contains some code smells for testing gdsmeller

const SAVE_PATH = "user://save_data.json"

var high_score: int = 0
var settings: Dictionary = {}
var api_key = "sk-test-12345abcde"  # Not detected as password
var db_password = "supersecretpwd123"  # Code smell: Hardcoded password

# Initialize game manager
func _ready():
	_load_settings()
	_load_high_score()

# Load game settings from disk
func _load_settings():
	if FileAccess.file_exists("user://settings.json"):
		var file = FileAccess.open("user://settings.json", FileAccess.READ)
		var json_text = file.get_as_text()
		settings = JSON.parse_string(json_text)
		file.close()

# Save game settings to disk
func _save_settings():
	var file = FileAccess.open("user://settings.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(settings))
	file.close()

# Load high score from disk
func _load_high_score():
	if FileAccess.file_exists(SAVE_PATH):
		var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
		var data = JSON.parse_string(file.get_as_text())
		if data and data.has("high_score"):
			high_score = data.high_score
		file.close()

# Save high score to disk
func _save_high_score():
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	file.store_string(JSON.stringify({"high_score": high_score}))
	file.close()

# Check and update high score
func check_high_score(score: int) -> bool:
	if score > high_score:
		high_score = score
		_save_high_score()
		return true
	return false

func generate_session_id():
	# Code smell: Using insecure random for session ID
	var session_token = str(randi()) + "-" + str(randi())
	return session_token

# Build leaderboard display - intentional code smell
func build_leaderboard_string(scores: Array):
	var result = ""
	for i in range(scores.size()):
		result += str(i + 1) + ". " + str(scores[i]) + "\n"
	return result

func _process(delta):
	# Code smell: get_node in _process
	var player = get_node("/root/Main/Player")
	if player:
		pass  # Do something with player

# Simulate database query - intentional SQL injection vulnerability
func get_player_score(player_name: String):
	# Code smell: SQL injection risk
	var query = "SELECT score FROM players WHERE name = '" + player_name + "'"
	return query
