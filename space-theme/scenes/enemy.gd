extends CharacterBody2D

var is_Colliding_with_player := false

var bullet_scene: PackedScene = preload("res://scenes/bullet.tscn")
@onready var shoot_position: Marker2D = $Shoot_Position
@onready var shoot_timer: Timer = $Timer  # Reference to the timer
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
var is_Shooting := false

var health := 100


func _process(delta: float) -> void:	
	# move enemy leftwards
	position.x -= 150 * delta * Globals.game_speed  # Adjust speed as needed

	if is_Colliding_with_player and not is_Shooting:
		shoot()
	
	if position.x < -100:
		queue_free()  # Remove enemy if it goes off-screen

func shoot() -> void:
	is_Shooting = true
	var bullet = bullet_scene.instantiate()
	bullet.direction = -1  # Move left towards player
	bullet.speed = 400
	bullet.position = shoot_position.global_position
	get_parent().add_child(bullet)
	shoot_timer.start()  # Start the timer to reset is_Shooting after cooldown
	AudioManager.play_sound("shoot")

func _on_area_2d_body_entered(body:Node2D) -> void:
	if body.is_in_group("player"):
		is_Colliding_with_player = true

func _on_area_2d_body_exited(body:Node2D) -> void:
	if body.is_in_group("player"):
		is_Colliding_with_player = false


func _on_timer_timeout() -> void:
	is_Shooting = false

func take_damage() -> void:
	if health <= 0:
		return  # Already dead
	health -= 40
	if health <= 0:
		animated_sprite.play("enemy_1_die")
		AudioManager.play_sound("ship_blast")
		$AnimatedSprite2D2.visible = false


func _on_animated_sprite_2d_animation_finished() -> void:
	if animated_sprite.animation == "enemy_1_die":
		queue_free()  # Remove enemy after explosion animation finishes


func _on_area_2d_2_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.hit_by_obstacle()
		queue_free()
