import pygame
import sys
import os
from scripts.cenas import Partida

pygame.init()
LARGURA = 400
ALTURA = 600
FPS = 60
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird - Estudo Dirigido")
clock = pygame.time.Clock()
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
partida = Partida(tela)
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if partida.estado == "partida":
                partida.jogador.flap()
        partida.tratar_evento(evento)
    partida.atualizar()
    partida.desenhar()
    pygame.display.update()
    clock.tick(FPS)
