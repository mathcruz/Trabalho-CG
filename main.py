# -*- coding: utf-8 -*-
# Import a library of functions called 'pygame'
import pygame
import math
from object3D import object3D
from object2D import object2D
from colors import *

# Initialize the game engine
pygame.init()

ambient_light_color = (WHITE)
ambient_light_intensity = 0.2

# Iniciando os valores do SRD (Sistema de Referencia do Display)
SRD = [800, 600]
screen = pygame.display.set_mode(SRD)

limiteMin = [0,0]       #[xMin, yMin]
limiteMax = [100,100]   #[xMax. yMax]

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

class dois(object2D):
	def __init__(self, screen, cor):
		pontos = [[0,0], [0,2], [6,7], [2,7], [1,6], [0,7], [0,8], [1,9], [7,9], [8,8], [8,6], [3,2], [8,2], [8,0]]
		super(dois, self).__init__(screen, pontos, cor)

fig = dois(screen,[255,140,0])
quadrado = object2D(screen, [[0,0],[0,10],[10,10],[10,0], [0, 0]], [132, 42, 181])
q3d = object3D.convert3d(quadrado)
q3d.rotate_x(2.09)
q3d.translate(50, 50, 5)
#fig.translate(50, 50)
fig2 = object3D(screen, [[[0,0,0],[10,0,0],[10,0,10],[0,0,10]],[[10,0,10],[10,0,0],[10,10,0],[10,10,10]],[[0,10,10],[10,10,10],[10,10,0],[0,10,0]],[[0,0,10],[0,10,10],[0,10,0],[0,0,0]],[[0,0,0],[0,10,0],[10,10,0],[10,0,0]],[[0,0,10],[10,0,10],[10,10,10],[0,10,10]]], BLUE)
teste = object3D(screen, [[[0,0,0],[10,0,0],[10,0,10],[0,0,10]],[[10,0,10],[10,0,0],[10,10,0],[10,10,10]],[[0,10,10],[10,10,10],[10,10,0],[0,10,0]],[[0,0,10],[0,10,10],[0,10,0],[0,0,0]],[[0,0,0],[0,10,0],[10,10,0],[10,0,0]],[[0,0,10],[10,0,10],[10,10,10],[0,10,10]]], GREEN)
fig2.rotate_x(2.09)
fig2.translate(80, 80, 2)
teste.translate(40, 80, 2)
fig2.draw()
fig3 = object3D.convert3d(fig)
#fig3.rotate_y(0.5)
#fig3.apl_rotate_x(0.5)
fig3.translate(10, 10, 2)
#fig2.rotate_y(1)
#fig.animate(200,200,0)
state = 0
max_state = 120
#fig.animate(100,100,0)
while not done:

    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    # This draws a triangle using the polygon command
    if(state < max_state):
        state += 1
        fig2.animate(2*math.pi, max_state)
        fig3.animate(math.pi, max_state)
        q3d.animate(math.pi, max_state)
        teste.animate(math.pi, max_state)
    else:
        state = 0
    fig.draw()
    fig2.draw_shading([200, 200, -100])
    fig3.draw_shading([200, 200, -100])
    q3d.draw_shading([200, 200, -100])
    teste.draw_shading([200, 200, -100])
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
