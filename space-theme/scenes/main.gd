extends Node2D

# Export variable for obstical scene
@export var obstical_scene: PackedScene
@export var enemy_scene: PackedScene
@export var ui_manager: CanvasLayer
@export var item_scene: PackedScene

var screen_width: int
var screen_height: int
@onready var background_1: TextureRect = $Background
@onready var background_2: TextureRect = $Background2
 
func _ready() -> void:
	UI.enable_ui()
	# Get screen dimensions
	var viewport_rect = get_viewport_rect()
	screen_width = viewport_rect.size.x
	screen_height = viewport_rect.size.y
	
	# Initialize background positions
	# Background 1 starts at x=0
	background_1.position.x = 0
	# Background 2 starts right after background 1
	var bg_width = background_1.size.x * background_1.scale.x
	background_2.position.x = bg_width
	AudioManager.play_sound("background_music")

	Globals.update_health(100 - 100)
	Globals.update_bullet_count(50 - 50)
	Globals.update_score(0)
	Globals.game_speed = 1.0

func _process(_delta: float) -> void: 
	# Add parallax effect to backgrounds
	add_parallax_effect(1.0)
	
	# Spawn obstical on a random interval using random.randi
	if randi() % int(100 / Globals.game_speed) < 1:  # Spawn rate increases as game speed increases
		var obstical_instance = obstical_scene.instantiate()
		obstical_instance.position = Vector2(screen_width, randf() * screen_height)
		get_parent().add_child(obstical_instance)

	# Spawn enemy on a random interval using random.randi
	if randi() % int(150 / Globals.game_speed) < 1:  # Spawn rate decreases as game speed increases
		var enemy_instance = enemy_scene.instantiate()
		enemy_instance.position = Vector2(screen_width, randf() * screen_height)
		# Scale the enemy between 1.5 to 2.5 times its original size
		var scale_factor = randf() * 0.4 + 0.5
		enemy_instance.scale = Vector2(scale_factor, scale_factor)
		get_parent().add_child(enemy_instance)
	
	# Increase game speed over time for difficulty scaling
	Globals.game_speed += 0.001

	# Spawn item on a random interval using random.randi
	# Appears roughly once every 15-20 seconds (assuming 60 FPS)
	if randi() % 1200 < 1:  # ~0.083% chance each frame
		var item_instance = item_scene.instantiate()
		item_instance.position = Vector2(screen_width, randf() * screen_height)
		get_parent().add_child(item_instance)


func add_parallax_effect(speed: float) -> void:
	# Move backgrounds leftwards for parallax effect
	background_1.position.x -= speed * Globals.game_speed
	background_2.position.x -= speed * Globals.game_speed
	
	# Get the width of the backgrounds
	var bg_width = background_1.size.x * background_1.scale.x
	
	# Reset position when background moves completely off-screen to the left
	if background_1.position.x + bg_width <= 0:
		background_1.position.x = background_2.position.x + bg_width
	
	if background_2.position.x + bg_width <= 0:
		background_2.position.x = background_1.position.x + bg_width


func update_score(amount: int) -> void:
	ui_manager.update_score(amount)

func update_health(amount: int) -> void:
	ui_manager.update_health(amount)

func update_bullet_count(amount: int) -> void:
	ui_manager.update_bullet_count(amount)
