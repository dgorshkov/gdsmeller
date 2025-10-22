extends Node

# Example of problematic GDScript code

class PlayerData:
	var name = "Player"
	var health = 100

var password = "mysecret123"

func process_player():
	var result = ""
	for i in range(100):
		result += "data"

func _process(delta):
	var player = get_node("Player")
	for i in range(10):
		var enemy = $Enemy
		enemy.update()

func generate_token():
	return str(randi())

func query_user(user_id):
	var query = "SELECT * FROM users WHERE id = " + str(user_id)
	return query
