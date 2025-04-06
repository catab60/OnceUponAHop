from components.init import *
from components.functions import *
import math

class NPC:
    def __init__(self, x, y, z, width, height, idle_sprites, key, command, interaction_radius=1.5, debug=False, hint_image_path=None, hint_width=1.0, hint_height=1.0):
        """
        A non-playable character (NPC) that runs a command when the player presses a specific key while within a certain radius.
        :param x, y, z: Position of the NPC.
        :param width, height: Dimensions of the NPC.
        :param idle_sprites: List of sprites for the idle animation.
        :param key: The key that needs to be pressed to execute the command.
        :param command: The function to execute when the key is pressed.
        :param interaction_radius: The radius within which the player can interact with the NPC.
        :param debug: Whether to show the interaction radius range.
        :param hint_image_path: Path to the image to display as the hint.
        :param hint_width: Width of the hint image.
        :param hint_height: Height of the hint image.
        """
        self.x, self.y, self.z = x, y, z
        self.width, self.height = width, height
        self.idle_sprites = idle_sprites
        self.key = key
        self.command = command
        self.interaction_radius = interaction_radius
        self.debug = debug
        self.hint_texture = load_texture(hint_image_path) if hint_image_path else None
        self.hint_texture_path = hint_image_path  # Store the hint image path
        self.hint_animation_time = 0  # Time variable for sinusoidal movement
        self.hint_width = hint_width
        self.hint_height = hint_height
        self.animation_frame = 0  # Frame counter for idle animation
        self.interacted = False  # Flag to track if player has interacted with this NPC

    def check_key_press(self, keys, player):
        """
        Check if the player is within the interaction radius and the specified key is pressed.
        :param keys: The current state of all keys.
        :param player: The player object.
        """
        # Calculate the center of the NPC
        npc_center_x = self.x + self.width / 2
        npc_center_y = self.y + self.height / 2

        # Calculate the distance from the player's center to the NPC's center
        player_center_x = player.x + player.collision_offset_x + player.collision_width / 2
        player_center_y = player.y + player.collision_offset_y + player.collision_height / 2
        distance = ((player_center_x - npc_center_x) ** 2 + (player_center_y - npc_center_y) ** 2) ** 0.5

        # Check if the player is within the interaction radius and the key is pressed
        if distance <= self.interaction_radius and keys[self.key]:
            self.interacted = True  # Mark as interacted
            self.command()

    def render_idle_animation(self):
        """
        Render the idle animation for the NPC.
        """
        sprite = self.idle_sprites[self.animation_frame // 10 % len(self.idle_sprites)]  # Cycle through sprites
        texture_data = pygame.image.tostring(sprite, "RGBA", True)
        width, height = sprite.get_size()

        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4f(1, 1, 1, 1)  # Full opacity
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(1, 0); glVertex3f(self.width, 0, 0)
        glTexCoord2f(1, 1); glVertex3f(self.width, self.height, 0)
        glTexCoord2f(0, 1); glVertex3f(0, self.height, 0)
        glEnd()

        glDisable(GL_BLEND)
        glPopMatrix()

        # Increment animation frame
        self.animation_frame = (self.animation_frame + 1) % (len(self.idle_sprites) * 10)

    def render_key_hint(self, player):
        """
        Render the image hint above the NPC if the player is within the interaction radius.
        :param player: The player object.
        """
        # Only show the hint if not yet interacted
        if self.interacted:
            return

        # Calculate the center of the NPC
        npc_center_x = self.x + self.width / 2
        npc_center_y = self.y + self.height / 2

        # Calculate the distance from the player's center to the NPC's center
        player_center_x = player.x + player.collision_offset_x + player.collision_width / 2
        player_center_y = player.y + player.collision_offset_y + player.collision_height / 2
        distance = ((player_center_x - npc_center_x) ** 2 + (player_center_y - npc_center_y) ** 2) ** 0.5

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

    def hide_hint(self):
        """
        Hide the hint image above the NPC.
        """
        self.hint_texture = None

    def show_hint(self, hint_image_path=None):
        """
        Show the hint image above the NPC by loading the specified image.
        If no path is provided, reload the stored hint image path.
        :param hint_image_path: Path to the image to display as the hint.
        """
        if hint_image_path:
            self.hint_texture_path = hint_image_path  # Update the stored path
        if self.hint_texture_path:
            self.hint_texture = load_texture(self.hint_texture_path)
