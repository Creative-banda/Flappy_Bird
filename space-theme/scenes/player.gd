extends CharacterBody2D

const UDP_PORT = 5005
const LERP_SPEED = 10.0  # How smoothly the player moves to target position
@onready var timer: Timer = $Timer

var udp := PacketPeerUDP.new()
var target_position_percent := 50.0  # Default to middle of screen
var screen_height := 0.0

@export var bullet_scene: PackedScene
@onready var shoot_position: Marker2D = $Shoot_Position

var is_player_shooting := false
var is_shooting := false
var last_is_shooting := false  # Track the last shooting state
func _ready():
	var err = udp.bind(UDP_PORT, "127.0.0.1")
	if err != OK:
		print("ERROR: Could not bind UDP socket on port ", UDP_PORT)
	else:
		print("SUCCESS: Listening for UDP packets on port ", UDP_PORT)
	
	# Get the screen height
	screen_height = get_viewport_rect().size.y

func _physics_process(delta):
	# Poll for incoming UDP data
	read_udp_input()
	
	# Calculate target Y position based on percentage (0% = top, 100% = bottom)
	var target_y = (target_position_percent / 100.0) * screen_height
	
	# Smoothly move player to target position
	position.y = lerp(position.y, target_y, LERP_SPEED * delta)
	
	# Optional: Keep player within screen bounds
	position.y = clamp(position.y, 0, screen_height)
	
	# Continuously check shooting state (even when no new data arrives)
	if is_shooting and not is_player_shooting:
		shoot()
		is_player_shooting = true  # Set to true to prevent rapid firing
		# Optional: Add a cooldown to prevent spamming using the timer
		timer.start()

func read_udp_input():  
	while udp.get_available_packet_count() > 0:
		var packet = udp.get_packet().get_string_from_utf8()		
		# Parse JSON data from Python
		if packet.begins_with("{"):
			var json = JSON.new()
			var parse_result = json.parse(packet)
			
			if parse_result == OK:
				var data = json.data
				
				# Handle vertical_position (0-100%)
				if data.has("vertical_position"):
					target_position_percent = clamp(data["vertical_position"], 0.0, 100.0)
				
				# Handle is_shooting - update the state when data arrives
				if data.has("is_shooting"):
					is_shooting = data["is_shooting"]
			else:
				print("ERROR: Failed to parse JSON: ", packet)

func shoot():
	if Globals.bullet_count <= 0:
		return  # No bullets left
	# Instance a bullet and add it to the scene
	var bullet_instance = bullet_scene.instantiate()
	bullet_instance.position = shoot_position.global_position
	get_parent().add_child(bullet_instance)
	AudioManager.play_sound("shoot")
	Globals.update_bullet_count(-1)


func take_damage(amount: int) -> void:
	if Globals.health <= 0:
		return  # Already dead
	Globals.update_health(-amount)
	if Globals.health <= 0:
		$player_animation.play("blast")
		AudioManager.play_sound("ship_blast")
		AudioManager.stop_music()

func _on_timer_timeout() -> void:
	is_player_shooting = false

func _on_player_animation_animation_finished() -> void:
	if $player_animation.animation == "blast":
		queue_free()  # Remove player from scene on blast animation finish
		Globals.game_over()

