import pygame
from OpenGL.GL import *

def load_texture(filepath):
    """
    Load a texture from a file and return the texture ID.
    """
    try:
        surface = pygame.image.load(filepath)
        tex_data = pygame.image.tostring(surface, "RGBA", True)
        width, height = surface.get_size()
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, 
                    GL_UNSIGNED_BYTE, tex_data)
        
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        return texture_id
    except Exception as e:
        print(f"Error loading texture {filepath}: {e}")
        # Return a default texture or None
        return None