extends Node2D


@onready var sprite: Sprite2D = $Sprite2D
var rotation_direction = 1 if randf() > 0.5 else -1
var health = 100

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Load a random texture from the "res://assets/obstical/" directory
	var texture_path = "res://assets/obstical/" + str(randi() % 1) + ".png"
	var texture = load(texture_path)
	sprite.texture = texture
 

func _process(delta: float) -> void:
	# Move obstical leftwards
	position.x -= 200 * delta * Globals.game_speed  # Adjust speed as needed

	# rotate obstical
	rotation_degrees += rotation_direction * 90 * delta  # Rotate 90 degrees per second in random direction
	# Remove obstical if it goes off-screen
	if position.x < -sprite.texture.get_size().x:
		queue_free()


func take_damage() -> void:
	health -= 50
	if health <= 0:
		AudioManager.play_sound("rock_smash")
		queue_free()  # Remove obstacle on damage


func _on_area_2d_body_entered(body:Node2D) -> void:
	if body.name == "player":
		body.take_damage(30 )
		queue_free()  # Remove obstacle on collision
