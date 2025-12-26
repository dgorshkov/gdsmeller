extends Control

# Heads-Up Display controller
# Shows player health, score, and level information

@onready var health_bar = $HealthBar
@onready var score_label = $ScoreLabel
@onready var level_label = $LevelLabel
@onready var game_over_panel = $GameOverPanel

# Initialize HUD
func _ready() -> void:
	game_over_panel.visible = false

# Update health bar display
func update_health(current: int, maximum: int) -> void:
	health_bar.max_value = maximum
	health_bar.value = current

# Update score display
func update_score(score: int) -> void:
	score_label.text = "Score: %d" % score

# Update level display
func update_level(level: int) -> void:
	level_label.text = "Level %d" % level

# Show game over screen
func show_game_over() -> void:
	game_over_panel.visible = true

# Hide game over screen
func hide_game_over() -> void:
	game_over_panel.visible = false
