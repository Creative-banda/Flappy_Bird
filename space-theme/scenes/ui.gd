extends CanvasLayer

@onready var health: Label = $Health
@onready var bullets: Label = $Bullets
@onready var score_label: Label = $Score

func update_health(hp: int) -> void:
	health.text = "Health: %d" % hp

func update_score(score: int) -> void:
	score_label.text = "Score: %d" % score

func update_bullet_count(bullet_count: int) -> void:
	bullets.text = "Bullets: %d" % bullet_count

func disable_ui() -> void:
	visible = false

func enable_ui() -> void:
	visible = true
