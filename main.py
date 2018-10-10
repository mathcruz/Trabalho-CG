import pygame
import numpy as np
import math
pygame.init()

# Definicao das cores (valores RGB)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Iniciando os valores do SRD (Sistema de Referencia do Display)
SRD = [400, 300]
tela = pygame.display.set_mode(SRD)

limiteMin = [0,0]       #[xMin, yMin]
limiteMax = [100,100]   #[xMax. yMax]


#funcao que mapeia as coordenadas do SRU para o SRD
def map(pontos):
    novosPontos = []
    for i in range(pontos.__len__()):
        x = pontos[i][0]
        y = pontos[i][1]
        novoX = x * SRD[0] / limiteMax[0]
        novoY = -1 * y * SRD[1] / limiteMax[1] + SRD[1]
        novosPontos.append([novoX,novoY])

    return novosPontos

fim = False
clock = pygame.time.Clock()

def animate(pontos, m, n, ang, t):
		ang = ang/t
		m = m/t + pontos[0][0]
		n = n/t + pontos[0][1]
		m_tr = [[math.cos(ang), math.sin(ang), 0],
		       [-math.sin(ang), math.cos(ang), 0],
		       [0, 0, 1]
			]

		m_tt = [[1, 0, m],
		    [0, 1, n],
		    [0, 0, 1]
		]

		m_t0 = [[1, 0, -pontos[0][0]],
		    [0, 1, -pontos[0][1]],
		    [0, 0, 1]
		]
		m_ta = np.dot(m_tr, m_t0)
		m_ta = np.dot(m_tt, m_ta)
#		self.translate(0,0)
#		self.rotate(-math.pi/2)
#		self.translate(m, n)
		for i in range(len(pontos)):
			a = [[pontos[i][0]], [pontos[i][1]], [1]]
			a = np.dot(m_ta, a)
			pontos[i][0] = a[0]
			pontos[i][1] = a[1]


pontos = [[0,0],
          [0,2],
          [6,7],
          [2,7],
          [1,6],
          [0,7],
          [0,8],
          [1,9],
          [7,9],
          [8,8],
          [8,6],
          [3,2],
          [8,2],
          [8,0]]

def translada(x, y, pontos):
    novosPontos = []
    for i in range(pontos.__len__()):
        novoX = pontos[i][0] + x
        novoY = pontos[i][1] + y
        novosPontos.append([novoX,novoY])

    return novosPontos

pontos = translada(50, 50, pontos)
state = 0
max_state = 60
while not fim:
    # o clock.tick(x) limita a repeticao do loop em x vezes por segundo (eh seguro deixa-lo assim)
    clock.tick(30)

    for event in pygame.event.get():  # Captura as interacoes do usuario
        if event.type == pygame.QUIT:  # Se o usuario clicou para sair..
            fim = True  # Muda a flag que indica o fim do loop

    # Limpa a tela e reseta o background
    tela.fill(BRANCO)

    # Desenha um poligono usando como referencia os pontos recebidos
    if(state < max_state):
        state = state + 1
        animate(pontos, -41, 42, -math.pi/2, max_state)
    pygame.draw.polygon(tela, PRETO, map(pontos), 1)

    # Desenha as mudancas feitas na tela
    pygame.display.flip()

pygame.quit()

