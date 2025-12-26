extends Node

# Utility functions for the game
# Contains helper methods for common operations

class_name GameUtils

# Mathematical utilities

# Calculate distance between two points
static func distance_between(a: Vector2, b: Vector2) -> float:
	return a.distance_to(b)

# Linear interpolation with clamping
static func lerp_clamped(from: float, to: float, weight: float) -> float:
	return clamp(lerpf(from, to, weight), min(from, to), max(from, to))

# Random utilities

# Get a random point within a rectangle
static func random_point_in_rect(rect: Rect2) -> Vector2:
	var x = randf_range(rect.position.x, rect.position.x + rect.size.x)
	var y = randf_range(rect.position.y, rect.position.y + rect.size.y)
	return Vector2(x, y)

# Get a random direction vector
static func random_direction() -> Vector2:
	var angle = randf() * TAU
	return Vector2(cos(angle), sin(angle))

# Formatting utilities

# Format time as MM:SS
static func format_time(seconds: float) -> String:
	var mins = int(seconds) / 60
	var secs = int(seconds) % 60
	return "%02d:%02d" % [mins, secs]

# Format large numbers with comma separators
static func format_number(num: int) -> String:
	var str_num = str(abs(num))
	var result = ""
	var count = 0
	for i in range(str_num.length() - 1, -1, -1):
		if count > 0 and count % 3 == 0:
			result = "," + result
		result = str_num[i] + result
		count += 1
	if num < 0:
		result = "-" + result
	return result

# Array utilities

# Shuffle an array in place
static func shuffle_array(arr: Array) -> void:
	for i in range(arr.size() - 1, 0, -1):
		var j = randi() % (i + 1)
		var temp = arr[i]
		arr[i] = arr[j]
		arr[j] = temp

# Pick a random element from an array
static func random_element(arr: Array):
	if arr.is_empty():
		return null
	return arr[randi() % arr.size()]

# Color utilities

# Lerp between two colors
static func color_lerp(from: Color, to: Color, weight: float) -> Color:
	return from.lerp(to, weight)

# Generate a random color
static func random_color() -> Color:
	return Color(randf(), randf(), randf())
