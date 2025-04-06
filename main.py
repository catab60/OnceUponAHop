from components.init import *
import components.config as config
from components.functions import *
from components.Player import PlayerObject, Enemy
from components.Cubes import Cube, SpecialKeyCube, Explosion
from components.Textbox import Textbox
from components.NPC import NPC  
import pyautogui
import math  
from components.functions import push_config_to_player







background_layers = get_background_layers()

start_button_texture = load_texture("assets/start_button.png")
exit_button_texture = load_texture("assets/exit_button.png")


logo_texture = load_texture("assets/logo.png")


if config.fast_start:
    in_menu = False
else:
    in_menu = True


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

def render_parallax_background(camera_x, camera_y, width_t=40):

    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    for layer in background_layers:
        glBindTexture(GL_TEXTURE_2D, layer["texture"])
        layer_x = -camera_x * layer["speed"] + layer["offset_x"]
        layer_y = -camera_y * layer["speed"] + layer["offset_y"]

        texture_width = layer.get("width", width_t)
        texture_height = texture_width * (height / width)

        spacing = layer.get("spacing", texture_width)


        for tile in range(-layer["left"], layer["right"] + 1):
            tile_offset = tile * spacing
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(layer_x + tile_offset - texture_width / 2, layer_y - texture_height / 2, -10)
            glTexCoord2f(1, 0); glVertex3f(layer_x + tile_offset + texture_width / 2, layer_y - texture_height / 2, -10)
            glTexCoord2f(1, 1); glVertex3f(layer_x + tile_offset + texture_width / 2, layer_y + texture_height / 2, -10)
            glTexCoord2f(0, 1); glVertex3f(layer_x + tile_offset - texture_width / 2, layer_y + texture_height / 2, -10)
            glEnd()

    glPopMatrix()
    glPopAttrib()
def render_moving_background():

    global background_offset_x
    background_offset_x -= background_scroll_speed  

    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    
    glBindTexture(GL_TEXTURE_2D, load_texture("assets/mainmenu.png"))
    glBegin(GL_QUADS)
    glTexCoord2f(0 + background_offset_x, 0); glVertex3f(-background_width / 2, -background_height / 2, -20)  
    glTexCoord2f(1 + background_offset_x, 0); glVertex3f(background_width / 2, -background_height / 2, -20)   
    glTexCoord2f(1 + background_offset_x, 1); glVertex3f(background_width / 2, background_height / 2, -20)    
    glTexCoord2f(0 + background_offset_x, 1); glVertex3f(-background_width / 2, background_height / 2, -20)   
    glEnd()

    glPopMatrix()
    glPopAttrib()

def render_menu():
    global logo_animation_time
    x_offset = 4500
    y_offset = -3000
    pad_y = 500


    logo_width = 7
    logo_height = 7
    logo_x_offset = -6
    logo_y_offset = -3.5 + math.sin(logo_animation_time * logo_frequency) * logo_amplitude

    logo_animation_time += 0.01
    button_width = 4
    button_height =3

    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    glBindTexture(GL_TEXTURE_2D, logo_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(logo_x_offset, logo_y_offset, -10)
    glTexCoord2f(1, 0); glVertex3f(logo_x_offset + logo_width, logo_y_offset, -10)
    glTexCoord2f(1, 1); glVertex3f(logo_x_offset + logo_width, logo_y_offset + logo_height, -10)
    glTexCoord2f(0, 1); glVertex3f(logo_x_offset, logo_y_offset + logo_height, -10)
    glEnd()


    glBindTexture(GL_TEXTURE_2D, start_button_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-button_width / 2 + x_offset / 1000, 0.5 + y_offset / 1000 + pad_y / 1000, -10)
    glTexCoord2f(1, 0); glVertex3f(button_width / 2 + x_offset / 1000, 0.5 + y_offset / 1000 + pad_y / 1000, -10)
    glTexCoord2f(1, 1); glVertex3f(button_width / 2 + x_offset / 1000, 0.5 + y_offset / 1000 + pad_y / 1000 + button_height, -10)
    glTexCoord2f(0, 1); glVertex3f(-button_width / 2 + x_offset / 1000, 0.5 + y_offset / 1000 + pad_y / 1000 + button_height, -10)
    glEnd()


    glBindTexture(GL_TEXTURE_2D, exit_button_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-button_width / 2 + x_offset / 1000, -0.5 + y_offset / 1000 - pad_y / 1000, -10)
    glTexCoord2f(1, 0); glVertex3f(button_width / 2 + x_offset / 1000, -0.5 + y_offset / 1000 - pad_y / 1000, -10)
    glTexCoord2f(1, 1); glVertex3f(button_width / 2 + x_offset / 1000, -0.5 + y_offset / 1000 - pad_y / 1000 + button_height, -10)
    glTexCoord2f(0, 1); glVertex3f(-button_width / 2 + x_offset / 1000, -0.5 + y_offset / 1000 - pad_y / 1000 + button_height, -10)
    glEnd()

    glPopMatrix()
    glPopAttrib()

def check_menu_click(mouse_x, mouse_y):

    
    (f"Mouse position: ({mouse_x}, {mouse_y})")
    start_button_x1, start_button_y1 = 1275, 520
    start_button_x2, start_button_y2 = 1680, 680

    exit_button_x1, exit_button_y1 = 1278, 755
    exit_button_x2, exit_button_y2 = 1680, 900

    if start_button_x1 <= mouse_x <= start_button_x2 and start_button_y1 <= mouse_y <= start_button_y2:
        return "start"

    if exit_button_x1 <= mouse_x <= exit_button_x2 and exit_button_y1 <= mouse_y <= exit_button_y2:
        return "exit"

    return None

def draw_cross_at_mouse():

    mouse_x, mouse_y = pyautogui.position()

    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glColor3f(1.0, 0.0, 0.0) 

    glBegin(GL_LINES)
    glVertex2f(mouse_x - 10, config.screen_height - mouse_y) 
    glVertex2f(mouse_x + 10, config.screen_height - mouse_y)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(mouse_x, config.screen_height - mouse_y - 10)
    glVertex2f(mouse_x, config.screen_height - mouse_y + 10)
    glEnd()

    glPopMatrix()
    glPopAttrib()

def fade_to_black():
 
    for alpha in range(0, 256, fade_speed): 
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glPushMatrix()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, alpha / 255.0) 
        glBegin(GL_QUADS)
        glVertex3f(-fade_width, -fade_height, -1)
        glVertex3f(fade_width, -fade_height, -1)
        glVertex3f(fade_width, fade_height, -1)
        glVertex3f(-fade_width, fade_height, -1)
        glEnd()
        glPopMatrix()
        glPopAttrib()
        pygame.display.flip()
        clock.tick(60)


def play_stage_music(stage_number):

    pygame.mixer.music.stop()
    
    if stage_number == 1:

        music_path = os.path.join("assets", "sounds", "sheldon.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)  
            pygame.mixer.music.play(-1)  


player = PlayerObject(0, 2, -5)
stageload(player)


pygame.mixer.init()

if config.stage == 1:
    play_stage_music(1)





previous_time = pygame.time.get_ticks() / 1000.0  

while True:
    
    current_time = pygame.time.get_ticks() / 1000.0
    delta_time = current_time - previous_time  
    previous_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and in_menu:
            mouse_x, mouse_y = pyautogui.position()  
            action = check_menu_click(mouse_x, mouse_y)
            if action == "start":
                fade_to_black()  
                in_menu = False
            elif action == "exit":
                pygame.quit()
                quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                
                if player.character == "monkey" and player.can_shoot:
                    player.shooting = True
                    player.state = "shoot"
                    config.gun_sound.play()
                    spawn_projectile(player)
                
                elif player.weapon_equipped and player.can_shoot:
                    player.shooting = True
                    player.state = "shoot"
                    spawn_projectile(player)
            else:
                player.shooting = False

    if in_menu:
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(config.fov, (width / height), config.near_clip, config.far_clip)
        render_moving_background()  
        render_menu()  
        draw_cross_at_mouse()  
        pygame.display.flip()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        config.zoom_generator = smooth_zoom(50, 1.0)

    if keys[pygame.K_x]:  
        config.zoom_generator = smooth_zoom(90, 1.0)

    if config.spawn_clouds:
        loadStage2Parkour("maps/rabbitmap.json", config.cubes, collide=True)
        config.spawn_clouds = False

    if not hasattr(config, 'last_stage') or config.stage != config.last_stage:
        background_layers = get_background_layers()
        config.last_stage = config.stage


        for cube in config.cubes:
            if isinstance(cube, SpecialKeyCube):
                cube.show_hint(hint_image_path="assets/hint_e.png")

        if hasattr(config, 'monkeyNPC') and config.monkeyNPC:
            config.monkeyNPC.show_hint()
        if hasattr(config, 'foxNPC') and config.foxNPC:
            config.foxNPC.show_hint()
        if hasattr(config, 'bearNPC') and config.bearNPC:
            config.bearNPC.show_hint()
        if hasattr(config, 'wife') and config.wife:
            config.wife.show_hint()

        if hasattr(config, 'wife_FANCY_NPC') and config.wife_FANCY_NPC:
            config.wife_FANCY_NPC.show_hint()


        if config.stage == 3:
            for npc in config.npc_final_scene:
                npc.show_hint()
            for npc in config.npc_final_scene_front:
                npc.show_hint()

    if keys[pygame.K_s]:
        shake_intensity = 0.1  
        config.camera_x += random.uniform(-shake_intensity, shake_intensity)
        config.camera_y += random.uniform(-shake_intensity, shake_intensity)

    if config.zoom_generator:
        try:
            next(config.zoom_generator)
        except StopIteration:
            config.zoom_generator = None

    
    target_camera_x = -player.x - player.width / 2 - 1
    target_camera_y = -player.y - player.height / 2 - 1
    config.camera_x += (target_camera_x - config.camera_x) * config.camera_smoothness
    config.camera_y += (target_camera_y - config.camera_y) * config.camera_smoothness

    

   

    
    if config.stage==1:
        config.wife.check_key_press(keys, player)

    
    if config.hint_update_queue:
        action, hint_image_path = config.hint_update_queue.pop(0)
        if action == "show":
            if config.stage ==1:
                config.wife.show_hint(hint_image_path)

    
            
    
                
        

    
    if config.textbox_update_queue:
        new_text, new_width, new_height = config.textbox_update_queue.pop(0)
        config.textbox.set_text(new_text, new_width, new_height)
    if config.stage == 1:
        if config.textboxWIFE_update_queue:
            new_text, new_width, new_height = config.textboxWIFE_update_queue.pop(0)
            config.textboxWIFE.set_text(new_text, new_width, new_height)


    if config.textboxMONKEY_update_queue:
        new_text, new_width, new_height = config.textboxMONKEY_update_queue.pop(0)
        config.textboxMONKEY.set_text(new_text, new_width, new_height)
    

    if config.textboxFOX_update_queue:
        new_text, new_width, new_height = config.textboxFOX_update_queue.pop(0)
        config.textboxFOX.set_text(new_text, new_width, new_height)
    
    if config.textboxBEAR_update_queue:
        new_text, new_width, new_height = config.textboxBEAR_update_queue.pop(0)
        config.textboxBEAR.set_text(new_text, new_width, new_height)

    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(config.fov, (width / height), config.near_clip, config.far_clip)
    glTranslatef(config.camera_x, config.camera_y, config.camera_z)

    
    render_parallax_background(config.camera_x, config.camera_y, width_t=20)

    
    glEnable(GL_DEPTH_TEST)

    

    for cube in config.cubes:
        cube.render()
        cube.render_hitbox()
        if isinstance(cube, SpecialKeyCube):
            cube.render_key_hint(player)
            cube.render_debug_radius() 
            cube.check_key_press(keys, player)

    for cube in config.breakCubes:
        cube.render()
        cube.render_hitbox()
  
    for explosion in config.explosions[:]:  
        explosion.update()
        explosion.render(scale=2)  
        if not explosion.active:
            config.explosions.remove(explosion)

    for transform in config.transform[:]:  
        transform.update()
        transform.render(scale=2)  
        if not transform.active:
            config.transform.remove(transform)

    
    if config.stage ==1:
        config.wife.render_idle_animation()
        config.wife.render_key_hint(player)
        config.wife.render_debug_radius()

   
    player.update(config.cubes + config.breakCubes)

    for cube in config.breakCubes:
        cube.render()
        cube.render_hitbox()

        if player.x + player.collision_offset_x + player.collision_width > cube.x and \
           player.x + player.collision_offset_x < cube.x + cube.width and \
           player.y + player.collision_offset_y + player.collision_height > cube.y and \
           player.y + player.collision_offset_y < cube.y + cube.height:
            if cube.collidable:
                config.breakCubes.remove(cube)

    for projectile in config.projectiles:
        if projectile:
            projectile.update(config.cubes, player,config.enemies) 
            projectile.render()


    for enemy in config.enemies[:]:  
        if enemy in config.enemies:
            enemy.update(player, config.cubes, delta_time)
            enemy.render()
            enemy.render_hitbox()

    if config.stage == 3:
        if hasattr(config, 'monkeyNPC') and config.monkeyNPC:
            config.monkeyNPC.render_idle_animation()
            config.monkeyNPC.render_key_hint(player)
            config.monkeyNPC.render_debug_radius()
        
    if hasattr(config, 'foxNPC') and config.foxNPC:
        config.foxNPC.render_idle_animation()
        config.foxNPC.render_key_hint(player)
        config.foxNPC.render_debug_radius()

    if hasattr(config, 'bearNPC') and config.bearNPC:
        config.bearNPC.render_idle_animation()
        config.bearNPC.render_key_hint(player)
        config.bearNPC.render_debug_radius()

    if config.stage == 4:
        if hasattr(config, 'wife_FANCY_NPC') and config.wife_FANCY_NPC:
            config.wife_FANCY_NPC.render_idle_animation()
            config.wife_FANCY_NPC.render_key_hint(player)
            config.wife_FANCY_NPC.render_debug_radius()


    for npc in config.npc_final_scene:
        npc.render_idle_animation()
        npc.render_key_hint(player)
        npc.render_debug_radius()

    
    player.render()
    player.render_hitbox()

    if config.stage == 3:
        if hasattr(config, 'monkeyNPC') and config.monkeyNPC:
            config.monkeyNPC.render_idle_animation()
            config.monkeyNPC.render_key_hint(player)
            config.monkeyNPC.render_debug_radius()
        
    if hasattr(config, 'foxNPC') and config.foxNPC:
        config.foxNPC.render_idle_animation()
        config.foxNPC.render_key_hint(player)
        config.foxNPC.render_debug_radius()
    
    if hasattr(config, 'bearNPC') and config.bearNPC:
        config.bearNPC.render_idle_animation()
        config.bearNPC.render_key_hint(player)
        config.bearNPC.render_debug_radius()

    if hasattr(config, 'wife_FANCY_NPC') and config.wife_FANCY_NPC:
        config.wife_FANCY_NPC.render_idle_animation()
        config.wife_FANCY_NPC.render_key_hint(player)
        config.wife_FANCY_NPC.render_debug_radius()
    


    for npc in config.npc_final_scene:
        npc.render_idle_animation()
        npc.render_key_hint(player)
        npc.render_debug_radius()
        

    for npc in config.npc_final_scene_front:
        npc.render_idle_animation()
        npc.render_key_hint(player)
        npc.render_debug_radius()
    
    for cube in config.breakFront:
        cube.render()
        cube.render_hitbox()


    config.player = player

    for cube in config.frontcubes:
        cube.render()
        cube.render_hitbox()
        if isinstance(cube, SpecialKeyCube):
            cube.render_key_hint(player)
            cube.render_debug_radius()

    if config.showTextBox:
        config.textbox.render(player.x+0.85, player.y+0.5, player.z)
    if config.stage == 1:
        if config.showTextBoxWIFE:
            config.textboxWIFE.render(config.wife.x-0.85, config.wife.y+0.5, config.wife.z)


    if config.showTextBoxMONKEY and hasattr(config, 'monkeyNPC') and config.monkeyNPC:
        config.textboxMONKEY.render(config.monkeyNPC.x-0.85, config.monkeyNPC.y+0.5, config.monkeyNPC.z)
    
    if config.showTextBoxFOX and hasattr(config, 'foxNPC') and config.foxNPC:  
        config.textboxFOX.render(config.foxNPC.x-0.85, config.foxNPC.y+0.5, config.foxNPC.z)
    
    if config.showTextBoxBEAR and hasattr(config, 'bearNPC') and config.bearNPC:
        config.textboxBEAR.render(config.bearNPC.x-0.85, config.bearNPC.y+0.5, config.bearNPC.z)

    if config.showTextBoxWIFEFANCY and hasattr(config, 'wife_FANCY_NPC') and config.wife_FANCY_NPC:
        config.textboxWIFEFANCY.render(config.wife_FANCY_NPC.x-0.85, config.wife_FANCY_NPC.y+0.5, config.wife_FANCY_NPC.z)

    if hasattr(config, 'monkeyNPC') and config.monkeyNPC:
        config.monkeyNPC.check_key_press(keys, player)
        
    if hasattr(config, 'foxNPC') and config.foxNPC:
        config.foxNPC.check_key_press(keys, player)

    if hasattr(config, 'bearNPC') and config.bearNPC:
        config.bearNPC.check_key_press(keys, player)

    if hasattr(config, 'wife_FANCY_NPC') and config.wife_FANCY_NPC:
        config.wife_FANCY_NPC.check_key_press(keys, player)
        
    for npc in config.npc_final_scene:
        npc.check_key_press(keys, player)
        
    for npc in config.npc_final_scene_front:
        npc.check_key_press(keys, player)

    push_config_to_player(player)


    def refresh_hint_textures():

        for cube in config.cubes:
            if isinstance(cube, SpecialKeyCube):
                if not hasattr(cube, 'hint_texture') or not cube.hint_texture:
                    cube.show_hint(hint_image_path="assets/hint_e.png")
        

        for cube in config.frontcubes:
            if isinstance(cube, SpecialKeyCube):
                if not hasattr(cube, 'hint_texture') or not cube.hint_texture:
                    cube.show_hint(hint_image_path="assets/hint_e.png")
        

        for npc_attr in ['monkeyNPC', 'foxNPC', 'bearNPC', 'wife', 'wife_FANCY_NPC']:
            if hasattr(config, npc_attr) and getattr(config, npc_attr):
                npc = getattr(config, npc_attr)
                if not hasattr(npc, 'hint_texture') or not npc.hint_texture:
                    npc.show_hint()
        

        for npc_list in [config.npc_final_scene, config.npc_final_scene_front]:
            if hasattr(config, 'npc_final_scene'):
                for npc in npc_list:
                    if not hasattr(npc, 'hint_texture') or not npc.hint_texture:
                        npc.show_hint()

    refresh_hint_textures()

    pygame.display.flip()
    clock.tick(60)

