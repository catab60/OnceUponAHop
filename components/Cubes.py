from components.init import *
import components.config as config
from components.functions import *
from components.utils import load_texture

class Cube:
    def __init__(self, x, y, z, width, height, length, textures, collidable=True, on_touch=None, id=None, debug=False):
        """
        :param x, y, z: Position of the cube.
        :param width, height, length: Dimensions of the cube.
        :param textures: Dictionary of textures for the cube faces.
        :param collidable: Whether the cube should block the player.
        :param on_touch: Function to execute when the player touches the cube.
        """
        self.id = id
        self.x, self.y, self.z = x, y, z
        self.width, self.height, self.length = width, height, length
        self.textures = textures  # Dictionary with keys: front, left, right, top, bottom
        self.collidable = collidable  # Determines if the cube should collide with the player
        self.on_touch = on_touch  # Command to execute when touched
        self.debug = debug  # Add debug attribute

    def render(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        # Reset color to white for textures
        glColor3f(1, 1, 1)

        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Front face
        if self.textures.get("front"):
            glBindTexture(GL_TEXTURE_2D, self.textures["front"])
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
            glTexCoord2f(self.width, 0); glVertex3f(self.width, 0, 0)
            glTexCoord2f(self.width, self.height); glVertex3f(self.width, self.height, 0)
            glTexCoord2f(0, self.height); glVertex3f(0, self.height, 0)
            glEnd()

        # Left face
        if self.textures.get("left"):
            glBindTexture(GL_TEXTURE_2D, self.textures["left"])
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
            glTexCoord2f(self.length, 0); glVertex3f(0, 0, -self.length)
            glTexCoord2f(self.length, self.height); glVertex3f(0, self.height, -self.length)
            glTexCoord2f(0, self.height); glVertex3f(0, self.height, 0)
            glEnd()

        # Right face
        if self.textures.get("right"):
            glBindTexture(GL_TEXTURE_2D, self.textures["right"])
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(self.width, 0, 0)
            glTexCoord2f(self.length, 0); glVertex3f(self.width, 0, -self.length)
            glTexCoord2f(self.length, self.height); glVertex3f(self.width, self.height, -self.length)
            glTexCoord2f(0, self.height); glVertex3f(self.width, self.height, 0)
            glEnd()

        # Top face
        if self.textures.get("top"):
            glBindTexture(GL_TEXTURE_2D, self.textures["top"])
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(0, self.height, 0)
            glTexCoord2f(self.width, 0); glVertex3f(self.width, self.height, 0)
            glTexCoord2f(self.width, self.length); glVertex3f(self.width, self.height, -self.length)
            glTexCoord2f(0, self.length); glVertex3f(0, self.height, -self.length)
            glEnd()

        # Bottom face
        if self.textures.get("bottom"):
            glBindTexture(GL_TEXTURE_2D, self.textures["bottom"])
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
            glTexCoord2f(self.width, 0); glVertex3f(self.width, 0, 0)
            glTexCoord2f(self.width, self.length); glVertex3f(self.width, 0, -self.length)
            glTexCoord2f(0, self.length); glVertex3f(0, 0, -self.length)
            glEnd()

        # Disable blending after rendering
        glDisable(GL_BLEND)

        glPopMatrix()

    def render_hitbox(self):
        if not config.debug:
            return
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1, 0, 0)  # Red color for hitbox
        glBegin(GL_LINE_LOOP)
        glVertex3f(0, 0, 0)
        glVertex3f(self.width, 0, 0)
        glVertex3f(self.width, self.height, 0)
        glVertex3f(0, self.height, 0)
        glEnd()
        glBegin(GL_LINE_LOOP)
        glVertex3f(0, 0, -self.length)
        glVertex3f(self.width, 0, -self.length)
        glVertex3f(self.width, self.height, -self.length)
        glVertex3f(0, self.height, -self.length)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, -self.length)
        glVertex3f(self.width, 0, 0)
        glVertex3f(self.width, 0, -self.length)
        glVertex3f(self.width, self.height, 0)
        glVertex3f(self.width, self.height, -self.length)
        glVertex3f(0, self.height, 0)
        glVertex3f(0, self.height, -self.length)
        glEnd()
        glPopMatrix()

class SpecialKeyCube(Cube):
    def __init__(self, x, y, z, width, height, length, textures, key, command, interaction_radius=1.5, collidable=True, debug=False, hint_image_path=None, hint_width=1.0, hint_height=1.0):
        """
        A special cube that runs a command when the player presses a specific key while within a certain radius.
        :param x, y, z: Position of the cube.
        :param width, height, length: Dimensions of the cube.
        :param textures: Dictionary of textures for the cube faces.
        :param key: The key that needs to be pressed to execute the command.
        :param command: The function to execute when the key is pressed.
        :param interaction_radius: The radius within which the player can interact with the cube.
        :param collidable: Whether the cube should block the player.
        :param debug: Whether to show the interaction radius range.
        :param hint_image_path: Path to the image to display as the hint.
        :param hint_width: Width of the hint image.
        :param hint_height: Height of the hint image.
        """
        super().__init__(x, y, z, width, height, length, textures, collidable)
        self.key = key
        self.command = command
        self.interaction_radius = interaction_radius
        self.debug = debug
        self.hint_texture = load_texture(hint_image_path) if hint_image_path else None
        self.hint_animation_time = 0  # Time variable for sinusoidal movement
        self.hint_width = hint_width
        self.hint_height = hint_height
        self.hint_texture_path = hint_image_path  # Store the hint image path
        self.interacted = False  # Flag to track if player has interacted with this cube

    def check_key_press(self, keys, player):
        """
        Check if the player is within the interaction radius and the specified key is pressed.
        :param keys: The current state of all keys.
        :param player: The player object.
        """
        # Calculate the center of the cube
        cube_center_x = self.x + self.width / 2
        cube_center_y = self.y + self.height / 2

        # Calculate the distance from the player's center to the cube's center
        player_center_x = player.x + player.collision_offset_x + player.collision_width / 2
        player_center_y = player.y + player.collision_offset_y + player.collision_height / 2
        distance = ((player_center_x - cube_center_x) ** 2 + (player_center_y - cube_center_y) ** 2) ** 0.5

        # Check if the player is within the interaction radius and the key is pressed
        if distance <= self.interaction_radius and keys[self.key]:
            self.interacted = True  # Mark as interacted
            self.command()

    def render_key_hint(self, player):
        # Only show the hint if not yet interacted
        if self.interacted:
            return
            
        # Calculate the center of the cube
        cube_center_x = self.x + self.width / 2
        cube_center_y = self.y + self.height / 2

        # Calculate the distance from the player's center to the cube's center
        player_center_x = player.x + player.collision_offset_x + player.collision_width / 2
        player_center_y = player.y + player.collision_offset_y + player.collision_height / 2
        distance = ((player_center_x - cube_center_x) ** 2 + (player_center_y - cube_center_y) ** 2) ** 0.5

        # Render the image hint if the player is within the interaction radius
        if distance <= self.interaction_radius and self.hint_texture:
            self.hint_animation_time += 0.05  # Increment time for animation (slowed down)
            offset_y = math.sin(self.hint_animation_time) * 0.1  # Sinusoidal offset for vertical movement

            glPushAttrib(GL_ENABLE_BIT)  # Save the current OpenGL state
            glPushMatrix()
            glTranslatef(self.x + self.width / 2, self.y + self.height + 0.5 + offset_y, self.z)
            glBindTexture(GL_TEXTURE_2D, self.hint_texture)
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Enable transparency
            glColor4f(1, 1, 1, 1.0)  # Set white color with full opacity
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(-self.hint_width / 2, 0, 0)
            glTexCoord2f(1, 0); glVertex3f(self.hint_width / 2, 0, 0)
            glTexCoord2f(1, 1); glVertex3f(self.hint_width / 2, self.hint_height, 0)
            glTexCoord2f(0, 1); glVertex3f(-self.hint_width / 2, self.hint_height, 0)
            glEnd()
            glDisable(GL_BLEND)  # Disable blending after rendering
            glPopMatrix()
            glPopAttrib()  # Restore the previous OpenGL state

    def render_debug_radius(self):
        """
        Render the interaction radius as a circle if debug is enabled.
        """
        if self.debug:
            glPushMatrix()
            glTranslatef(self.x + self.width / 2, self.y + self.height / 2, self.z)
            glColor4f(0, 1, 0, 0.3)  # Semi-transparent green
            glBegin(GL_LINE_LOOP)
            for angle in range(0, 360, 10):  # Draw a circle
                rad = math.radians(angle)  # Convert degrees to radians
                glVertex3f(self.interaction_radius * math.cos(rad), self.interaction_radius * math.sin(rad), 0)
            glEnd()
            glPopMatrix()

    def show_hint(self, hint_image_path):
        """
        Show the hint image above the cube by loading the specified image.
        :param hint_image_path: Path to the image to display as the hint.
        """
        self.hint_texture = load_texture(hint_image_path)


#animation class
class Explosion:
    def __init__(self, x, y, z, animation_sprites):
        """
        Initialize an explosion animation.
        :param x, y, z: Coordinates where the animation will play.
        :param animation_sprites: List of sprites for the explosion animation.
        """
        self.x = x
        self.y = y
        self.z = z
        self.animation_sprites = animation_sprites
        self.animation_frame = 0
        self.active = True

    def update(self):
        """
        Update the explosion animation frame.
        """
        if self.active:
            self.animation_frame += 1
            if self.animation_frame >= len(self.animation_sprites):
                self.active = False  # Deactivate the explosion when the animation ends

    def render(self, scale=1.0):
        """
        Render the explosion animation with optional scaling.
        :param scale: A scaling factor to make the sprite bigger (>1.0) or smaller (<1.0).
        """
        if self.active:
            sprite = self.animation_sprites[self.animation_frame]

            # Convert sprite to texture
            texture_data = pygame.image.tostring(sprite, "RGBA", True)
            width, height = sprite.get_size()
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

            # Render the sprite as a scaled 2D plane
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)

            # Enable blending for transparency
            glDisable(GL_DEPTH_TEST)  # Disable depth testing to allow transparency
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            glColor4f(1, 1, 1, 1)  # Full opacity for the sprite
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
            glTexCoord2f(1, 0); glVertex3f(scale, 0, 0)  # Scale width
            glTexCoord2f(1, 1); glVertex3f(scale, scale, 0)  # Scale width and height
            glTexCoord2f(0, 1); glVertex3f(0, scale, 0)  # Scale height
            glEnd()

            # Re-enable depth testing
            glEnable(GL_DEPTH_TEST)
            glDisable(GL_BLEND)

            glPopMatrix()


# enemy class
class Enemy(Cube):
    def __init__(self, x, y, z, width, height, length, textures, speed=0.05, gravity=0.01, radius=10, damage=10, collidable=True, debug=False, health=1):
        """
        A simple enemy that moves toward the player if within a certain radius and is affected by gravity.
        :param health: The health of the enemy (default is 2).
        """
        super().__init__(x, y, z, width, height, length, textures, collidable, debug=debug)
        self.health = health  # Enemy health
        self.damage = damage
        self.speed = speed  # Speed at which the enemy moves
        self.gravity = gravity  # Gravity affecting the enemy
        self.velocity_y = 0  # Vertical velocity
        self.on_ground = False  # Whether the enemy is on the ground
        self.radius = radius  # Detection radius for the player
        self.attack_cooldown = 0
        self.stun_timer = 0

    def update(self, player, cubes, delta_time):
        """
        Update the enemy's position to move toward the player if within radius and handle gravity.
        :param player: The player object.
        :param cubes: The list of cubes for collision detection.
        """

        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time
        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            return
        # Apply gravity
        self.velocity_y -= self.gravity  # Gravity effect (pulling downward)
        new_y = self.y + self.velocity_y

        # Vertical collision handling
        collision, cube = player.check_collision(self.x, new_y, cubes)
        if collision:
            if self.velocity_y < 0:  # Falling
                # Align the enemy precisely on top of the cube
                self.y = cube.y + cube.height
                self.velocity_y = 0
                self.on_ground = True
            elif self.velocity_y > 0:  # Hitting ceiling
                # Align the enemy precisely below the cube
                self.y = cube.y - self.height
                self.velocity_y = 0
        else:
            self.on_ground = False
            self.y = new_y  # Apply gravity if no collision

        # Check if the player is within the detection radius
        distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
        if distance <= self.radius:
            # Move toward the player on the x-axis only
            direction_x = player.x - self.x
            if abs(direction_x) > 0.1:  # Avoid jittering when very close
                direction_x = direction_x / abs(direction_x)  # Normalize direction to -1 or 1
                new_x = self.x + direction_x * self.speed

                # Check for collisions on the x-axis
                collision_x, _ = player.check_collision(new_x, self.y, cubes)
                if not collision_x:
                    self.x = new_x
                    
    def deal_damage(self, player):
        """
        Deal damage to the player.
        :param player: The player object to damage.
        """
        player.health -= self.damage
        print(f"Player hit! Remaining health: {player.health}")
        if player.health <= 0:
            print("Player has died!")
            player.handle_death()

    def take_damage(self, enemies, cubes):
        """
        Reduce the enemy's health when hit by a projectile.
        If health reaches 0, remove the enemy from the game.
        """
        self.health -= 1
        print(f"Enemy hit! Remaining health: {self.health}")
        if self.health <= 0:
            print("Enemy defeated!")
            if self in enemies:
                enemies.remove(self)  # Remove the enemy from the enemies list
            if self in cubes:
                cubes.remove(self)