extends Node

@onready var background_music: AudioStreamPlayer2D = $background_music
@onready var hit: AudioStreamPlayer2D = $hit
@onready var shoot: AudioStreamPlayer2D = $shoot
@onready var ship_blast: AudioStreamPlayer2D = $ship_blast
@onready var rock_smash: AudioStreamPlayer2D = $rock_smash
@onready var collect: AudioStreamPlayer2D = $collect
@onready var main_menu: AudioStreamPlayer2D = $main_menu

func _ready():
	print("AudioManager initialized.")


# Play sound based on the player name
func play_sound(sound_name: String):
	match sound_name:
		"background_music":
			main_menu.stop()
			background_music.play()
		"hit":
			hit.play()
		"shoot":
			shoot.play()
		"ship_blast":
			ship_blast.play()
		"rock_smash":
			rock_smash.play()
		"collect":
			collect.play()
		"main_menu":
			main_menu.play()
		_:
			print("⚠️ Sound not found: ", sound_name)


func stop_music():
	background_music.stop()

func stop_all():
	background_music.stop()
	hit.stop()
	shoot.stop()
