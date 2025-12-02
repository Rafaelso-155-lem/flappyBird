import pygame
import os
import random

class Cano:
    def __init__(self, tela):
        self.tela = tela
        assets = os.path.join(os.path.dirname(__file__), "..", "assets")

       
        img = pygame.image.load(os.path.join(assets, "cano.png")).convert_alpha()

        self.largura = img.get_width()
        self.cabeca_altura = 32  

       
        self.cabeca = img.subsurface((0, 0, self.largura, self.cabeca_altura))
        self.corpo = img.subsurface((0, self.cabeca_altura, self.largura, img.get_height() - self.cabeca_altura))

        self.x = tela.get_width()
        self.velocidade = 3
        self.gap = 180

        ALTURA_TELA = tela.get_height()

        
        buraco = random.randint(120, ALTURA_TELA - 200)

       
        self.altura_cima = buraco  
        self.altura_baixo = ALTURA_TELA - (buraco + self.gap)

        
        head_top_cima = buraco - self.cabeca_altura
        body_top_cima = head_top_cima - self.altura_cima

       
        head_top_baixo = buraco + self.gap
        body_top_baixo = head_top_baixo + self.cabeca_altura

        self.rect_cima = pygame.Rect(self.x, body_top_cima, self.largura, self.altura_cima + self.cabeca_altura)
        self.rect_baixo = pygame.Rect(self.x, head_top_baixo, self.largura, self.altura_baixo + self.cabeca_altura)

        self.body_top_cima = body_top_cima
        self.head_top_cima = head_top_cima
        self.body_top_baixo = body_top_baixo
        self.head_top_baixo = head_top_baixo

    def atualizar(self):
        self.x -= self.velocidade
        self.rect_cima.x = self.x
        self.rect_baixo.x = self.x
        self.body_top_cima = self.rect_cima.y
        self.head_top_cima = self.body_top_cima + self.altura_cima
        self.body_top_baixo = self.head_top_baixo = self.rect_baixo.y
        
        self.head_top_baixo = self.rect_baixo.y
        self.body_top_baixo = self.head_top_baixo + self.cabeca_altura

    def desenhar(self):
       
        if self.altura_cima > 0:
            corpo_cima = pygame.transform.flip(self.corpo, False, True)
            corpo_cima = pygame.transform.scale(corpo_cima, (self.largura, self.altura_cima))
            self.tela.blit(corpo_cima, (self.x, self.body_top_cima))
      
        cabeca_cima = pygame.transform.flip(self.cabeca, False, True)
        self.tela.blit(cabeca_cima, (self.x, self.head_top_cima))

       
        if self.altura_baixo > 0:
            corpo_baixo = pygame.transform.scale(self.corpo, (self.largura, self.altura_baixo))
            self.tela.blit(corpo_baixo, (self.x, self.body_top_baixo))
       
        self.tela.blit(self.cabeca, (self.x, self.head_top_baixo))

    def detectarColisao(self, jogador_rect):
        return (
            self.rect_cima.colliderect(jogador_rect) or
            self.rect_baixo.colliderect(jogador_rect)
        )
