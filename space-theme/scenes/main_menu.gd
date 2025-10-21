extends Control

var screen_width: int
var screen_height: int
@onready var background_1: TextureRect = $Background
@onready var background_2: TextureRect = $Background2
 
func _ready() -> void:
	UI.disable_ui()
	# Get screen dimensions
	var viewport_rect = get_viewport_rect()
	screen_width = viewport_rect.size.x
	screen_height = viewport_rect.size.y
	Globals.game_speed = 1.0
	
	# Initialize background positions
	# Background 1 starts at x=0
	background_1.position.x = 0
	# Background 2 starts right after background 1
	var bg_width = background_1.size.x * background_1.scale.x
	background_2.position.x = bg_width
	AudioManager.play_sound("main_menu")


func _process(_delta: float) -> void: 
	# Add parallax effect to backgrounds
	add_parallax_effect(1.0)

func add_parallax_effect(speed: float) -> void:
	# Move backgrounds leftwards for parallax effect
	background_1.position.x -= speed * Globals.game_speed 
	background_2.position.x -= speed * Globals.game_speed
	
	# Reset position when background moves completely off-screen to the left
	if background_1.position.x + background_1.size.x * background_1.scale.x <= 0:
		background_1.position.x = background_2.position.x + background_1.size.x * background_1.scale.x

	if background_2.position.x + background_2.size.x * background_2.scale.x <= 0:
		background_2.position.x = background_1.position.x + background_2.size.x * background_2.scale.x


func _on_play_pressed() -> void:
	# Change to main game scene
	get_tree().change_scene_to_file("res://scenes/main.tscn")


func _on_quit_pressed() -> void:
	# Quit the game
	get_tree().quit()
