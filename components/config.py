from components.init import *
from components.functions import *
from components.Cubes import *
from components.Textbox import Textbox

enemies = []
breakFront = []
projectiles = []
explosions = []
transform = []
cubes = []
frontcubes = []
config.player = None
hint_update_queue_monkey = []
hint_update_queue_fox = []
hint_update_queue_bear = []
hint_update_queue_WIFEFANCY = []
hint_update_queue = []
textboxWIFE_update_queue = []
textbox_update_queue = []
breakCubes = []
npc_final_scene = []
npc_final_scene_front = []

bear_unlocked = False
rabbit_unlocked = True
monkey_unlocked = False
fox_unlocked = False
fancy_rabbit_unlocked = True
background_layers = None

config.player = None
talked_to_wife = False
showTextBox = False
showTextBoxWIFE = False
showTextBoxMONKEY = False
showTextBoxFOX = False
showTextBoxWIFEFANCY = False
showTextBoxBEAR = False

showTextBox = False
showTextBoxWIFE = False

wife = None
textboxWIFE_update_queue = []
textboxMONKEY_update_queue = []
textboxFOX_update_queue = []
textboxBEAR_update_queue = []
textboxWIFEFANCY_update_queue = []
textbox_update_queue = []
falling_block = None
stage = 1

debug = False
fast_start = False

leap_of_faith_triggered = False
screen_width = 1920
screen_height = 1080
camera_x, camera_y, camera_z = 0, 0, -3
camera_smoothness = 0.1
spawn_clouds = False
zoom_generator = None

fov = 50
near_clip = 0.1
far_clip = 1000.0
npc_idle_sprites = load_sprites("assets/npc_idle")
fox_idle_sprites = load_sprites("assets/animals/fox/fox_idle")
bear_idle_sprites = load_sprites("assets/animals/bear/bear_idle")
monkey_idle_sprites = load_sprites("assets/animals/monkey/monkey_idle")
monkey_run_sprites = load_sprites("assets/animals/monkey/monkey_run")

npc_idle_sprites = load_sprites("assets/npc_idle")
wife_fancy_idle_sprites = load_sprites("assets/animals/wife")
textbox = Textbox("Hello!jjjjj", 5, 1, "assets/font.otf", 100)
textboxWIFE = Textbox("Wife",2,1, "assets/font.otf", 100)
textboxMONKEY = Textbox("Monkey",2,1, "assets/font.otf", 100)
textboxFOX = Textbox("FOX",2,1, "assets/font.otf", 100)
textboxBEAR = Textbox("ber",2,1, "assets/font.otf", 100)
textboxWIFEFANCY = Textbox("<3",1,1, "assets/font.otf", 100)
background_scroll_speed = 0.001
background_width = 50
background_height = 28 
background_offset_x = 0  


logo_animation_time = 0
logo_amplitude = 0.3
logo_frequency = 10 

fade_width = 3 
fade_height = 2  
fade_speed = 1


claw_sound = pygame.mixer.Sound("assets/sounds/claw_sound.mp3")
poof_sound = pygame.mixer.Sound("assets/sounds/poof.mp3")
gun_sound = pygame.mixer.Sound("assets/sounds/gun.mp3")

black_texture = {
    "front": load_texture("assets/black.png"),
    "left": load_texture("assets/black.png"),
    "right": load_texture("assets/black.png"),
    "top": load_texture("assets/black.png"),
    "bottom": load_texture("assets/black.png")
}

iron_bars_texture = {
    "front": load_texture("assets/ironbars.png"),
    "left": load_texture("assets/ironbars.png"),
    "right": load_texture("assets/ironbars.png"),
    "top": load_texture("assets/empty.png"),
    "bottom": load_texture("assets/empty.png")
}
floor_texture = {
    "front": load_texture("assets/brick_floor.png"),
    "left": load_texture("assets/brick_floor.png"),
    "right": load_texture("assets/brick_floor.png"),
    "top": load_texture("assets/brick_floor.png"),
    "bottom": load_texture("assets/brick_floor.png")
}

brick_texture = {
    "front": load_texture("assets/brick.png"),
    "left": load_texture("assets/brick.png"),
    "right": load_texture("assets/brick.png"),
    "top": load_texture("assets/brick.png"),
    "bottom": load_texture("assets/brick.png")
}

carpet_texture = {
    "front": load_texture("assets/carpet.png"),
    "left": load_texture("assets/carpet.png"),
    "right": load_texture("assets/carpet.png"),
    "top": load_texture("assets/carpet.png"),
    "bottom": load_texture("assets/carpet.png")
}

grass_texture = {
    "front": load_texture("assets/front.png"),
    "left": load_texture("assets/front.png"),
    "right": load_texture("assets/front.png"),
    "top": load_texture("assets/top.png"),
    "bottom": load_texture("assets/bottom.png")
}

dirt_texture = {
    "front": load_texture("assets/bottom.png"),
    "left": load_texture("assets/bottom.png"),
    "right": load_texture("assets/bottom.png"),
    "top": load_texture("assets/bottom.png"),
    "bottom": load_texture("assets/bottom.png")
}

gravel_texture = {
    "front": load_texture("assets/gravel.png"),
    "left": load_texture("assets/gravel.png"),
    "right": load_texture("assets/gravel.png"),
    "top": load_texture("assets/gravel.png"),
    "bottom": load_texture("assets/gravel.png")
}

empty_texture = {
    "front": load_texture("assets/empty.png"),
    "left": load_texture("assets/empty.png"),
    "right": load_texture("assets/empty.png"),
    "top": load_texture("assets/empty.png"),
    "bottom": load_texture("assets/empty.png")
}

bark_texture = {
    "front": load_texture("assets/bark_side.png"),
    "left": load_texture("assets/bark_side.png"),
    "right": load_texture("assets/bark_side.png"),
    "top": load_texture("assets/bark_top.png"),
    "bottom": load_texture("assets/bark_top.png")
}

leaves_texture = {
    "front": load_texture("assets/leaves.png"),
    "left": load_texture("assets/leaves.png"),
    "right": load_texture("assets/leaves.png"),
    "top": load_texture("assets/leaves.png"),
    "bottom": load_texture("assets/leaves.png")
}

special_cube_texture = {
    "front": load_texture("assets/special.png"),
    "left": load_texture("assets/special.png"),
    "right": load_texture("assets/special.png"),
    "top": load_texture("assets/special.png"),
    "bottom": load_texture("assets/special.png")
}

water_texture = {
    "front": load_texture("assets/water.png"),
    "left": load_texture("assets/water.png"),
    "right": load_texture("assets/water.png"),
    "top": load_texture("assets/water.png"),
    "bottom": load_texture("assets/water.png")
}

wood_texture = {
    "front": load_texture("assets/wood.png"),
    "left": load_texture("assets/wood.png"),
    "right": load_texture("assets/wood.png"),
    "top": load_texture("assets/wood.png"),
    "bottom": load_texture("assets/wood.png")
}
snow_texture = {
    "front": load_texture("assets/snow.png"),
    "left": load_texture("assets/snow.png"),
    "right": load_texture("assets/snow.png"),
    "top": load_texture("assets/snow.png"),
    "bottom": load_texture("assets/snow.png")
}
glass_texture = {
    "front": load_texture("assets/glass.png"),
    "left": load_texture("assets/glass.png"),
    "right": load_texture("assets/glass.png"),
    "top": load_texture("assets/glass.png"),
    "bottom": load_texture("assets/glass.png")
}
flower_texture = {
    "front": load_texture("assets/flower.png"),
    "left": load_texture("assets/empty.png"),
    "right": load_texture("assets/empty.png"),
    "top": load_texture("assets/empty.png"),
    "bottom": load_texture("assets/empty.png")
}
cloud_texture = {
    "front": load_texture("assets/cloud.png"), 
    "left": load_texture("assets/empty.png"),
    "right": load_texture("assets/empty.png"), 
    "top": load_texture("assets/empty.png"),
    "bottom": load_texture("assets/empty.png")  
}

idle_sprites = load_sprites("assets/idle")
run_sprites = load_sprites("assets/run")
jump_sprites = load_sprites("assets/jump")


weapon_idle_sprites = load_sprites("assets/weapon_idle")
weapon_run_sprites = load_sprites("assets/weapon_run")
weapon_jump_sprites = load_sprites("assets/weapon_jump")
weapon_shoot_sprites = load_sprites("assets/weapon_shoot")
projectile_sprite = load_texture("assets/banana.png")


explosion_sprites = load_sprites("assets/cube_explosion")

transform_sprites = load_sprites("assets/character_smoke")

idle_fox = load_sprites("assets/animals/fox/fox_idle")
run_fox = load_sprites("assets/animals/fox/fox_run")


animal_sprites = {
    "bear": {
        "attack": load_sprites("assets/animals/bear/bear_idle"),
        "idle": load_sprites("assets/animals/bear/bear_idle"),
        "run": load_sprites("assets/animals/bear/bear_run"),
        "jump": load_sprites("assets/animals/bear/bear_jump")
    },
    "rabbit": {
        "idle": load_sprites("assets/animals/rabbit/rabbit_idle"),
        "run": load_sprites("assets/animals/rabbit/rabbit_run"),
        "jump": load_sprites("assets/animals/rabbit/rabbit_jump")
    },
    "monkey": {
        "idle": load_sprites("assets/animals/monkey/monkey_idle"),
        "run": load_sprites("assets/animals/monkey/monkey_run"), 
        "jump": load_sprites("assets/animals/monkey/monkey_jump")
    },
    "fox": {
        "idle": load_sprites("assets/animals/fox/fox_idle"),
        "run": load_sprites("assets/animals/fox/fox_run"),
        "jump": load_sprites("assets/animals/fox/fox_jump")
    },
    "fancy_rabbit":{
        "idle": load_sprites("assets/animals/fancy_rabbit/fancy_rabbit_idle"),
        "run": load_sprites("assets/animals/fancy_rabbit/fancy_rabbit_run"),
        "jump": load_sprites("assets/animals/fancy_rabbit/fancy_rabbit_jump")
    },
    "man1":{
        "idle": load_sprites("assets/enemy/man1/idle"),
        "run": load_sprites("assets/enemy/man1/run")
    },
    "man2":{
        "idle": load_sprites("assets/enemy/man2/idle"),
        "run": load_sprites("assets/enemy/man2/run")
    }
}

claw_sprites = load_sprites("assets/claw")
idle_sprites = load_sprites("assets/idle")
run_sprites = load_sprites("assets/run")
jump_sprites = load_sprites("assets/jump")

