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

class object2D(abstract_object):
	def __init__(self, screen, pontos, cor):
		super(abstract_object, self).__init__()
		self.faces = [pontos]
		self.dimension = 2
		self.cor = cor
		self.screen = screen

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
			pygame.draw.polygon(self.screen, BLACK, self.map(face), 1)
