from components.init import *
from components.config import *
from components.functions import *
from components.Cubes import Cube, SpecialKeyCube, Explosion

import components.config as config

class PlayerObject:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.width, self.height = 2, 2  # Plane dimensions
        self.collision_width, self.collision_height = 0.8, 1.5  # Editable collision box dimensions
        self.collision_offset_x, self.collision_offset_y = 0.5, 0  # Collision box offset
        self.velocity_y = 0
        self.on_ground = False
        self.direction = 1  # 1 for right, -1 for left
        self.animation_frame = 0
        self.state = "idle"  # idle, run, jump, shoot
        self.speed = 0.1
        self.jump_speed = 0.2
        self.weapon_equipped = False  # Whether the player is holding a weapon
        self.shooting = False  # Whether the player is shooting

        self.health = 100000

        self.melee_cooldown = 0  # Cooldown timer for melee attacks
        self.melee_cooldown_time = 30

        self.available_characters = ["bear", "rabbit", "monkey", "fox", "owl", "fancy_rabbit"]
        self.character = "rabbit"  # Always start with rabbit
        
        # Character-specific attributes
        self.character_attributes = {
            "bear": {
                "jump_speed": 0.2,
                "can_melee": True,
                "can_shoot": False,
                "speed": 0.1
            },
            "rabbit": {
                "jump_speed": 0.27,  # Higher jump
                "can_shoot": False,
                "can_melee": False,
                "speed": 0.12       # Slightly faster
            },
            "monkey": {
                "jump_speed": 0.2, # Lower jump
                "can_shoot": True,
                "can_melee": False,
                "speed": 0.1
            },
            "fox": {
                "jump_speed": 0.22,
                "can_shoot": True,
                "can_melee": False,
                "speed": 0.14,       # Fast runner
                "dash_power": 3,   # How far the dash goes
                "dash_cooldown": 60  # Frames before dash can be used again
            },
            "fancy_rabbit": {
                "jump_speed": 0.27,  # Higher jump than rabbit
                "can_shoot": False,   # Can shoot
                "can_melee": False,  # Cannot melee
                "speed": 0.12        # Faster than rabbit
            }
        }

        self.jump_speed = self.character_attributes[self.character]["jump_speed"]
        self.can_shoot = self.character_attributes[self.character]["can_shoot"]
        self.speed = self.character_attributes[self.character]["speed"]
        
        self.weapon_equipped = False  # Whether the player is holding a weapon
        self.shooting = False  # Whether the player is shooting

        self.dash_cooldown = 0  # Current cooldown timer
        self.dashing = False    # Whether currently dashing

        self.flying = False       # Replace gliding with flying
        self.flight_energy = 100  # Start with full flight energy

        self.previous_q_state = False

        # Add new properties for smooth dash
        self.dash_progress = 0       # Current progress of dash (0 to dash_duration)
        self.dash_duration = 10      # Number of frames to complete dash
        self.dash_target_x = 0       # Target X position for dash
        self.dash_speed = 0          # Speed of dash movement per frame
        self.dash_trail_timer = 0    # Timer for creating trail effects

    def change_character(self, new_character):
        """Change the current character and update attributes accordingly."""
        # Check if the character is unlocked in config
        if new_character == "bear" and not config.bear_unlocked:

            return False
        elif new_character == "rabbit" and not config.rabbit_unlocked:

            return False
        elif new_character == "monkey" and not config.monkey_unlocked:

            return False
        elif new_character == "fox" and not config.fox_unlocked:

            return False
        elif new_character == "fancy_rabbit" and not config.fancy_rabbit_unlocked:
            return False
        
        # If the character is unlocked and in the available list, proceed with the change
        if new_character in self.available_characters:
            self.character = new_character


            # Update character-specific attributes
            self.jump_speed = self.character_attributes[self.character]["jump_speed"]
            self.can_shoot = self.character_attributes[self.character].get("can_shoot", False)
            self.can_melee = self.character_attributes[self.character].get("can_melee", False)
            self.speed = self.character_attributes[self.character]["speed"]

            return True
        return False

    def check_collision(self, x, y, cubes):
        """Check if the player would collide with any collidable cubes at a given position."""
        for cube in cubes:
            if cube.collidable and (
                x + self.collision_offset_x + self.collision_width > cube.x and
                x + self.collision_offset_x < cube.x + cube.width and
                y + self.collision_offset_y + self.collision_height > cube.y and
                y + self.collision_offset_y < cube.y + cube.height
            ):
                return (True, cube)  # Collision detected
        return (False, None)  # No collision

    def check_inside_cube(self, cubes):
        """Check if player is inside any cube and determine where to place them."""
        for cube in cubes:
            if cube.collidable:
                player_hitbox_left = self.x + self.collision_offset_x
                player_hitbox_right = player_hitbox_left + self.collision_width
                player_hitbox_top = self.y + self.collision_offset_y + self.collision_height
                player_hitbox_bottom = self.y + self.collision_offset_y

                # Check if player is inside cube
                if (player_hitbox_right > cube.x and
                    player_hitbox_left < cube.x + cube.width and
                    player_hitbox_top > cube.y and
                    player_hitbox_bottom < cube.y + cube.height):
                    # If player is falling and closer to the top of the cube, place them on top
                    if self.velocity_y < 0 and abs(player_hitbox_bottom - cube.y - cube.height) < abs(player_hitbox_top - cube.y):
                        return (cube, "top")
                    # Otherwise place them below
                    return (cube, "bottom")
        return None

    def update(self, cubes):


        keys = pygame.key.get_pressed()
        self.state = "idle"
        self.shooting = False
        if config.stage == 1:
            self.jump_speed = 0.22
        elif config.stage == 2:
            self.jump_speed = 0.27
        if config.stage == 2:
            if config.leap_of_faith_triggered and self.x > 47:
                config.stageend(config.stage)

            if self.x <= - 36 or self.x >= 31 :
                if self.y <= 1:
                    self.x = 1
                    self.y = 1


        if self.melee_cooldown > 0:
            self.melee_cooldown -= 1


        if (
            keys[pygame.K_f]
            and self.character == "bear"
            and self.character_attributes["bear"]["can_melee"]
            and self.melee_cooldown == 0
        ):

            pygame.mixer.Sound(config.claw_sound).play()
            

            self.state = "attack"
            
            explosion_x = self.x + (self.direction * 1.0)
            explosion_y = self.y + 0.5
            config.explosions.append(
                Explosion(
                    explosion_x,
                    explosion_y - self.height / 2,
                    self.z,
                    config.claw_sprites,
                )
            )


            melee_range = 1.5
            melee_x = self.x + (self.direction * melee_range)
            for enemy in config.enemies:

                if (
                    abs(melee_x - enemy.x) < melee_range
                    and abs(self.y - enemy.y) < 1.5
                ) or (

                    self.x + self.collision_offset_x + self.collision_width > enemy.x
                    and self.x + self.collision_offset_x < enemy.x + enemy.width
                    and self.y + self.collision_offset_y + self.collision_height > enemy.y
                    and self.y + self.collision_offset_y < enemy.y + enemy.height
                ):
                    enemy.take_damage(config.enemies, cubes)


            if self.character == "bear" and self.can_melee:
                melee_x = self.x + (1.5 if self.direction > 0 else -1.5) 
                
                
                pygame.mixer.Sound(config.claw_sound).play()
                
                
                claw_effect = Explosion(
                    melee_x,
                    self.y,
                    self.z,
                    config.claw_sprites,  
                )
                config.explosions.append(claw_effect)
                
             
                for cube in config.breakCubes[:]:
                    if (
                        abs(melee_x - cube.x) < 1.5
                        and abs(self.y - cube.y) < 1.5
                    ):
                        
                        cube_explosion = Explosion(
                            cube.x,
                            cube.y,
                            cube.z,
                            config.explosion_sprites,  
                        )
                        config.explosions.append(cube_explosion)
                        
                        
                        config.breakCubes.remove(cube)
                        
                        
                        if len(config.breakCubes) == 0:
                            
                            for front_cube in config.breakFront[:]:
                                
                                front_explosion = Explosion(
                                    front_cube.x,
                                    front_cube.y,
                                    front_cube.z,
                                    config.explosion_sprites,  
                                )
                                config.explosions.append(front_explosion)
                            
                           
                            config.breakFront.clear()

                self.melee_cooldown = self.melee_cooldown_time

           
            if self.character == "bear" and self.can_melee and self.melee_cooldown == 0:
                melee_x = self.x + (1 if self.direction > 0 else -1)
                
                config.explosions.append(
                    Explosion(
                        melee_x,
                        self.y,
                        self.z,
                        config.claw_sprites,
                    )
                )
                self.melee_cooldown = self.melee_cooldown_time

            
            self.melee_cooldown = self.melee_cooldown_time

        
        if self.state == "attack" and self.melee_cooldown < self.melee_cooldown_time - 15:
            self.state = "idle"  

            

       
        if keys[pygame.K_1]:
            if self.character != "rabbit" and self.change_character("rabbit"):
                transform_animation = Explosion(
                    self.x, 
                    self.y,  
                    self.z,
                    config.transform_sprites,
                )
                config.transform.append(transform_animation)

        if keys[pygame.K_2]:
            
            if self.character != "monkey" and self.change_character("monkey"):
                transform_animation = Explosion(
                    self.x,  
                    self.y,  
                    self.z,
                    config.transform_sprites,
                )
                config.transform.append(transform_animation)

        if keys[pygame.K_3]:
           
            if self.character != "fox" and self.change_character("fox"):
                transform_animation = Explosion(
                    self.x,  
                    self.y,  
                    self.z,
                    config.transform_sprites,
                )
                config.transform.append(transform_animation)

        if keys[pygame.K_4]:
            if self.character != "bear" and self.change_character("bear"):
                transform_animation = Explosion(
                    self.x,  
                    self.y,  
                    self.z,
                    config.transform_sprites,
                )
                config.transform.append(transform_animation)
        


        if keys[pygame.K_f] and self.weapon_equipped and self.can_shoot:
            self.shooting = True
            self.state = "shoot"

        if self.character == "fox" and keys[pygame.K_LSHIFT] and self.dash_cooldown == 0 and self.dash_progress == 0:
            config.poof_sound.play()
            dash_distance = self.character_attributes["fox"]["dash_power"] * self.direction
            
            if not self.check_collision(self.x + dash_distance, self.y, cubes)[0]:
                config.explosions.append(Explosion(self.x, self.y - self.height/2, self.z, config.explosion_sprites))
                
                self.dash_target_x = self.x + dash_distance
                self.dash_progress = 1  
                self.dash_speed = dash_distance / self.dash_duration
                self.dash_cooldown = self.character_attributes["fox"]["dash_cooldown"]
                self.dashing = True
                self.state = "jump"  

        if self.dash_progress > 0 and self.dash_progress < self.dash_duration:
            move_amount = self.dash_speed
            new_x = self.x + move_amount
            
            if self.check_collision(new_x, self.y, cubes)[0]:
                self.dash_progress = 0
                self.dashing = False
            else:
                self.x = new_x
                self.dash_progress += 1
                
                self.dash_trail_timer += 1
                if self.dash_trail_timer >= 2:  
                    config.explosions.append(Explosion(self.x - (self.direction * 0.5), 
                                                      self.y - self.height/2, 
                                                      self.z, 
                                                      config.explosion_sprites))  
                    self.dash_trail_timer = 0
                
        elif self.dash_progress == self.dash_duration:
            self.dash_progress = 0
            self.dashing = False
            self.dash_trail_timer = 0

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if self.dashing:
            self.dashing = False

        new_x = self.x

        if keys[pygame.K_a]:
            if not self.check_collision(self.x - self.speed, self.y, cubes)[0]:
                new_x -= self.speed
            self.direction = -1
            self.state = "run"
        if keys[pygame.K_d]:
            if not self.check_collision(self.x + self.speed, self.y, cubes)[0]:
                new_x += self.speed
            self.direction = 1
            self.state = "run"

        if self.on_ground:
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                self.velocity_y = self.jump_speed  
                self.on_ground = False
                self.state = "jump"

        self.velocity_y -= 0.01  # Gravity effect (pulling downward)
        new_y = self.y + self.velocity_y

        collision, cube = self.check_collision(self.x, new_y, cubes)
        if collision:
            if self.velocity_y < 0:  
                
                self.y = cube.y + cube.height - self.collision_offset_y
                self.velocity_y = 0
                self.on_ground = True
            elif self.velocity_y > 0:  
                self.y = cube.y - self.collision_height - self.collision_offset_y
                self.velocity_y = 0
        else:
            self.on_ground = False
            self.y = new_y  

        self.x = new_x

        if not self.on_ground and not self.shooting:
            self.state = "jump"

        for cube in cubes:
            if cube.on_touch:
                player_hitbox = (
                    self.x + self.collision_offset_x,
                    self.y + self.collision_offset_y,
                    self.x + self.collision_offset_x + self.collision_width,
                    self.y + self.collision_offset_y + self.collision_height,
                )
                cube_hitbox = (
                    cube.x,
                    cube.y,
                    cube.x + cube.width,
                    cube.y + cube.height,
                )
                if (player_hitbox[2] > cube_hitbox[0] and
                    player_hitbox[0] < cube_hitbox[2] and
                    player_hitbox[3] > cube_hitbox[1] and
                    player_hitbox[1] < cube_hitbox[3]):
                    cube.on_touch()

        self.animation_frame = (self.animation_frame + 1) % 60

    def render(self):
        sprite = None  
        
        if self.weapon_equipped:
            if self.state == "idle":
                weapon_sprites = config.weapon_idle_sprites
                if weapon_sprites and len(weapon_sprites) > 0:
                    sprite = weapon_sprites[self.animation_frame // 10 % len(weapon_sprites)]
        else:
            try:
                character_sprites = None
                
                if self.state == "idle" and self.character in config.animal_sprites:
                    character_sprites = config.animal_sprites[self.character]["idle"]
                elif self.state == "run" and self.character in config.animal_sprites:
                    character_sprites = config.animal_sprites[self.character]["run"]
                elif self.state == "jump" and self.character in config.animal_sprites:
                    character_sprites = config.animal_sprites[self.character]["jump"]
                elif self.state == "attack" and self.character in config.animal_sprites and "attack" in config.animal_sprites[self.character]:
                    character_sprites = config.animal_sprites[self.character]["attack"]
                elif self.state == "idle" and self.character == "fancy_rabbit" and "idle" in config.animal_sprites["fancy_rabbit"]:
                    character_sprites = config.animal_sprites["fancy_rabbit"]["idle"]
                elif self.state == "run" and self.character == "fancy_rabbit" and "run" in config.animal_sprites["fancy_rabbit"]:
                    character_sprites = config.animal_sprites["fancy_rabbit"]["run"]
                elif self.state == "jump" and self.character == "fancy_rabbit" and "jump" in config.animal_sprites["fancy_rabbit"]:
                    character_sprites = config.animal_sprites["fancy_rabbit"]["jump"]
                elif self.state == "attack" and self.character == "fancy_rabbit" and "attack" in config.animal_sprites["fancy_rabbit"]:
                    character_sprites = config.animal_sprites["fancy_rabbit"]["attack"]
                    
                if character_sprites and len(character_sprites) > 0:
                    sprite = character_sprites[self.animation_frame // 10 % len(character_sprites)]
            except (KeyError, IndexError, ZeroDivisionError) as e:
                print(f"Error loading character sprite: {e}")
                
            if sprite is None:
                if self.state == "idle" and len(config.idle_sprites) > 0:
                    sprite = config.idle_sprites[self.animation_frame // 10 % len(config.idle_sprites)]
                elif self.state == "run" and len(config.run_sprites) > 0:
                    sprite = config.run_sprites[self.animation_frame // 10 % len(config.run_sprites)]
                elif self.state == "jump" and len(config.jump_sprites) > 0:
                    sprite = config.jump_sprites[self.animation_frame // 10 % len(config.jump_sprites)]

        if sprite is None and len(config.idle_sprites) > 0:
            sprite = config.idle_sprites[0]

        if sprite is None:
            return

        if self.direction == -1:
            sprite = pygame.transform.flip(sprite, True, False)

        texture_data = pygame.image.tostring(sprite, "RGBA", True)
        width, height = sprite.get_size()
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4f(1, 1, 1, 1)  
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(1, 0); glVertex3f(self.width, 0, 0)
        glTexCoord2f(1, 1); glVertex3f(self.width, self.height, 0)
        glTexCoord2f(0, 1); glVertex3f(0, self.height, 0)
        glEnd()

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)

        glPopMatrix()

    def render_hitbox(self):
        if not config.debug:
            return
        glPushMatrix()
        glTranslatef(self.x + self.collision_offset_x, self.y + self.collision_offset_y, self.z)
        glColor3f(0, 1, 0)  
        glBegin(GL_LINE_LOOP)
        glVertex3f(0, 0, 0)
        glVertex3f(self.collision_width, 0, 0)
        glVertex3f(self.collision_width, self.collision_height, 0)
        glVertex3f(0, self.collision_height, 0)
        glEnd()
        glPopMatrix()

    def handle_death(self):
        """Handle the player's death."""
        if self.health <= 0:
            print("Player has died!")
            pygame.quit()
            quit()

class Enemy:
    def __init__(self, x, y, z, width, height, texture_path=None, speed=0.05, gravity=0.01, 
                 radius=10, damage=10, health=1, collidable=True, debug=False, 
                 sprite_set="default", behavior="follow", patrol_min_x=None, patrol_max_x=None):
        """
        An enemy with different behavior patterns.
        :param behavior: "static" (stand still), "follow" (chase player), or "patrol" (move between boundaries)
        :param patrol_min_x: Minimum x coordinate for patrol behavior
        :param patrol_max_x: Maximum x coordinate for patrol behavior
        """
        self.x, self.y, self.z = x, y, z
        self.width, self.height = width, height
        self.health = health
        self.damage = damage
        self.speed = speed
        self.gravity = gravity
        self.velocity_y = 0
        self.on_ground = False
        self.radius = radius
        self.attack_cooldown = 0
        self.stun_timer = 0
        self.collidable = collidable
        self.debug = debug
        self.direction = 1  
        
        self.behavior = behavior  
        self.patrol_min_x = patrol_min_x if patrol_min_x is not None else x - 5
        self.patrol_max_x = patrol_max_x if patrol_max_x is not None else x + 5
        
        self.sprite_set = sprite_set  
        
        self.animation_frame = 0
        self.state = "idle"  
        
        if sprite_set != "default" and sprite_set in config.animal_sprites:
            self.use_character_sprites = True
        else:
            self.use_character_sprites = False
            
        if texture_path and not self.use_character_sprites:
            if os.path.isdir(texture_path):
                self.idle_sprites = load_sprites(os.path.join(texture_path, "idle"))
                self.run_sprites = load_sprites(os.path.join(texture_path, "run"))
                self.attack_sprites = load_sprites(os.path.join(texture_path, "attack"))
            else:
                texture = load_texture(texture_path)
                self.texture = texture
                self.idle_sprites = self.run_sprites = self.attack_sprites = None
        else:
            self.texture = load_texture("assets/enemy_default.png")
            self.idle_sprites = self.run_sprites = self.attack_sprites = None

    def update(self, player, cubes, delta_time):
        """Update the enemy's position based on its behavior type."""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time
            
        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            return
            
        self.velocity_y -= self.gravity
        new_y = self.y + self.velocity_y

        collision, cube, collision_type = self.check_ground_collision(new_y, cubes)
        if collision:
            if collision_type == "top" or (self.velocity_y < 0 and collision_type == "inside"):
                self.y = cube.y + cube.height + 0.01
                self.velocity_y = 0
                self.on_ground = True
            elif collision_type == "bottom" or (self.velocity_y > 0 and collision_type == "inside"):
                self.y = cube.y - self.height
                self.velocity_y = 0
            elif collision_type == "inside":
                top_penetration = (cube.y + cube.height) - self.y
                bottom_penetration = self.y + self.height - cube.y
                
                if top_penetration < bottom_penetration:
                    self.y = cube.y + cube.height + 0.01  
                else:
                    self.y = cube.y - self.height  
                self.velocity_y = 0
        else:
            self.on_ground = False
            self.y = new_y  

        if self.behavior == "static":
            self.state = "idle"
            
        elif self.behavior == "follow":
            distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
            if distance <= self.radius:
                self.state = "run"
                
                self.direction = 1 if player.x > self.x else -1
                
                direction_x = player.x - self.x
                if abs(direction_x) > 0.1:  
                    direction_x = direction_x / abs(direction_x)  
                    new_x = self.x + direction_x * self.speed

                    if not self.check_horizontal_collision(new_x, cubes):
                        self.x = new_x
                        
                if distance < 1.5:
                    self.state = "attack"
            else:
                self.state = "idle"
                
        elif self.behavior == "patrol":
            self.state = "run"
            
            new_x = self.x + (self.direction * self.speed)
            
            if new_x <= self.patrol_min_x:
                self.direction = 1  
                new_x = self.patrol_min_x + self.speed  
            elif new_x + self.width >= self.patrol_max_x:
                self.direction = -1  
                new_x = self.patrol_max_x - self.width - self.speed  
                
            if not self.check_horizontal_collision(new_x, cubes):
                self.x = new_x
            else:
                self.direction *= -1

        self.animation_frame += 1

    def check_horizontal_collision(self, new_x, cubes):
        """Check for horizontal collisions with cubes."""
        for cube in cubes:
            if cube.collidable and (
                new_x + self.width > cube.x and
                new_x < cube.x + cube.width and
                self.y + self.height > cube.y and
                self.y < cube.y + cube.height
            ):
                return True  
        return False  

    def render(self):
        """Render the enemy with sprites based on its current state."""
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glPushMatrix()
        
        glTranslatef(self.x, self.y + self.height/2, self.z)  
        
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        sprite = None
        
        if self.use_character_sprites and self.sprite_set in config.animal_sprites:
            char_sprites = config.animal_sprites[self.sprite_set]
            
            if self.state == "idle" and "idle" in char_sprites and len(char_sprites["idle"]) > 0:
                sprite = char_sprites["idle"][self.animation_frame // 10 % len(char_sprites["idle"])]
            elif self.state == "run" and "run" in char_sprites and len(char_sprites["run"]) > 0:
                sprite = char_sprites["run"][self.animation_frame // 10 % len(char_sprites["run"])]
            elif self.state == "attack" and "jump" in char_sprites and len(char_sprites["jump"]) > 0:
                sprite = char_sprites["jump"][self.animation_frame // 10 % len(char_sprites["jump"])]
        else:
            if self.state == "idle" and self.idle_sprites and len(self.idle_sprites) > 0:
                sprite = self.idle_sprites[self.animation_frame // 10 % len(self.idle_sprites)]
            elif self.state == "run" and self.run_sprites and len(self.run_sprites) > 0:
                sprite = self.run_sprites[self.animation_frame // 10 % len(self.run_sprites)]
            elif self.state == "attack" and self.attack_sprites and len(self.attack_sprites) > 0:
                sprite = self.attack_sprites[self.animation_frame // 10 % len(self.attack_sprites)]
        
        if sprite is not None:
            texture_data = pygame.image.tostring(sprite, "RGBA", True)
            width, height = sprite.get_size()
            
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        else:
            if not hasattr(self, 'texture') or self.texture is None:
                texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texture_id)
                
                pixels = bytes([255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255])  
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 2, 2, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                
                self.texture = texture_id
            else:
                glBindTexture(GL_TEXTURE_2D, self.texture)
        
        scale_factor = 1.0  
        glScalef(self.width * scale_factor, self.height * scale_factor, 1.0)
        
        if self.direction < 0:
            glScalef(-1, 1, 1)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0)
        glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0)
        glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0)
        glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, 0)
        glEnd()
        
        glPopMatrix()
        glPopAttrib()

    def render_hitbox(self):
        if self.debug:
            glPushAttrib(GL_ALL_ATTRIB_BITS)
            glPushMatrix()
            glDisable(GL_TEXTURE_2D)
            
            glColor4f(1.0, 0.0, 0.0, 0.5)  
            glBegin(GL_LINE_LOOP)
            glVertex3f(self.x, self.y, self.z)
            glVertex3f(self.x + self.width, self.y, self.z)
            glVertex3f(self.x + self.width, self.y + self.height, self.z)
            glVertex3f(self.x, self.y + self.height, self.z)
            glEnd()
            
            
            glColor4f(0.0, 1.0, 0.0, 1.0)  # Green
            glBegin(GL_LINES)
            glVertex3f(self.x + self.width/2, self.y, self.z)
            glVertex3f(self.x + self.width/2, self.y - 0.2, self.z)  
            glEnd()
            
            glPopMatrix()
            glPopAttrib()

    def deal_damage(self, player):
        """Deal damage to the player if attack cooldown allows."""
        if self.attack_cooldown <= 0:
            player.health -= self.damage

            self.attack_cooldown = 1.0  
            
            if player.health <= 0:

                player.handle_death()

    def take_damage(self, enemies, cubes):
        """Reduce the enemy's health when hit and remove if health reaches 0."""
        self.health -= 1
        self.stun_timer = 0.3  
        print(f"Enemy hit! Remaining health: {self.health}")
        
        if self.health <= 0:
            print("Enemy defeated!")
            if self in enemies:
                enemies.remove(self)
            if self in cubes:
                cubes.remove(self)
            
            config.explosions.append(
                Explosion(
                    self.x,
                    self.y,
                    self.z,
                    config.explosion_sprites,
                )
            )

    def check_ground_collision(self, new_y, cubes):
        """Check if the enemy would collide with any collidable cubes at a given position."""
       
        enemy_bottom = new_y 
        
        for cube in cubes:
            if cube.collidable and (
                
                self.x + self.width > cube.x and
                self.x < cube.x + cube.width
            ):
                if (enemy_bottom <= cube.y + cube.height + 0.1 and  
                    enemy_bottom >= cube.y + cube.height - 0.1):    
                    return (True, cube, "top")  
                    
                elif (enemy_bottom + self.height >= cube.y - 0.1 and
                      enemy_bottom + self.height <= cube.y + 0.1):
                    return (True, cube, "bottom")  
                    
                elif (enemy_bottom < cube.y + cube.height and
                      enemy_bottom + self.height > cube.y):
                    return (True, cube, "inside")  
                    
        return (False, None, None)  

class Projectile:#this
    def __init__(self, x, y, z, direction, speed=0.2, size=0.5, facing_right=True):
        """
        Initialize a projectile.
        :param x, y, z: Starting position of the projectile.
        :param direction: Direction of the projectile (1 for right, -1 for left).
        :param speed: Speed of the projectile.
        :param size: Size of the projectile (controls both width and height)
        """
        self.x, self.y, self.z = x, y, z
        self.width, self.height = size, size  
        self.direction = direction
        self.speed = speed
        self.active = True  
        self.facing_right = facing_right

    def update(self, cubes, player,enemies):
        """
        Update the position of the projectile.
        """
        
        if self.active:
            self.x += self.speed if self.facing_right else -self.speed

            if self.x  >= player.x + 10 or self.x <= player.x - 10:  
                self.active = False
                config.projectiles.remove(self)
            self.check_collision(cubes, enemies)
  
    def check_collision(self, cubes, enemies):
        """
        Check if the projectile collides with any cube or enemy.
        :param cubes: List of cubes in the game.
        :param enemies: List of enemies in the game.
        """
        for enemy in enemies:
            if (self.x + self.width > enemy.x and
                self.x < enemy.x + enemy.width and
                self.y + self.height > enemy.y and
                self.y < enemy.y + enemy.height):
                self.active = False
                try:
                    config.projectiles.remove(self)  
                except ValueError:
                    pass
                enemy.take_damage(enemies, cubes)  
                return  

        for cube in cubes:
            if cube.collidable:  
                if (self.x + self.width > cube.x and
                    self.x < cube.x + cube.width and
                    self.y + self.height > cube.y and
                    self.y < cube.y + cube.height):
                    self.active = False
                    try:
                        config.projectiles.remove(self)  
                    except ValueError:
                        pass
                    return  

    def render(self):
        """
        Render the projectile using the bullet sprite.
        """
        if self.active:
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)

            glBindTexture(GL_TEXTURE_2D, config.projectile_sprite)

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            glColor4f(1, 1, 1, 1)  
            glBegin(GL_QUADS)
            if self.facing_right:
                glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
                glTexCoord2f(1, 0); glVertex3f(self.width, 0, 0)
                glTexCoord2f(1, 1); glVertex3f(self.width, self.height, 0)
                glTexCoord2f(0, 1); glVertex3f(0, self.height, 0)
            else:  
                glTexCoord2f(1, 0); glVertex3f(0, 0, 0)
                glTexCoord2f(0, 0); glVertex3f(self.width, 0, 0)
                glTexCoord2f(0, 1); glVertex3f(self.width, self.height, 0)
                glTexCoord2f(1, 1); glVertex3f(0, self.height, 0)
            glEnd()

            glDisable(GL_BLEND)  
            glPopMatrix()