# Import a library of functions called 'pygame'
import pygame
import numpy as np
import math
import abc

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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

class abstract_object(object):
	def __init__(self):
		self.faces = [[]]
		self.dimension = 0
		self.cor = [0, 0, 0]

	def map(self, pontos):
		novosPontos = []
		for i in range(pontos.__len__()):
			x = pontos[i][0]
			y = pontos[i][1]
			novoX = x * SRD[0] / limiteMax[0]
			novoY = -1 * y * SRD[1] / limiteMax[1] + SRD[1]
			novosPontos.append([novoX,novoY])
		return novosPontos

	def get_dimension(self):
		return self.faces[0].__len__()

	#translada o objeto para a posição atual mais as coordenadas passadas como parâmetro
	def translate(self, x, y, max_state = 1):
		x = x / max_state
		y = y / max_state
		matrix = self.apl_translate(x, y)
		self.transform(matrix)

	def animate(self, x, y, ang, max_state = 1):
		ang = ang/max_state
		x = x/max_state
		y = y/max_state
		matrix = self.apl_translate(x + self.faces[0][0][0], y + self.faces[0][0][1], self.apl_rotate(ang, self.apl_translate(-self.faces[0][0][0], -self.faces[0][0][1])))
		self.transform(matrix)

	def get_faces(self):
		return np.copy(self.faces)

	def get_edges(self):
		edges = []
		for face in faces:
			for i in range(len(face)):
				edge = [face[i], face[(i+1)%len(face)]]
				edges.append(edge)
		return edges

	#Alterar para utilizar a função pronta da biblioteca numpy np.inner(a, b)
	def inner_product(self, vector1, vector2):
		result = 0
		for i in range(len(vector1)):
			result += vector1[i] * vector2[i]
		return result

	def norm(self, vector):
		return math.sqrt(self.inner_product(vector, vector))

	def cos(self, vector1, vector2):
		return float(self.inner_product(vector1, vector2)/(self.norm(vector1) * self.norm(vector2)))

	def ang(self, vector1, vector2):
		return math.acos(sefl.get_cos(vector1, vector2))

	def vector_product(self, vector1, vector2):
		return np.cross(vector1, vector2)

class object2D(abstract_object):
	def __init__(self, pontos, cor):
		super(abstract_object, self).__init__()
		self.faces = [pontos]
		self.dimension = 2
		self.cor = cor

	#cria uma translação a partir de uma matriz passada como parâmetro
	def apl_translate(self, m, n,  matrix = np.identity(3)):
		if(matrix.all()):
			matrix = np.identity(self.dimension + 1)
		m_t = [[1, 0, m],
			  [0, 1, n],
			  [0, 0, 1]
			  ]
		return np.dot(m_t, matrix)

	#cria uma rotação a partir de uma matriz passada como parâmetro
	def apl_rotate(self, ang, matrix = np.identity(3)):
		if(matrix.all()):
			matrix = np.identity(self.dimension + 1)
		m_t = [[math.cos(ang), math.sin(ang), 0],
	   		  [-math.sin(ang), math.cos(ang), 0],
	   		  [0, 0, 1]
			  ]
		return np.dot(m_t, matrix)

	#aplica a transformação dada uma matriz de transformação
	def transform(self, matrix):
		for face in self.faces:
			for i in range(len(face)):
				a = [[face[i][0]], [face[i][1]], [1]]
				a = np.dot(matrix, a)
			for k in range(self.dimension):
				face[i][k] = a[k]

	#desenha em wire frame
	def draw(self):
		for face in self.faces:
			pygame.draw.polygon(screen, BLACK, self.map(face), 1)

class object3D(abstract_object):
	def __init__(self, faces, cor):
		super(abstract_object, self).__init__()
		self.faces = faces
		self.dimension = 3
		self.cor = cor

	#cria uma translação a partir de uma matriz passada como parâmetro
	def apl_translate(self, m, n, p,  matrix = np.identity(4)):
		if(matrix.all()):
			matrix = np.identity(self.dimension + 1)
		m_t = [[1, 0, 0, m],
			  [0, 1, 0, n],
			  [0, 0, 1, p],
			  [0, 0, 0, 1]
			  ]
		return np.dot(m_t, matrix)

	#translada o objeto para a posição atual mais as coordenadas passadas como parâmetro
	def translate(self, x, y, z):
		matrix = self.apl_translate(x, y, z)
		self.transform(matrix)

	#cria uma rotação em torno do eixo x a partir de uma matriz passada como parâmetro
	def apl_rotate_x(self, ang, matrix = np.identity(4)):
		if(matrix.all()):
			matrix = np.identity(self.dimension + 1)
		m_t = [[1, 0, 0, 0],
			   [0, math.cos(ang), -math.sin(ang), 0],
			   [0, math.sin(ang), math.cos(ang), 0],
			   [0, 0, 0, 1]
			  ]
		return np.dot(m_t, matrix)
	#gira em torno do eixo x
	def rotate_x(self, ang):
		matrix = self.apl_rotate_x(ang)
		self.transform(matrix)

	#cria uma rotação em torno do eixo y a partir de uma matriz passada como parâmetro
	def apl_rotate_y(self, ang, matrix = np.identity(4)):
		if(matrix.all()):
			matrix = np.identity(self.dimension + 1)
		m_t = [[math.cos(ang), 0, math.sin(ang), 0],
			   [0, 1, 0, 0],
			   [-math.sin(ang), 0, math.cos(ang), 0],
			   [0, 0, 0, 1]
			  ]
		return np.dot(m_t, matrix)

	#gira em torno do eixo y
	def rotate_y(self,ang):
		matrix = self.apl_rotate_y(ang)
		self.transform(matrix)

	#aplica a transformação dada uma matriz de transformação
	def transform(self, matrix):
		for face in self.faces:
			for i in range(len(face)):
				a = [[face[i][0]], [face[i][1]], [face[i][2]], [1]]
				a = np.dot(matrix, a)
				for k in range(self.dimension):
					face[i][k] = a[k]


	def animate(self, ang, max_state):
		ang = ang / max_state
		matrix = self.apl_translate(self.faces[0][0][0], self.faces[0][0][1], self.faces[0][0][2], self.apl_rotate_y(ang / 2, self.apl_translate(-self.faces[0][0][0], -self.faces[0][0][1], -self.faces[0][0][2])))
		self.transform(matrix)

	#cria uma rotação em torno do eixo z a partir de uma matriz passada como parâmetro
	def apl_rotate_z(self, ang, matrix = np.identity(4)):
		if(matrix.all()):
			matrix = np.identity(self.dimension + 1)
		m_t = [[math.cos(ang), -math.sin(ang), 0, 0],
			   [math.sin(ang), math.cos(ang), 0, 0],
			   [0, 0, 1, 0],
			   [0, 0, 0, 1]
			  ]
		return np.dot(m_t, matrix)

	#conversão de objeto 2d para objeto 3d(
	def convert3d(obj2d, e = 5):
		faces = []
		face_front = []
		face_back = []
		for i in range(len(obj2d.faces[0])):
			face_front.append([obj2d.faces[0][i][0], obj2d.faces[0][i][1], 0])
			face_back.append([obj2d.faces[0][-i - 1][0], obj2d.faces[0][-i - 1][1], e])
		faces.append(face_front)
		faces.append(face_back)
		for i in range(len(obj2d.faces[0])):
			face = [[face_front[i][0], face_front[i][1], face_front[i][2]],
				   [face_front[i - 1][0], face_front[i - 1][1], face_front[i - 1][2]],
				   [face_back[((len(face_front)) - i)%len(face_back)][0], face_back[((len(face_front)) - i)%len(face_back)][1], face_back[((len(face_front)) - i)%len(face_back)][2]],
				   [face_back[((len(face_front)) - i - 1)%len(face_back)][0], face_back[((len(face_front)) - i - 1)%len(face_back)][1], face_back[((len(face_front)) - i - 1)%len(face_back)][2]]
			]
			faces.append(face)
		return object3D(faces, obj2d.cor)

	#projeção obliqua
	def projection(self, face, ang):
		m_t = [[1, 0, math.cos(ang), 0],
			   [0, 1, math.cos(ang), 0],
			   [0, 0, 0, 0],
			   [0, 0, 0, 1]
			  ]
		f_aux = []
		for i in range(len(face)):
			a = [[face[i][0]], [face[i][1]], [face[i][2]], [1]]
			a = np.dot(m_t, a)
			f_aux.append([a[0], a[1]])
		return f_aux

	#projeção perspecticva 1 ponto de vista
	def projection_perspec(self, face, zcp = -5):
		m_t = [[1, 0, 0, 0],
			   [0, 1, 0, 0],
			   [0, 0, 0, 0],
			   [0, 0, -1/zcp, 1]
			  ]
		f_aux = []
		for i in range(len(face)):
			a = [[face[i][0]], [face[i][1]], [face[i][2]], [1]]
			a = np.dot(m_t, a)
			f_aux.append([a[0], a[1]])
		return f_aux

	#desenha em wire frame
	def draw(self):
		for face in self.faces:
			pygame.draw.polygon(screen, BLACK, self.map(self.projection(face, 2.09)), 1)

	def draw_shading(self, light_source):
		for face in self.faces:
			incidence_vector = [0, 0, 0]
			v1 = [0, 0, 0]
			v2 = [0, 0, 0]
			for i in range(3):
				incidence_vector[i] = float(light_source[i] - face[0][i])
				v1[i] = float(face[1][i] - face[0][i])
				v2[i] = float(face[2][i] - face[1][i])
			norm_face = self.vector_product(v1, v2)
#			incidence_vector = self.map_3d(incidence_vector)
			if(self.inner_product([0, 0, 100], norm_face) < 0):
#				print(self.cos(incidence_vector, norm_face))
				new_color = [0, 0, 0]
				for i in range(3):
					aux = self.cos(norm_face, incidence_vector) * self.cor[i] + ambient_light_intensity * ambient_light_color[i]
					if(aux < 0):
						aux = 0
					elif(aux > 255):
						aux = 255
					new_color[i] = aux
				pygame.draw.polygon(screen, new_color, self.map(self.projection_perspec(face, 100)), 0)

class dois(object2D):
	def __init__(self, cor):
		pontos = [[0,0], [0,2], [6,7], [2,7], [1,6], [0,7], [0,8], [1,9], [7,9], [8,8], [8,6], [3,2], [8,2], [8,0]]
		super(dois, self).__init__(pontos, cor)

fig = dois([255,140,0])
quadrado = object2D([[0,0],[0,10],[10,10],[10,0], [0, 0]], [132, 42, 181])
q3d = object3D.convert3d(quadrado)
q3d.rotate_x(2.09)
q3d.translate(50, 50, 5)
#fig.translate(50, 50)
fig2 = object3D([[[0,0,0],[10,0,0],[10,0,10],[0,0,10]],[[10,0,10],[10,0,0],[10,10,0],[10,10,10]],[[0,10,10],[10,10,10],[10,10,0],[0,10,0]],[[0,0,10],[0,10,10],[0,10,0],[0,0,0]],[[0,0,0],[0,10,0],[10,10,0],[10,0,0]],[[0,0,10],[10,0,10],[10,10,10],[0,10,10]]], BLUE)
teste = object3D([[[0,0,0],[10,0,0],[10,0,10],[0,0,10]],[[10,0,10],[10,0,0],[10,10,0],[10,10,10]],[[0,10,10],[10,10,10],[10,10,0],[0,10,0]],[[0,0,10],[0,10,10],[0,10,0],[0,0,0]],[[0,0,0],[0,10,0],[10,10,0],[10,0,0]],[[0,0,10],[10,0,10],[10,10,10],[0,10,10]]], GREEN)
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
