extends Control

# Main menu controller
# Handles menu navigation and game start

@onready var start_button = $VBoxContainer/StartButton
@onready var options_button = $VBoxContainer/OptionsButton
@onready var quit_button = $VBoxContainer/QuitButton
@onready var high_score_label = $HighScoreLabel
@onready var options_panel = $OptionsPanel

# Initialize menu
func _ready() -> void:
	_connect_signals()
	_update_high_score()

# Connect button signals
func _connect_signals() -> void:
	start_button.pressed.connect(_on_start_pressed)
	options_button.pressed.connect(_on_options_pressed)
	quit_button.pressed.connect(_on_quit_pressed)

# Update high score display
func _update_high_score() -> void:
	var game_manager = get_node_or_null("/root/GameManager")
	if game_manager:
		high_score_label.text = "High Score: %d" % game_manager.high_score

# Start the game
func _on_start_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/main.tscn")

# Show options menu
func _on_options_pressed() -> void:
	options_panel.visible = true

# Quit the game
func _on_quit_pressed() -> void:
	get_tree().quit()

# Close options panel
func _on_options_back_pressed() -> void:
	options_panel.visible = false

# Handle escape key
func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		if options_panel.visible:
			options_panel.visible = false
