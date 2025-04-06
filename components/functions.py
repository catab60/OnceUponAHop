from components.init import *
from components.utils import load_texture
from components.Player import Projectile, Enemy
from components.Cubes import Cube, SpecialKeyCube
from components.NPC import NPC
from components.Textbox import Textbox
import components.config as config
import json
import random
import time


def load_sprites(folder_path):
    sprites = []
    for file in sorted(os.listdir(folder_path)):
        sprite = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
        sprites.append(sprite)
    return sprites

def drawTransparentSprite(t, i):
    """
    Renders a transparent quad with the given texture and image information.
    :param t: TextureInformation containing textureID, target, x, y, w, h
    :param i: ImageInformation containing x, y, w, h, alpha
    """
    # Enable blending and set blending function
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_COLOR_MATERIAL)

    # Set the color with alpha transparency
    glColor4f(1.0, 1.0, 1.0, i.alpha)

    # Bind the texture
    glBindTexture(t.target, t.textureID)

    # Draw the quad
    glBegin(GL_QUADS)
    glTexCoord2d(t.x, t.y)
    glVertex3d(i.x, i.y, 0)
    glTexCoord2d(t.x, t.y + t.h)
    glVertex3d(i.x, i.y + i.h, 0)
    glTexCoord2d(t.x + t.w, t.y + t.h)
    glVertex3d(i.x + i.w, i.y + i.h, 0)
    glTexCoord2d(t.x + t.w, t.y)
    glVertex3d(i.x + i.w, i.y, 0)
    glEnd()

    # Disable blending after rendering
    glDisable(GL_BLEND)

# Smooth zoom function
def smooth_zoom(target_fov, duration):
    import components.config as config
    start_fov = config.fov
    steps = int(duration * 60)  
    for i in range(steps):
        t = i / steps  
        eased_t = t * t * (3 - 2 * t)  
        config.fov = start_fov + (target_fov - start_fov) * eased_t
        yield  

def spawn_projectile(player):
    if len(config.projectiles) < 5:
        # Create a larger projectile - size 0.8 is 4x the original size
        projectile_size = 0.8
        
        offset_x = 0.5 if player.direction > 0 else -0.5  
        new_projectile = Projectile(
            x=player.x + offset_x,  
            y=player.y + (player.height * 0.3),  # Position at 50% of player height
            z=player.z,
            direction=player.direction,  
            speed=0.2,
            size=projectile_size,  # Pass the size parameter explicitly
            facing_right=(player.direction > 0)  
        )
        config.projectiles.append(new_projectile)

def JsonLoadData(map_file, cubes, collide=True):
    with open(map_file, "r") as file:
        cube_data = json.load(file)
    for data in cube_data:
        # Determine if the cube should be collidable based on its z value
        is_collidable = collide and float(data["z"]) >= -4.5

        if data["texture_id"] == "1":
            cubes.append(Cube(
            data["x"],
            data["y"],
            float(data["z"]),  # Convert z to float since it's a string in the JSON
            data["width"],
            data["height"],
            10,  # Assuming depth is always 1
            config.grass_texture,
            collidable=is_collidable,  # Set collidable based on the condition
            debug=True  # Enable debug mode for hitboxes
        )) 

         # Select texture based on texture_id
        elif data["texture_id"] == "2":
            cubes.append(Cube(
            data["x"],
            data["y"]+1,
            float(data["z"]),  # Convert z to float since it's a string in the JSON
            data["width"],
            -10,
            1,  # Assuming depth is always 1
            config.dirt_texture,
            collidable=is_collidable,  # Set collidable based on the condition
            debug=True  # Enable debug mode for hitboxes
        ))
            
def get_background_layers():
    """
    Returns the appropriate background layers based on the current game stage.
    """
    if config.stage == 1:
        return [
            #{"texture": load_texture("assets/Clouds/Clouds1/1.png"), "speed": 0.2, "left": 10, "right": 10, "offset_x": 0, "offset_y": 10, "width": 100},
            {"texture": load_texture("assets/forestt/1.png"), "speed": 0.1, "left": 10, "right": 10, "offset_x": 0, "offset_y": 6, "width": 50},
            {"texture": load_texture("assets/forestt/4.png"), "speed": 0.3, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4, "width": 10},
            {"texture": load_texture("assets/forestt/2.png"), "speed": 0.1, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4, "width": 10},
            {"texture": load_texture("assets/forestt/3.png"), "speed": 0.2, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4, "width": 10},
            {"texture": load_texture("assets/forestt/5.png"), "speed": 0.4, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4, "width": 10},
            {"texture": load_texture("assets/forestt/6.png"), "speed": 0.4, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4, "width": 10},
            {"texture": load_texture("assets/forestt/8.png"), "speed": 0.5, "left": 10, "right": 10, "offset_x": 0, "offset_y": 8, "width": 10},
        ]
    elif config.stage == 2:
        return [
            {"texture": load_texture("assets/Clouds/Clouds1/1.png"), "speed": 0.2, "left": 10, "right": 10, "offset_x": 0, "offset_y": 10, "width": 100},  
            {"texture": load_texture("assets/Clouds/Clouds1/2.png"), "speed": 0.3, "left": 10, "right": 10, "offset_x": 0, "offset_y": 7, "width": 10},
            {"texture": load_texture("assets/Clouds/Clouds1/3.png"), "speed": 0.4, "left": 10, "right": 10, "offset_x": 0, "offset_y": 7, "width": 10},  
            {"texture": load_texture("assets/Clouds/Clouds1/4.png"), "speed": 0.5, "left": 10, "right": 10, "offset_x": 0, "offset_y": 7, "width": 10},
        ]
    elif config.stage == 3:
        return [
            {"texture": load_texture("assets/Clouds/Clouds5/1.png"), "speed": 0.2, "left": 10, "right": 10, "offset_x": 0, "offset_y": 10, "width": 100},
            {"texture": load_texture("assets/Clouds/Clouds5/2.png"), "speed": 0.3, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4.3, "width": 10},
            {"texture": load_texture("assets/Clouds/Clouds5/3.png"), "speed": 0.4, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4.3, "width": 10},
            {"texture": load_texture("assets/Clouds/Clouds5/4.png"), "speed": 0.5, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4.3, "width": 10},
            {"texture": load_texture("assets/Clouds/Clouds5/5.png"), "speed": 0.6, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4.3, "width": 10}
        ]
    elif config.stage == 4:
        return [
            {"texture": load_texture("assets/Clouds/Clouds2/1.png"), "speed": 0.2, "left": 10, "right": 10, "offset_x": 0, "offset_y": 10, "width": 100},
            {"texture": load_texture("assets/Clouds/Clouds2/2.png"), "speed": 0.3, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4.3, "width": 10},
            {"texture": load_texture("assets/Clouds/Clouds2/3.png"), "speed": 0.4, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4.3, "width": 10},
            {"texture": load_texture("assets/Clouds/Clouds2/4.png"), "speed": 0.5, "left": 10, "right": 10, "offset_x": 0, "offset_y": 4.3, "width": 10}
        ]


def loadStage2Parkour(map_file, cubes, collide=True):
    with open(map_file, "r") as file:
        cube_data = json.load(file)

    for data in cube_data:
        # Determine if the cube should be collidable based on its z value
        is_collidable = collide and float(data["z"]) >= -4.5

        if data["texture_id"] == "4":
            cubes.append(Cube(
            data["x"],
            data["y"],
            float(data["z"]),  # Convert z to float since it's a string in the JSON
            data["width"],
            data["height"],
            1,  # Assuming depth is always 1
            config.cloud_texture,
            collidable=is_collidable,  # Set collidable based on the condition
            debug=True  # Enable debug mode for hitboxes
        )) 

def spawning_clouds():
    """
    Handles the leap of faith interaction and tracks if it has been triggered.
    """
    if not config.spawn_clouds:
        config.spawn_clouds = True
        # Call the original textbox_cube function
        textbox_cube(
            first="This sucks!", 
            second="I want to go home!", 
            first_scale=1, 
            second_scale=1
        )
def add_tree(x,y,z, option=0):
    if option == 0:
        config.cubes.append(Cube(0+x, 0+y, 0+z, 1, 4, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(-2+x, 3+y, 1+z, 5, 2, 3, config.leaves_texture, collidable=False))
        config.cubes.append(Cube(-1+x, 3+y, 2+z, 3, 2, 5, config.leaves_texture, collidable=False))
        config.cubes.append(Cube(-1+x, 5+y, 1+z, 3, 2, 3, config.leaves_texture, collidable=False))
    else:
        config.frontcubes.append(Cube(0+x, 0+y, 0+z, 1, 4, 1, config.bark_texture, collidable=False))
        config.frontcubes.append(Cube(-2+x, 3+y, 1+z, 5, 2, 3, config.leaves_texture, collidable=False))
        config.frontcubes.append(Cube(-1+x, 3+y, 2+z, 3, 2, 5, config.leaves_texture, collidable=False))
        config.frontcubes.append(Cube(-1+x, 5+y, 1+z, 3, 2, 3, config.leaves_texture, collidable=False))

def add_ball(x,y,z, l, option=0, collidable=False, lenght=0):
    if option == 0:
        config.cubes.append(Cube(1+x, 5+y, -6.5+z, 3+l, 1, 3+lenght, config.grass_texture, collidable=collidable))
        config.cubes.append(Cube(0+x, 4+y, -6.5+z, 5+l, 1, 3+lenght, config.grass_texture, collidable=collidable))
        config.cubes.append(Cube(1+x, 4+y, -5.5+z, 3+l, 1, 5+lenght, config.grass_texture, collidable=collidable))
        config.cubes.append(Cube(0+x, 2+y, -6.5+z, 5+l, 2, 3+lenght, config.dirt_texture, collidable=collidable))
        config.cubes.append(Cube(1+x, 2+y, -5.5+z, 3+l, 2, 5+lenght, config.dirt_texture, collidable=collidable))
        config.cubes.append(Cube(1+x, 1+y, -6.5+z, 3+l, 1, 3+lenght, config.dirt_texture, collidable=collidable))
    else:
        config.frontcubes.append(Cube(1+x, 5+y, -6.5+z, 3+l, 1, 3+lenght, config.grass_texture, collidable=collidable))
        config.frontcubes.append(Cube(0+x, 4+y, -6.5+z, 5+l, 1, 3+lenght, config.grass_texture, collidable=collidable))
        config.frontcubes.append(Cube(1+x, 4+y, -5.5+z, 3+l, 1, 5+lenght, config.grass_texture, collidable=collidable))
        config.frontcubes.append(Cube(0+x, 2+y, -6.5+z, 5+l, 2, 3+lenght, config.dirt_texture, collidable=collidable))
        config.frontcubes.append(Cube(1+x, 2+y, -5.5+z, 3+l, 2, 5+lenght, config.dirt_texture, collidable=collidable))
        config.frontcubes.append(Cube(1+x, 1+y, -6.5+z, 3+l, 1, 3+lenght, config.dirt_texture, collidable=collidable))

def reset_tutorial(player):
    
    player.x = 20
    player.y = 1
    config.zoom_generator = smooth_zoom(60,1.0)

def first_tutorial_cube():
    def sub_process():
        config.textbox_update_queue
        config.showTextBox
        config.zoom_generator
        time.sleep(2)
        config.textbox_update_queue.append(("Finish this course to\ncomplete the tutorial!", 8, 1))
        time.sleep(4)
        config.showTextBox = False
        config.zoom_generator = smooth_zoom(60, 1.0)  

    config.showTextBox
    config.zoom_generator
    config.showTextBox = True
    config.zoom_generator = smooth_zoom(40, 1.0)
    config.textbox_update_queue.append(("Let's Learn", 4, 1))  
    threading.Thread(target=sub_process).start()

def cut_scene_enter():
    config.zoom_generator
    config.zoom_generator = smooth_zoom(50, 2.0)

def get_captured():
    def sub_processkkk():
        """
        Simulate a shaking effect, reposition the player, and delay the falling block animation.
        """
       
        config.zoom_generator = smooth_zoom(30, 1.0)
        
        delay_frames = 160  
        for frame in range(180):  
            shake_intensity = 0.1
            config.camera_x += random.uniform(-shake_intensity, shake_intensity)
            config.camera_y += random.uniform(-shake_intensity, shake_intensity)

            if frame >= delay_frames:
                config.falling_block.y = 10 - (7 * ((frame - delay_frames) / (180 - delay_frames)))  # Linear interpolation from 10 to 3

            config.player.x = 52.2
            config.player.y = 3

            time.sleep(1 / 60) 
        pygame.mixer.music.stop()
        music_path = os.path.join("assets", "sounds", "captureboom.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed
            pygame.mixer.music.play()
        config.frontcubes.append(Cube(-100, -100, 2.5, 1000, 1000, 1, config.black_texture, collidable=False, id="blackscreen"))
        
        config.player.x = 1
        config.player.y = 1
        
        time.sleep(3)
        config.zoom_generator = smooth_zoom(50, 1.0)
        config.frontcubes = [cube for cube in config.frontcubes if cube.id != "blackscreen"]

        config.stage = 2
        config.cubes = []
        config.frontcubes = []
        config.breakCubes = []
        config.breakFront = []
        config.background_layers = get_background_layers()
        stageload(config.player)

    if config.talked_to_wife:

        config.zoom_generator = smooth_zoom(50, 1.0)
        threading.Thread(target=sub_processkkk).start()

def talk_to_wife():
    def sub_process():
        config.textboxWIFE_update_queue
        config.showTextBoxWIFE
        config.talked_to_wife
        time.sleep(2)
        config.showTextBoxWIFE = False
        config.talked_to_wife = True
        config.hint_update_queue.append(("show", "assets/hint_e.png"))
    config.hint_update_queue
    config.showTextBoxWIFE
    config.wife.hide_hint()
    config.textboxWIFE_update_queue.append(("<3", 2, 1))
    config.showTextBoxWIFE = True
    threading.Thread(target=sub_process).start()

def push_config_to_player(actual_player):
    """
    Push the updated config.player data to the actual player object.
    """
    actual_player.x = config.player.x
    actual_player.y = config.player.y
    actual_player.z = config.player.z
    actual_player.direction = config.player.direction

def unlock_animal(animal_name):
    """Unlock a specific animal character."""
    if animal_name == "bear":
        config.bear_unlocked = True
        print("Bear character unlocked!")
    elif animal_name == "monkey":
        config.monkey_unlocked = True
        print("Monkey character unlocked!")
    elif animal_name == "fox":
        config.fox_unlocked = True
        print("Fox character unlocked!")
    

def caveMaker():
    # Use a distinctive texture for breakable cubes
    special_texture = config.special_cube_texture if hasattr(config, 'special_cube_texture') else config.grass_texture
    
    config.breakCubes.append(Cube(2, 1, -4.5, 1, 1, 1, special_texture, collidable=True))
    config.breakCubes.append(Cube(2, 2, -4.5, 1, 1, 1, special_texture, collidable=True))

    config.breakFront.append(Cube(3, 1, -3.5, 1, 1, 1, special_texture, collidable=True))
    config.breakFront.append(Cube(4, 1, -3.5, 1, 1, 1, special_texture, collidable=True))
    config.breakFront.append(Cube(5, 1, -3.5, 1, 1, 1, special_texture, collidable=True))
    config.breakFront.append(Cube(6, 1, -3.5, 1, 1, 1, special_texture, collidable=True))

    config.breakFront.append(Cube(3, 2, -3.5, 1, 1, 1, special_texture, collidable=True))
    config.breakFront.append(Cube(4, 2, -3.5, 1, 1, 1, special_texture, collidable=True))
    config.breakFront.append(Cube(5, 2, -3.5, 1, 1, 1, special_texture, collidable=True))
    config.breakFront.append(Cube(6, 2, -3.5, 1, 1, 1, special_texture, collidable=True))


def end_game():
    config.frontcubes.append(Cube(-100, -100, 2.5, 1000, 1000, 1, config.black_texture, collidable=False, id="blackscreen"))
    config.player.x = -1 
    config.player.y= 1
    def sub_process():
        config.player.change_character("fancy_rabbit")
        
        config.stage = 4
        config.cubes = []
        config.breakCubes = []
        config.breakFront = []
        time.sleep(1)
        stageload(config.player)
        time.sleep(2)
        config.frontcubes = [cube for cube in config.frontcubes if cube.id != "blackscreen"]
        

    threading.Thread(target=sub_process).start()

def leap_of_faith_interaction():
    """
    Handles the leap of faith interaction and tracks if it has been triggered.
    """
    if not config.leap_of_faith_triggered:
        config.leap_of_faith_triggered = True
        # Call the original textbox_cube function
        textbox_cube(
            first="A leap of faith!", 
            second="Got the courage?", 
            first_scale=1, 
            second_scale=1
        )

def textbox_cube(first, second, first_scale=1, second_scale=1):
    def sub_process():
        config.textbox_update_queue
        config.showTextBox
        config.zoom_generator
        time.sleep(2)
        config.textbox_update_queue.append((second, 8, second_scale))
        time.sleep(4)
        config.showTextBox = False
        config.zoom_generator = smooth_zoom(50, 1.0)  # Hide the textbox after the message

    config.showTextBox
    config.zoom_generator
    config.showTextBox = True
    config.zoom_generator = smooth_zoom(40, 1.0)
    config.textbox_update_queue.append((first, 4, first_scale))  # Add initial text update to the queue
    threading.Thread(target=sub_process).start()

def stageend(x):
    def transition_process():
        # Add black screen
        config.frontcubes.append(Cube(-100, -100, 2.5, 1000, 1000, 1, config.black_texture, collidable=False, id="blackscreen"))
        
        # Reset player position
        config.player.x = 1
        config.player.y = 1
        config.stage = 3
        
        # Wait for 3 seconds
        time.sleep(3)
        

        # Change zoom and clear objects
        config.zoom_generator = smooth_zoom(50, 1.0)
        config.cubes.clear()
        config.frontcubes = [cube for cube in config.frontcubes if cube.id != "blackscreen"]
        config.stage = 3
        stageload(config.player)
        config.background_layers = get_background_layers()
        
    
    # Run the transition in a separate thread
    threading.Thread(target=transition_process).start()

def stageload(player):
    config.cubes = []
    config.frontcubes = []
    config.breakCubes = []
    config.breakFront = []
    config.hint_update_queue = []
    config.hint_update_queue_monkey = []
    config.hint_update_queue_fox = []
    config.hint_update_queue_bear = []
    if config.stage == 1:    
        config.cubes.append(Cube(-500, -2, 50, 1000, 3, 65, config.grass_texture, collidable=True))
        add_ball(-15,-1,-1-.5,5)
        add_ball(-10,-3,0-.5, 4)
        add_ball(-6,-2,-2-.5,6)
        add_ball(4,-1,-1-.5,3)
        add_ball(8,-3,0-.5, 4)
        add_ball(16, -3, -3-.5, 5)

        add_tree(-11.5,2,-6.5)
        add_tree(-5,3,-7.5)
        add_tree(5,1,1.5, 1)

        config.cubes.append(Cube(4,1,-7,1,1,1, config.grass_texture, collidable=False))
        add_tree(3,3,-8)
        add_tree(12,3,-9)
        add_tree(20,1,-7)
        add_ball(-12, -3, 7, 4)
        config.frontcubes.append(Cube(-3, 1, 2, 7, 1, 2, config.grass_texture, collidable=False))
        config.frontcubes.append(Cube(4, 1, 1, 7, 1, 2, config.grass_texture, collidable=False))

        config.cubes.append(Cube(-3, 1.3, -4.5, 1, 6, 1, config.empty_texture, collidable=True))
        config.cubes.append(Cube(-12, 0.05, -4.5, 35, 1, 1, config.gravel_texture, collidable=False))
        config.cubes.append(SpecialKeyCube(18, 1, -5.5, 1,1,1, config.special_cube_texture, key=pygame.K_e, command=first_tutorial_cube, collidable=False, hint_image_path="assets/hint_e.png"))

        config.cubes.append(Cube(25, 0.01, 50, 100, 1, 65, config.water_texture, collidable=False, 
                                 on_touch=lambda: reset_tutorial(player)))
        add_ball(25, -2, -6, 100)
        config.cubes.append(Cube(23, 1, -4.5, 1,1,1, config.grass_texture, collidable=True))
        config.cubes.append(Cube(26, 2, -4, 2,1,2, config.grass_texture, collidable=True))
        config.cubes.append(Cube(29, 3, -4, 3,1,2, config.grass_texture, collidable=True))
        add_tree(31,4,-5)
        config.cubes.append(Cube(34, 3.5, -4.5, 3,1,2, config.grass_texture, collidable=True))
        config.cubes.append(Cube(40, 1, -4.5, 2,5,2, config.bark_texture, collidable=True))
        config.cubes.append(Cube(40, 6, -5.5, 2,4,1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(40, 10, -4.5, 2,10,2, config.bark_texture, collidable=True))


        config.cubes.append(Cube(46, 3.5, -4.5, 3,1,2, config.grass_texture, collidable=True))




        add_ball(52, -3, 4, 6, collidable=True, lenght=3)

        config.cubes.append(Cube(54, 3, -5.5, 1,4,1, config.wood_texture, collidable=False))
        config.frontcubes.append(Cube(54, 3, -3.5, 1,4,1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(54, 5, -4.5, 1,2,1, config.wood_texture, collidable=True))
        config.cubes.append(Cube(54, 3, -6.5, 7,4,1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(61, 3, -3.5, 1,4,3, config.wood_texture, collidable=True))
        config.cubes.append(Cube(54,2.01,-3.5, 7, 1, 4, config.wood_texture, collidable=False))
        config.cubes.append(Cube(55, 6.5, -3.5, 6,1,3, config.wood_texture, collidable=True))

        config.falling_block = Cube(53, 20, -4.5, 1, 1, 1, config.special_cube_texture, collidable=True)

        config.cubes.append(Cube(54, 3, -4.5, 1,1,1, config.empty_texture, collidable=False, on_touch=get_captured))
        config.frontcubes.append(config.falling_block)

        config.wife = NPC(
        x=60, 
        y=3, 
        z=-5, 
        width=-1.8, 
        height=1.8, 
        idle_sprites=config.npc_idle_sprites, 
        key=pygame.K_e, 
        command=talk_to_wife, 
        interaction_radius=2.0, 
        hint_image_path="assets/hint_e.png"
        )

        config.cubes.append(Cube(49, 4.5, -4.5,1,2,1, config.empty_texture, collidable=False, on_touch=cut_scene_enter))

        config.textbox = Textbox("Hello!jjjjj", 5, 1, "assets/font.otf", 100)
        config.textboxWIFE = Textbox("Wife",2,1, "assets/font.otf", 100)
    elif config.stage == 2:
        pygame.mixer.music.stop()
        music_path = os.path.join("assets", "sounds", "sheldon.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed
            pygame.mixer.music.play()

        config.cubes.append(Cube(-30, 0, 4, 100, 1,20 , config.grass_texture, collidable=True))
        config.cubes.append(Cube(0, 0, 5, 1, 1, 2, config.grass_texture, collidable=True))
        config.cubes.append(Cube(-30, 1, -5, 10, 6, 1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(-20, 1, -5.5, 10, 6, 1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(-10, 1, -6.5, 10, 6, 1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(0, 1, -7.5, 10, 6, 1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(10, 1, -6.5, 10, 6, 1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(20, 1, -5.5, 10, 6, 1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(30, 1, -5, 10, 6, 1, config.wood_texture, collidable=False))

        #config.cubes.append(Cube(-25, 1, 2, 1, 15, 10, config.bars_texture_left, collidable=True))
        #config.cubes.append(Cube(30, 1, 2, 1, 15, 7, config.bars_texture_left, collidable=True))
        #config.cubes.append(Cube(29, 1, 2, 0.1, 15, 7, config.empty_texture, collidable=True))
        add_tree(15,1,-5.5)
        config.cubes.append(SpecialKeyCube(15, 1, -4.5, 1, 1, 1, config.empty_texture, 
            key=pygame.K_e, 
            command=spawning_clouds,  # Call this function instead of the lambda
            collidable=False, 
            hint_image_path="assets/hint_e.png"))
        

        config.cubes.append(SpecialKeyCube(44, 15.8, -4.5, 1, 1, 1, config.flower_texture, 
            key=pygame.K_e, 
            command=lambda: leap_of_faith_interaction(),
            collidable=False, 
            hint_image_path="assets/hint_e.png"))
        
        JsonLoadData("maps/rabbitmap.json", config.cubes, collide=True)

        config.cubes.append(Cube(-30, 1, 2, 1, 6, 10, config.wood_texture, collidable=True))
        config.cubes.append(Cube(30, 1, 2, 1, 6, 7, config.wood_texture, collidable=False))
        config.cubes.append(Cube(29, 1, 2, 0.1, 6, 7, config.empty_texture, collidable=True))


    elif config.stage == 3:
        def reset_playerstage3():
                    player.x = -2
                    player.y = 0
        player.x=-2
        config.cubes.append(Cube(-500, -2, 50, 512, 3, 65, config.grass_texture, collidable=True))
        config.cubes.append(Cube(12, -2, 50, 20, 3, 65, config.floor_texture, collidable=True))
        config.cubes.append(Cube(15, -1.99, 50, 7, 3, 20, config.floor_texture, collidable=True,on_touch=reset_playerstage3))

        config.cubes.append(Cube(-7, 1, 1.5-2, 2, 4, 10, config.wood_texture, collidable=True))
        config.cubes.append(Cube(-5, 1, -5.5-4, 4, 4, 2, config.wood_texture, collidable=False))
        config.cubes.append(Cube(-1, 1, -6.5-4, 3, 4, 2, config.wood_texture, collidable=False))
        config.cubes.append(Cube(2, 1, -7.5-4, 2, 4, 2, config.wood_texture, collidable=False))
        config.cubes.append(Cube(4, 1, -6.5-4, 3, 4, 2, config.wood_texture, collidable=False))
        config.cubes.append(Cube(7, 1, -5.5-4, 4, 4, 2, config.wood_texture, collidable=False))

        config.cubes.append(Cube(-3, 1, -6.5, 4, 0.5, 1, config.wood_texture, collidable=False))
        config.frontcubes.append(Cube(-3, 1, -3.5, 4, 0.5, 1, config.wood_texture, collidable=False))

        config.cubes.append(Cube(-2, 0.3, -4.5, 2, 1, 2, config.water_texture, collidable=False))

        config.cubes.append(Cube(-3, 1, -4.5, 1, 0.5, 2, config.wood_texture, collidable=True))
        config.cubes.append(Cube(0, 1, -4.5, 1, 0.5, 2, config.wood_texture, collidable=True))

        config.cubes.append(Cube(12, 4, 1.5, 1, 1, 12, config.wood_texture, collidable=True))
        config.cubes.append(Cube(11, 1, -8.5, 2, 4, 1, config.wood_texture, collidable=False))


        config.cubes.append(Cube(12, 0.2, 1.5, 1, 1, 10, config.wood_texture, collidable=False))
        

        config.cubes.append(Cube(15, 1, -4, 1, 1, 2, config.wood_texture, collidable=True))
        config.cubes.append(Cube(17, 2, -4, 3, 1, 2, config.wood_texture, collidable=True))

        config.cubes.append(Cube(12, 1, -10, 20, 5, 5, config.brick_texture, collidable=False))

        config.cubes.append(Cube(22, 1, 1.5, 10, 3, 12, config.brick_texture, collidable=True))
        
        config.cubes.append(Cube(22, -2, 50, 512, 3, 65, config.water_texture, collidable=False, on_touch=reset_playerstage3))

        config.cubes.append(Cube(22, 1, -15, 500, 1, 1, config.grass_texture, collidable=False))

        config.cubes.append(Cube(12, 1, 1.5, 1, 3, 4, config.glass_texture, collidable=False))
        config.cubes.append(Cube(12, 1, -5.5, 1, 3, 2, config.glass_texture, collidable=False))

        config.cubes.append(Cube(34, 4, -4, 3, 1, 2, config.brick_texture, collidable=True))
        config.cubes.append(Cube(40, 5, -4, 2, 1, 2, config.brick_texture, collidable=True))
        config.cubes.append(Cube(44, 6, -4, 3, 1, 2, config.brick_texture, collidable=True))
        config.cubes.append(Cube(49, 7, -4, 2, 1, 2, config.brick_texture, collidable=True))

        config.cubes.append(Cube(54, 1, -6, 23, 7.1, 1, config.brick_texture, collidable=False))
        config.cubes.append(Cube(54, 1, -4, 22, 7, 2, config.wood_texture, collidable=True))
        config.cubes.append(Cube(54, 1, -3, 20, 7.1, 1, config.brick_texture, collidable=False))
        
        config.cubes.append(Cube(74, 1, 2, 1, 7.1, 6, config.brick_texture, collidable=False))
        config.cubes.append(Cube(75, 1, 2, 1, 7, 6, config.wood_texture, collidable=True))
        config.cubes.append(Cube(76, 1, 2, 1, 7.1, 9, config.brick_texture, collidable=True))

        config.cubes.append(Cube(77,1,2, 10,1,9, config.grass_texture, collidable=True))
        config.cubes.append(Cube(77,2,-7, 7,3,1, config.wood_texture, collidable=False))
        config.cubes.append(Cube(84,2,2, 1,3,9, config.wood_texture, collidable=True))

        config.cubes.append(Cube(83,2,-4.5, 1,1,1, config.special_cube_texture, collidable=True))

        config.cubes.append(Cube(92,2,-4, 2,1,2, config.special_cube_texture, collidable=True))

        config.cubes.append(Cube(99,3,-4, 3,1,2, config.special_cube_texture, collidable=True))

        config.cubes.append(Cube(109,1,-4, 3,1,2, config.special_cube_texture, collidable=True))



        config.cubes.append(Cube(118,1,0, 10,1,12, config.snow_texture, collidable=True))

        config.cubes.append(Cube(121,2,-6.5, 6,3,4, config.snow_texture, collidable=False))
        config.cubes.append(Cube(122,2,-5.5, 4,3,6, config.snow_texture, collidable=False))
        config.cubes.append(Cube(122,2,-6.5, 4,4,4, config.snow_texture, collidable=False))
        config.cubes.append(Cube(119,2,-7.5, 2,2,2, config.snow_texture, collidable=False))

        config.cubes.append(Cube(129,2,-4, 2,1,2, config.snow_texture, collidable=True))

        config.cubes.append(Cube(133,3,-4, 2,1,2, config.snow_texture, collidable=True))

        config.cubes.append(Cube(138,1,-4, 3,1,2, config.snow_texture, collidable=True))

        config.cubes.append(Cube(143,1,-1, 7,1,15, config.grass_texture, collidable=True))
        config.cubes.append(Cube(147,2,-5.5, 3,6,10.5, config.brick_texture, collidable=False))

        config.breakCubes.append(Cube(147,2,-1, 1,3,15, config.brick_texture, collidable=True))
        config.breakCubes.append(Cube(148,2,-1, 1,3,3, config.brick_texture, collidable=True))
        config.breakCubes.append(Cube(149,2,-1, 1,3,5, config.brick_texture, collidable=True))

        config.breakCubes.append(Cube(147,5,-1, 3,3,5, config.brick_texture, collidable=True))

        config.cubes.append(Cube(150,0,-1, 100, 2, 6, config.grass_texture, collidable=True))

        

        config.cubes.append(Cube(160,2,-4.5, 1, 1, 1, config.empty_texture, collidable=False, on_touch=end_game))

        # Ensure breakCubes are processed for collision
        for cube in config.breakCubes:
            cube.collidable = True
        #add enemies
        add_static_enemy(12, 1, -4.5, width=2, height=2, sprite_set="man1", debug=True,orientation="left")
        add_patrol_enemy(21, 5, -4.5, width=2, height=2, sprite_set="man2", patrol_min_x=22, patrol_max_x=31, debug=False)
        add_patrol_enemy(55, 5, -4.5, width=2, height=2, sprite_set="man1", patrol_min_x=55, patrol_max_x=76, debug=False)
        add_patrol_enemy(68, 5, -4.5, width=2, height=2, sprite_set="man2", patrol_min_x=55, patrol_max_x=76, debug=False)

        def talk_to_monkey():
            config.zoom_generator = smooth_zoom(35, 1.0)
            def sub_process():
                config.showTextBoxMONKEY = False
                config.monkeyNPC.hide_hint()
                config.textbox_update_queue.append(("Monke wanna\nescape?", 3, 1))
                config.showTextBox = True
                time.sleep(2)
                config.showTextBox = False
                config.showTextBoxMONKEY = True
                config.textboxMONKEY_update_queue.append(("ye", 1, 1))
                time.sleep(2)
                config.monkey_unlocked = True
                config.textboxMONKEY_update_queue.append(("I feel like you\nshould press 2...", 4, 1))
                time.sleep(2)
                config.showTextBoxMONKEY = False
                time.sleep(1)
                config.showTextBoxMONKEY = True
                config.textboxMONKEY_update_queue.append(("And maybe you\nshould press F...", 4, 1))
                config.zoom_generator = smooth_zoom(50, 1.0)
                time.sleep(2)
                config.showTextBoxMONKEY = False

                config.hint_update_queue_monkey.append(("show", "assets/hint_e.png"))


                
                

            threading.Thread(target=sub_process).start()

        def talk_to_fox():
            config.zoom_generator = smooth_zoom(35, 1.0)
            def sub_process():
                config.showTextBoxFOX = False
                config.foxNPC.hide_hint()
                config.textbox_update_queue.append(("Fox wanna\nescape?", 3, 1))
                config.showTextBox = True
                time.sleep(2)
                config.showTextBox = False
                config.showTextBoxFOX = True
                config.textboxFOX_update_queue.append(("ye", 1, 1))
                time.sleep(2)
                config.fox_unlocked = True
                config.textboxFOX_update_queue.append(("I feel like you\nshould press 3...", 4, 1))
                time.sleep(2)
                config.showTextBoxFOX = False
                time.sleep(1)
                config.showTextBoxFOX = True
                config.textboxFOX_update_queue.append(("And maybe you\nshould press SHIFT...", 4, 1))
                config.zoom_generator = smooth_zoom(50, 1.0)
                time.sleep(2)
                config.showTextBoxFOX = False

                config.hint_update_queue_fox.append(("show", "assets/hint_e.png"))
            threading.Thread(target=sub_process).start()

        def talk_to_bear():
            config.zoom_generator = smooth_zoom(35, 1.0)
            def sub_process():
                config.showTextBoxBEAR = False
                config.bearNPC.hide_hint()
                config.textbox_update_queue.append(("Bear wanna\nescape?", 3, 1))
                config.showTextBox = True
                time.sleep(2)
                config.showTextBox = False
                config.showTextBoxBEAR = True
                config.textboxBEAR_update_queue.append(("ye", 1, 1))
                time.sleep(2)
                config.bear_unlocked = True
                config.textboxBEAR_update_queue.append(("I feel like you\nshould press 4...", 4, 1))
                time.sleep(2)
                config.showTextBoxBEAR = False
                time.sleep(1)
                config.showTextBoxBEAR = True
                config.textboxBEAR_update_queue.append(("And maybe you\nshould press F...", 4, 1))
                config.zoom_generator = smooth_zoom(50, 1.0)
                time.sleep(2)
                config.showTextBoxBEAR = False
                config.bear_unlocked = True

                config.hint_update_queue_bear.append(("show", "assets/hint_e.png"))


                
                

            threading.Thread(target=sub_process).start()


        config.monkeyNPC = NPC(
        x=6, 
        y=1, 
        z=-5, 
        width=-1.8, 
        height=1.8, 
        idle_sprites=config.monkey_run_sprites, 
        key=pygame.K_e, 
        command=talk_to_monkey, 
        interaction_radius=2.0, 
        hint_image_path="assets/hint_e.png"
        )

        config.bearNPC = NPC(
        x=126, 
        y=2, 
        z=-5, 
        width=-1.8, 
        height=1.8, 
        idle_sprites=config.bear_idle_sprites, 
        key=pygame.K_e, 
        command=talk_to_bear, 
        interaction_radius=2.0, 
        hint_image_path="assets/hint_e.png"
        )

        config.foxNPC = NPC(
        x=83, 
        y=2, 
        z=-5, 
        width=-1.8, 
        height=1.8, 
        idle_sprites=config.fox_idle_sprites, 
        key=pygame.K_e, 
        command=talk_to_fox, 
        interaction_radius=2.0, 
        hint_image_path="assets/hint_e.png"
        )

    elif config.stage == 4:
        pygame.mixer.music.stop()
        music_path = os.path.join("assets", "sounds", "weddingsong.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        player.x=-2
        player.y = 1
        config.cubes.append(Cube(-500, -2, 50, 1000, 3, 65, config.grass_texture, collidable=True))
        #cubes.append(Cube(1, 1, -5.5, 4, 1, 1, config.grass_texture, collidable=False))
        add_ball(-15,-1,-4-.5,5)
        add_ball(-10,-3,-3-.5, 4)
        add_ball(-6,-2,-5-.5,6)
        add_ball(4,-1,-4-.5,3)
        add_ball(8,-3,-3-.5, 4)
        add_ball(16, -3, -6-.5, 5)
        config.cubes.append(Cube(-3, 1.3, -4.5, 1, 2, 1, config.empty_texture, collidable=True))
        config.cubes.append(Cube(-2, 0.05, -4, 15, 1, 2, config.carpet_texture, collidable=False))

        config.cubes.append(Cube(13, 1, -3, 1, 0.5, 4, config.wood_texture, collidable=True))
        config.cubes.append(Cube(14, 1, -3, 1, 1, 4, config.wood_texture, collidable=True))
        config.cubes.append(Cube(15, 1, -3, 1, 1.5, 4, config.wood_texture, collidable=True))
        config.cubes.append(Cube(16, 1, -2.5, 6, 2, 5, config.wood_texture, collidable=True))
        config.cubes.append(Cube(22, 1, -2.5, 1, 5, 5, config.wood_texture, collidable=True))
        config.cubes.append(Cube(22, 6, -3, 1, 1, 4, config.wood_texture, collidable=True))

        add_ball(24, -2, 2, 2)
        add_ball(23, -1, -2, 2)

        add_tree(25, 4, -5)
        add_tree(27, 3, -3)

        add_tree(-8.5,1,-6.5)
        add_tree(-2,3,-11)
        add_tree(5,1,1.5, 1)

        add_tree(12,1,-9)

        add_tree(12,1,-9)

        add_tree(18,2,-11.5)


        config.cubes.append(Cube(4, 1, -6.5, 0.5, 1, 2, config.wood_texture, collidable=False))
        config.npc_final_scene.append(NPC(x=4, y=1.3, z=-7, width=1.8, height=1.8, idle_sprites=config.monkey_idle_sprites, key=pygame.K_e, command=talk_to_wife, interaction_radius=0, hint_image_path="assets/hint_e.png"))
        config.cubes.append(Cube(4.1, 0.3, -6.5, 1, 1, 2, config.wood_texture, collidable=False))
        

        config.cubes.append(Cube(6, 1, -6.5, 0.5, 1, 2, config.wood_texture, collidable=False))
        config.cubes.append(Cube(6.1, 0.3, -6.5, 1, 1, 2, config.wood_texture, collidable=False))
        config.npc_final_scene.append(NPC(x=6, y=1.3, z=-7, width=1.8, height=1.8, idle_sprites=config.bear_idle_sprites, key=pygame.K_e, command=talk_to_wife, interaction_radius=0, hint_image_path="assets/hint_e.png"))


        config.frontcubes.append(Cube(4, 1, -1.5, 0.5, 1, 2, config.wood_texture, collidable=False))
        config.npc_final_scene_front.append(NPC(x=4, y=1.3, z=-2.5, width=1.8, height=1.8, idle_sprites=config.npc_idle_sprites, key=pygame.K_e, command=talk_to_wife, interaction_radius=0, hint_image_path="assets/hint_e.png"))
        config.frontcubes.append(Cube(4.1, 0.3, -1.5, 1, 1, 2, config.wood_texture, collidable=False))

        
        config.frontcubes.append(Cube(6, 1, -1.5, 0.5, 1, 2, config.wood_texture, collidable=False))
        config.frontcubes.append(Cube(6.1, 0.3, -1.5, 1, 1, 2, config.wood_texture, collidable=False))
        config.npc_final_scene_front.append(NPC(x=5.5, y=1.3, z=-2.5, width=1.8, height=1.8, idle_sprites=config.fox_idle_sprites, key=pygame.K_e, command=talk_to_wife, interaction_radius=0, hint_image_path="assets/hint_e.png"))


        
        config.cubes.append(Cube(0, 1, -6.5, 0.5, 1, 2, config.wood_texture, collidable=False))
        config.cubes.append(Cube(0.1, 0.3, -6.5, 1, 1, 2, config.wood_texture, collidable=False))
        config.npc_final_scene.append(NPC(x=0, y=1.3, z=-7, width=1.8, height=1.8, idle_sprites=config.npc_idle_sprites, key=pygame.K_e, command=talk_to_wife, interaction_radius=0, hint_image_path="assets/hint_e.png"))


        config.cubes.append(Cube(2, 1, -6.5, 0.5, 1, 2, config.wood_texture, collidable=False))
        config.cubes.append(Cube(2.1, 0.3, -6.5, 1, 1, 2, config.wood_texture, collidable=False))
        config.npc_final_scene.append(NPC(x=2, y=1.3, z=-7, width=1.8, height=1.8, idle_sprites=config.npc_idle_sprites, key=pygame.K_e, command=talk_to_wife, interaction_radius=0, hint_image_path="assets/hint_e.png"))


        config.frontcubes.append(Cube(0, 1, -1.5, 0.5, 1, 2, config.wood_texture, collidable=False))
        config.frontcubes.append(Cube(0.1, 0.3, -1.5, 1, 1, 2, config.wood_texture, collidable=False))
        config.npc_final_scene_front.append(NPC(x=0, y=1.3, z=-2.5, width=1.8, height=1.8, idle_sprites=config.npc_idle_sprites, key=pygame.K_e, command=talk_to_wife, interaction_radius=0, hint_image_path="assets/hint_e.png"))

        
        config.frontcubes.append(Cube(2, 1, -1.5, 0.5, 1, 2, config.wood_texture, collidable=False))
        config.frontcubes.append(Cube(2.1, 0.3, -1.5, 1, 1, 2, config.wood_texture, collidable=False))
        config.npc_final_scene_front.append(NPC(x=2, y=1.3, z=-2.5, width=1.8, height=1.8, idle_sprites=config.npc_idle_sprites, key=pygame.K_e, command=talk_to_wife, interaction_radius=0, hint_image_path="assets/hint_e.png"))

        def zoom_marry():
            config.zoom_generator = smooth_zoom(30, 1.0)

        def talk_to_wife_fancy():

            def sub_process():
                config.wife_FANCY_NPC.hide_hint()
                time.sleep(2)
                config.showTextBoxWIFEFANCY = True
                config.textboxWIFEFANCY_update_queue.append(("<3", 1, 1))
                time.sleep(4)
                config.frontcubes.append(Cube(-100, -100, 2.5, 1000, 1000, 1, config.black_texture, collidable=False, id="blackscreen"))

                
            threading.Thread(target=sub_process).start()


        config.cubes.append(Cube(14, 3, -4.5, 1, 1, 1, config.empty_texture, collidable=False, on_touch=zoom_marry))

        config.wife_FANCY_NPC = NPC(
        x=21, 
        y=3, 
        z=-5, 
        width=-2, 
        height=2, 
        idle_sprites=config.wife_fancy_idle_sprites, 
        key=pygame.K_e, 
        command=talk_to_wife_fancy, 
        interaction_radius=2.0, 
        hint_image_path="assets/hint_e.png"
        )



    '''elif config.stage == 3:
        JsonLoadData("maps/skibidi.json", config.cubes, collide=True)
        config.cubes.append(Cube(7, 0.01, -2, 6, 1, 6, config.water_texture, collidable=False,on_touch=lambda: reset_tutorial(player)))
        #config.cubes.append(Cube(6, 1, -1, 1, 1, 7, config.grass_texture, collidable=True))
        #config.cubes.append(Cube(6, 1, -8, 7, 1, 1, config.grass_texture, collidable=True))
        #config.cubes.append(Cube(13, 1, -1, 1, 1, 8, config.grass_texture, collidable=True))
        #config.cubes.append(Cube(6, 1, -1, 7, 1, 1, config.grass_texture, collidable=True))
        config.cubes.append(Cube(24, 1, -1, 7, 1, 1, config.grass_texture, collidable=True))
        #baseplate
        
        

        config.cubes.append(Cube(-500, -2, 50, 1000, 3, 65, config.grass_texture, collidable=True))

        #0,0 refrence
        config.cubes.append(Cube(0, 1, -5.5, 1, 1, 1, config.grass_texture, collidable=False))
        config.cubes.append(Cube(0, 2, -5.5, 1, 1, 1, config.grass_texture, collidable=False))
        config.cubes.append(Cube(0, 3, -5.5, 1, 1, 1, config.grass_texture, collidable=False))

        #big tree   
        config.cubes.append(Cube(3, 0, -5.5, 1, 20, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(4, 0, -5.5, 1, 20, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(3, 0, -6.5, 1, 20, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(4, 0, -6.5, 1, 20, 1, config.bark_texture, collidable=False))

        config.cubes.append(Cube(-5, 1, -10.5, 10, 10, 1, config.bark_texture, collidable=False))
        #middle part wall
        config.cubes.append(Cube(5, 1, -9.5, 10, 10, 1, config.bark_texture, collidable=False))
        #right
        config.cubes.append(Cube(15, 1, -8.5, 10, 10, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(25, 1, 1.5, 1, 10, 10, config.bark_texture, collidable=True))
        config.cubes.append(Cube(24, 1, -5.5, 1, 10, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(23, 1, -6.5, 1, 10, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(22, 1, -7.5, 1, 10, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(24, 1, -5.5, 1, 10, 1, config.empty_texture, collidable=True))

        #left part wall
        config.cubes.append(Cube(-15, 1, -9.5, 10, 10, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(-25, 1, -8.5, 10, 10, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(-24, 1, 1.5, 1, 10, 10, config.bark_texture, collidable=True))
        config.cubes.append(Cube(-23, 1, -6.5, 1, 10, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(-22, 1, -7.5, 1, 10, 1, config.bark_texture, collidable=False))
        config.cubes.append(Cube(-24, 1, -5.5, 1, 100, 1, config.empty_texture, collidable=False))
    elif config.stage == 4:

        #config.cubes.append(Cube(-10, 1, 5, 20, 1, 20, config.grass_texture, collidable=True))
        #config.cubes.append(Cube(10, 0, -4, 1, 1, 3, config.dirt_texture, collidable=True))
        #config.cubes.append(Cube(9, -5, -1, 1, 6, 5, config.dirt_texture, collidable=True))
        config.cubes.append(Cube(-10, 1, 5, 20, 1, 20, config.grass_texture, collidable=True))
    
        # Cave entrance and staircase (rotated to face left/player)
        # Front wall (was right wall)
        config.cubes.append(Cube(10, 1, -1, 1, 5, 7, config.bark_texture, collidable=True))
        # Back wall (was left wall)
        config.cubes.append(Cube(16, 1, -1, 1, 5, 7, config.bark_texture, collidable=True))
        # Left side wall (was back wall)
        config.cubes.append(Cube(11, 1, -7, 5, 5, 1, config.bark_texture, collidable=True))
        # Right side wall
        config.cubes.append(Cube(11, 1, 5, 5, 5, 1, config.bark_texture, collidable=True))
        # Ceiling
        config.cubes.append(Cube(11, 6, -1, 5, 1, 7, config.bark_texture, collidable=True))
        
        # Staircase - going left (negative x) instead of forward
        config.cubes.append(Cube(9, 1, -1, 2, 1, 2, config.dirt_texture, collidable=True))
        config.cubes.append(Cube(7, 0, -1, 2, 1, 2, config.dirt_texture, collidable=True))
        config.cubes.append(Cube(5, -1, -1, 2, 1, 2, config.dirt_texture, collidable=True))
        config.cubes.append(Cube(3, -2, -1, 2, 1, 2, config.dirt_texture, collidable=True))
        config.cubes.append(Cube(1, -3, -1, 2, 1, 2, config.dirt_texture, collidable=True))
        config.cubes.append(Cube(-1, -4, -1, 2, 1, 2, config.dirt_texture, collidable=True))
        
        # Bottom cave area (expanding in negative x direction)
        config.cubes.append(Cube(-12, -5, 0, 11, 1, 2, config.dirt_texture, collidable=True))
        config.cubes.append(Cube(-12, -5, -3, 11, 1, 2, config.dirt_texture, collidable=True))
        config.cubes.append(Cube(-12, -5, -1, 12, 1, 1, config.dirt_texture, collidable=True))
        
        # Add some stalactites for cave atmosphere
        config.cubes.append(Cube(8, 5, -0.5, 1, 1, 1, config.gravel_texture, collidable=False))
        config.cubes.append(Cube(5, 4, -2, 1, 2, 1, config.gravel_texture, collidable=False))'''


def add_static_enemy(x, y, z=0, width=2, height=2, sprite_set="man1", health=1, damage=10, 
                    debug=False, direction=1, orientation="right"):
    """
    Add a static enemy that doesn't move but damages the player on contact.
    
    :param orientation: The direction the enemy is facing ("left" or "right")
    """
    # Create a default texture in case the sprite loading fails
    default_texture = load_texture("assets/enemies/default.png") if os.path.exists("assets/enemies/default.png") else load_texture("assets/empty.png")
    
    enemy = Enemy(
        x=x, y=y, z=z,
        width=width, height=height,
        sprite_set=sprite_set,
        behavior="static",
        health=health,
        damage=damage,
        debug=debug,
        texture_path="assets/enemies/default.png"  # Fallback texture path
    )
    
    # Set the enemy's direction based on orientation
    if orientation.lower() == "left":
        enemy.direction = -1
    else:  # Default to right
        enemy.direction = 1
        
    # Ensure the enemy has a valid texture
    if not hasattr(enemy, 'texture') or enemy.texture is None:
        enemy.texture = default_texture
        
    config.enemies.append(enemy)
    return enemy

def add_patrol_enemy(x, y, z=0, width=2, height=2, patrol_min_x=None, patrol_max_x=None, 
                    sprite_set="man2", speed=0.04, health=2, damage=15, debug=False):
    """Add a patrol enemy that moves back and forth between two points."""
    # Default patrol range if not specified
    if patrol_min_x is None:
        patrol_min_x = x - 5
    if patrol_max_x is None:
        patrol_max_x = x + 5
    
    # Create a default texture in case the sprite loading fails
    default_texture = load_texture("assets/enemies/default.png") if os.path.exists("assets/enemies/default.png") else load_texture("assets/empty.png")
    
    enemy = Enemy(
        x=x, y=y, z=z,
        width=width, height=height,
        sprite_set=sprite_set,
        behavior="patrol",
        patrol_min_x=patrol_min_x,
        patrol_max_x=patrol_max_x,
        speed=speed,
        health=health,
        damage=damage,
        debug=debug,
        texture_path="assets/enemies/default.png"  # Fallback texture path
    )
    
    # Ensure the enemy has a valid texture
    if not hasattr(enemy, 'texture') or enemy.texture is None:
        enemy.texture = default_texture
        
    config.enemies.append(enemy)
    return enemy

def add_follow_enemy(x, y, z=0, width=2, height=2, radius=8, 
                    sprite_set="rabbit", speed=0.06, health=1, damage=10, debug=False):
    """Add a follow enemy that chases the player when in range."""
    # Create a default texture in case the sprite loading fails
    default_texture = load_texture("assets/enemies/default.png") if os.path.exists("assets/enemies/default.png") else load_texture("assets/empty.png")
    
    enemy = Enemy(
        x=x, y=y, z=z,
        width=width, height=height,
        sprite_set=sprite_set,
        behavior="follow",
        radius=radius,
        speed=speed,
        health=health,
        damage=damage,
        debug=debug,
        texture_path="assets/enemies/default.png"  # Fallback texture path
    )
    
    # Ensure the enemy has a valid texture
    if not hasattr(enemy, 'texture') or enemy.texture is None:
        enemy.texture = default_texture
        
    config.enemies.append(enemy)
    return enemy


