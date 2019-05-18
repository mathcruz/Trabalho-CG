# -*- coding: utf-8 -*-
from abstract_object import abstract_object
import numpy as np
import math
import pygame
from colors import *

# Iniciando os valores do SRD (Sistema de Referencia do Display)
SRD = [800, 600]

limiteMin = [0,0]       #[xMin, yMin]
limiteMax = [100,100]   #[xMax. yMax]

ambient_light_color = (WHITE)
ambient_light_intensity = 0.2

class object3D(abstract_object):
	def __init__(self, screen, faces, cor):
		super(abstract_object, self).__init__()
		self.faces = faces
		self.dimension = 3
		self.cor = cor
		self.screen = screen

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
	@staticmethod
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
		return object3D(obj2d.screen, faces, obj2d.cor)

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

	#desenha em wire frame
	def draw(self):
		for face in self.faces:
			pygame.draw.polygon(self.screen, BLACK, self.map(self.projection(face, 2.09)), 1)

	def projection_perspec(self, face, zcp = -5):
		m_t = [[1, 0, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 0, 0],
			[0, 0, -1/zcp, 1]]
		f_aux = []
		for i in range(len(face)):
			a = [[face[i][0]], [face[i][1]], [face[i][2]], [1]]
			a = np.dot(m_t, a)
			f_aux.append([a[0], a[1]])
		return f_aux

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
				pygame.draw.polygon(self.screen, new_color, self.map(self.projection_perspec(face, 100)), 0)
