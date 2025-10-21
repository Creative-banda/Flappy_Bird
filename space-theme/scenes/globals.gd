extends Node2D


var health := 100
var score := 0
var bullet_count := 50
var game_speed := 1.0

func update_health(amount: int) -> void:
	print("Updating health by: ", amount)
	health += amount
	if health < 0:
		health = 0
	UI.update_health(health)

func update_score(amount: int) -> void:
	print("Updating score by: ", amount)
	score += amount
	UI.update_score(score)

func update_bullet_count(amount: int) -> void:
	# print("Updating bullet count by: ", amount)
	bullet_count += amount
	UI.update_bullet_count(bullet_count)
	print("Current bullet count: ", bullet_count)


func game_over() -> void:
	health = 100
	score = 0
	bullet_count = 50
	# wait a moment before changing scene
	await get_tree().create_timer(1.0).timeout
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
