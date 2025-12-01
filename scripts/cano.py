import pygame
import os
import random

class Cano:
    def __init__(self, tela):
        assets = os.path.join(os.path.dirname(__file__), "..", "assets")
        try:
            self.imagem = pygame.image.load(os.path.join(assets, "cano.png")).convert_alpha()
        except:
            self.imagem = pygame.Surface((52,320), pygame.SRCALPHA)
            self.imagem.fill((34,139,34))

        self.tela = tela

        self.x = tela.get_width()
        self.velocidade = 3
        self.distancia = 250  # GAP

        ALTURA_TELA = tela.get_height()
        
        # garante que o buraco NUNCA sai da tela
        altura_do_buraco = random.randint(80, ALTURA_TELA - 180)

        # topo do cano superior
        self.topo = altura_do_buraco - self.imagem.get_height()
        # posição do cano inferior
        self.base = altura_do_buraco + self.distancia

        self.rect_cima = self.imagem.get_rect(topleft=(self.x, self.topo))
        self.rect_baixo = self.imagem.get_rect(topleft=(self.x, self.base))

    def atualizar(self):
        self.x -= self.velocidade
        self.rect_cima.x = self.x
        self.rect_baixo.x = self.x

    def desenhar(self):
        self.tela.blit(self.imagem, self.rect_cima)
        self.tela.blit(pygame.transform.flip(self.imagem, False, True), self.rect_baixo)

    def detectarColisao(self, jogador_rect):
        return (
            self.rect_cima.colliderect(jogador_rect) or 
            self.rect_baixo.colliderect(jogador_rect)
        )
