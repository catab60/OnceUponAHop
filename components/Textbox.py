from components.init import *
from components.config import *
import pygame

class Textbox:
    def __init__(self, text, width, height, font_path, font_size, x=0, y=0, z=0):
        """
        Initialize the Textbox.
        :param text: The text to display.
        :param width: The width of the textbox.
        :param height: The height of the textbox.
        :param font_path: Path to the font file.
        :param font_size: Size of the font.
        :param x, y, z: Position of the textbox.
        """
        self.text = text
        self.width = width
        self.height = height
        self.font = pygame.font.Font(font_path, font_size)
        self.x, self.y, self.z = x, y, z
        self.texture = None
        self.update_texture()

    def update_texture(self):
        """
        Update the texture for the text, handling multiple lines.
        """
        lines = self.text.split("\n")  # Split text into lines
        line_surfaces = [self.font.render(line, True, (255, 255, 255, 255)) for line in lines]
        
        # Calculate total height and maximum width
        total_height = sum(surface.get_height() for surface in line_surfaces)
        max_width = max(surface.get_width() for surface in line_surfaces)

        # Create a surface to combine all lines
        combined_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        y_offset = 0
        for surface in line_surfaces:
            combined_surface.blit(surface, (0, y_offset))
            y_offset += surface.get_height()

        texture_data = pygame.image.tostring(combined_surface, "RGBA", True)
        width, height = combined_surface.get_size()

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def render(self, target_x, target_y, target_z):
        """
        Render the textbox above the target (player or cube).
        :param target_x: X position of the target.
        :param target_y: Y position of the target.
        :param target_z: Z position of the target.
        """
        glPushAttrib(GL_ENABLE_BIT)
        glPushMatrix()
        glTranslatef(target_x, target_y + self.height + 0.5, target_z)  # Position above the target

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw background quad (black with 0.5 alpha, same size as the text box)
        glDisable(GL_TEXTURE_2D)  # Disable texture for the background
        glColor4f(0, 0, 0, 0.5)  # Black color with 50% opacity
        glBegin(GL_QUADS)
        glVertex3f(-self.width / 2, 0, -0.01)  # Same size as the text quad
        glVertex3f(self.width / 2, 0, -0.01)
        glVertex3f(self.width / 2, self.height, -0.01)
        glVertex3f(-self.width / 2, self.height, -0.01)
        glEnd()

        # Draw text quad
        glEnable(GL_TEXTURE_2D)  # Re-enable texture for the text
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColor4f(1, 1, 1, 1)  # White color with full opacity
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-self.width / 2, 0, 0)
        glTexCoord2f(1, 0); glVertex3f(self.width / 2, 0, 0)
        glTexCoord2f(1, 1); glVertex3f(self.width / 2, self.height, 0)
        glTexCoord2f(0, 1); glVertex3f(-self.width / 2, self.height, 0)
        glEnd()

        glDisable(GL_BLEND)
        glPopMatrix()
        glPopAttrib()

    def set_text(self, new_text, width=None, height=None):
        """
        Update the text and refresh the texture.
        :param new_text: The new text to display.
        """
        self.text = new_text
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        self.update_texture()

