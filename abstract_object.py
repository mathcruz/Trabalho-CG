# -*- coding: utf-8 -*-
from abc import ABC
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

class abstract_object(ABC):


	def __init__(self, screen):
		self.faces = [[]]
		self.dimension = 0
		self.cor = [0, 0, 0]
		self.screen = None


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
