import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import os
import math
import random
import threading

pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

glutInit()

glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)  # Enable blending
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blending function
glClearColor(0.1, 0.1, 0.1, 1) 