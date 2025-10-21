extends Node2D


@onready var health_icon: Sprite2D = $HpIcon
@onready var ammo_icon: Sprite2D = $Bullet

var item_type: String

func _ready() -> void:
	# Select a random item type
	item_type = ['health', 'ammo'][randi() % 2]
	match item_type:
		"health":
			health_icon.visible = true
		"ammo":
			ammo_icon.visible = true


var rotation_speed := randf_range(-2.0, 2.0)

func _process(delta: float) -> void:
	# Move item leftwards
	position.x -= 100 * delta * Globals.game_speed
	# Apply random rotation
	rotation += rotation_speed * delta 


func _on_area_2d_body_entered(body:Node2D) -> void:
	if body.is_in_group("player"):
		if item_type == "health":
			Globals.update_health(30)
		elif item_type == "ammo":
			Globals.update_bullet_count(10)
		queue_free()  # Remove item after collection
		AudioManager.play_sound("collect")
