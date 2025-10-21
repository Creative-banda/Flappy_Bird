extends Node2D


var direction := 1
var speed := 600


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	position.x += direction * speed * delta * Globals.game_speed  # Move bullet horizontally

	if position.x > get_viewport_rect().size.x or position.x < 0:
		queue_free()  # Remove bullet if it goes off-screen

func _on_bullet_body_entered(body:Node2D) -> void:
	if body.is_in_group("enemy"):
		body.take_damage()
		Globals.update_score(10)
		queue_free()
	
	if body.is_in_group("obstacle"):
		body.take_damage()
		Globals.update_score(5)
		queue_free()
	
	if body.is_in_group("player"):
		body.take_damage(10)
		queue_free()

func _on_bullet_area_entered(area:Area2D) -> void:
	var parent = area.get_parent()
	if parent.is_in_group("obstacle"):
		parent.take_damage()
		Globals.update_score(5)
		queue_free()
