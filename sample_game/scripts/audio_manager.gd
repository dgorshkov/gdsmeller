extends Node

# Audio Manager Singleton
# Handles all game audio including music and sound effects

@onready var music_player: AudioStreamPlayer = $MusicPlayer
@onready var sfx_pool: Array[AudioStreamPlayer] = []

var music_volume := 1.0
var sfx_volume := 1.0
var is_music_muted := false
var is_sfx_muted := false

const SFX_POOL_SIZE = 8
const SOUNDS = {
	"shoot": preload("res://audio/shoot.ogg"),
	"explosion": preload("res://audio/explosion.ogg"),
	"powerup": preload("res://audio/powerup.ogg"),
	"hit": preload("res://audio/hit.ogg"),
}

# Initialize audio manager
func _ready() -> void:
	_create_sfx_pool()

# Create a pool of audio players for sound effects
func _create_sfx_pool() -> void:
	for i in range(SFX_POOL_SIZE):
		var player = AudioStreamPlayer.new()
		player.bus = "SFX"
		add_child(player)
		sfx_pool.append(player)

# Play a sound effect by name
func play_sfx(sound_name: String) -> void:
	if is_sfx_muted:
		return
	
	if not SOUNDS.has(sound_name):
		push_warning("Sound not found: " + sound_name)
		return
	
	var player = _get_available_sfx_player()
	if player:
		player.stream = SOUNDS[sound_name]
		player.volume_db = linear_to_db(sfx_volume)
		player.play()

# Get an available sound effect player from the pool
func _get_available_sfx_player() -> AudioStreamPlayer:
	for player in sfx_pool:
		if not player.playing:
			return player
	# All players busy, return the first one (will cut off)
	return sfx_pool[0]

# Play background music
func play_music(music_stream: AudioStream, fade_time: float = 1.0) -> void:
	if is_music_muted:
		return
	
	if music_player.playing:
		_crossfade_music(music_stream, fade_time)
	else:
		music_player.stream = music_stream
		music_player.volume_db = linear_to_db(music_volume)
		music_player.play()

# Crossfade between tracks
func _crossfade_music(new_track: AudioStream, fade_time: float) -> void:
	var tween = create_tween()
	tween.tween_property(music_player, "volume_db", -80, fade_time)
	tween.tween_callback(func():
		music_player.stream = new_track
		music_player.volume_db = linear_to_db(music_volume)
		music_player.play()
	)

# Stop music with optional fade out
func stop_music(fade_time: float = 0.5) -> void:
	if fade_time > 0:
		var tween = create_tween()
		tween.tween_property(music_player, "volume_db", -80, fade_time)
		tween.tween_callback(music_player.stop)
	else:
		music_player.stop()

# Set music volume (0.0 to 1.0)
func set_music_volume(volume: float) -> void:
	music_volume = clamp(volume, 0.0, 1.0)
	if music_player.playing:
		music_player.volume_db = linear_to_db(music_volume)

# Set sound effects volume (0.0 to 1.0)
func set_sfx_volume(volume: float) -> void:
	sfx_volume = clamp(volume, 0.0, 1.0)

# Toggle music mute
func toggle_music_mute() -> void:
	is_music_muted = not is_music_muted
	if is_music_muted:
		music_player.stop()

# Toggle sound effects mute
func toggle_sfx_mute() -> void:
	is_sfx_muted = not is_sfx_muted
