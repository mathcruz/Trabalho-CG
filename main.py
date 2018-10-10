# Import a library of functions called 'pygame'
import pygame
import numpy as np
import math

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [1000, 1000]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

class dois():
	def __init__(self):
		self.pontos = [[10,00],#1
	  [35,00],#2
	  [50,10],#3
	  [50,45],#4
	  [5,60],#5
	  [50,60],#6
	  [50,70],#7
	  [00,70],#8
	  [00,53],#9
	  [40,38],#10
	  [40,15],#11
      [33,10],#12
	  [13,10],#13
	  [5,18],#14
	  [0,10]]#15

	def draw(self):
		for i in range(-1, len(self.pontos) - 1):
			pygame.draw.line(screen, BLACK, self.pontos[i], self.pontos[i + 1], 1)

	def translate(self, m, n):
		if(self.pontos[0] == m and self.pontos[1] == n):
			return
		m = m
		n = n
		m_t = [[1, 0, m],
		    [0, 1, n],
		    [0, 0, 1]
		]
		for i in range(len(self.pontos)):
			a = [[self.pontos[i][0]], [self.pontos[i][1]], [1]]
			m_t = np.matrix(m_t)
			a = np.matrix(a)
			a = np.dot(m_t, a)
			self.pontos[i][0] = a[0]
			self.pontos[i][1] = a[1]
	def rotate(self, ang):
		m_t = [[math.cos(ang), math.sin(ang), 0],
		       [-math.sin(ang), math.cos(ang), 0],
		       [0, 0, 1]
		]
		for i in range(len(self.pontos)):
			a = [[self.pontos[i][0]], [self.pontos[i][1]], [1]]
			m_t = np.matrix(m_t)
			a = np.matrix(a)
			a = np.dot(m_t, a)
			self.pontos[i][0] = a[0]
			self.pontos[i][1] = a[1]

	def animate(self, m, n, ang, t):
		ang = ang/t
		m = m/t + self.pontos[0][0]
		n = n/t + self.pontos[0][1]
		m_tr = [[math.cos(ang), math.sin(ang), 0],
		       [-math.sin(ang), math.cos(ang), 0],
		       [0, 0, 1]
			]

		m_tt = [[1, 0, m],
		    [0, 1, n],
		    [0, 0, 1]
		]

		m_t0 = [[1, 0, -self.pontos[0][0]],
		    [0, 1, -self.pontos[0][1]],
		    [0, 0, 1]
		]
		m_ta = np.dot(m_tr, m_t0)
		m_ta = np.dot(m_tt, m_ta)
#		self.translate(0,0)
#		self.rotate(-math.pi/2)
#		self.translate(m, n)
		for i in range(len(self.pontos)):
			a = [[self.pontos[i][0]], [self.pontos[i][1]], [1]]
			a = np.dot(m_ta, a)
			self.pontos[i][0] = a[0]
			self.pontos[i][1] = a[1]

fig = dois()
fig.translate(50, 50)
#fig.animate(200,200,0)
state = 0
max_state = 120
#fig.animate(100,100,0)
while not done:

    # This limits the while loop to a max of 10 times per second.
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
        state = state + 1
        fig.animate(400, 400, -math.pi/2, max_state)
    fig.draw()

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
