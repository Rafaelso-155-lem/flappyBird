import pygame
import os
import random

class Cano:
    def __init__(self, tela):
        self.tela = tela
        assets = os.path.join(os.path.dirname(__file__), "..", "assets")

        # carrega sprite (assume que a cabeça está na parte de cima da imagem)
        img = pygame.image.load(os.path.join(assets, "cano.png")).convert_alpha()

        self.largura = img.get_width()
        self.cabeca_altura = 32  # altura da "cabeça" do cano no sprite (ajuste se necessário)

        # recortes: cabeça (topo) e corpo (embaixo)
        self.cabeca = img.subsurface((0, 0, self.largura, self.cabeca_altura))
        self.corpo = img.subsurface((0, self.cabeca_altura, self.largura, img.get_height() - self.cabeca_altura))

        self.x = tela.get_width()
        self.velocidade = 3
        self.gap = 180

        ALTURA_TELA = tela.get_height()

        # garante que o buraco fique dentro da área jogável
        buraco = random.randint(120, ALTURA_TELA - 200)

        # alturas dos corpos (em pixels)
        self.altura_cima = buraco  # altura do corpo acima da cabeça invertida
        self.altura_baixo = ALTURA_TELA - (buraco + self.gap)

        # ======= calcular tops corretamente =======
        # Para o cano superior:
        # head_top = buraco - head_height
        # body_top = head_top - body_height
        head_top_cima = buraco - self.cabeca_altura
        body_top_cima = head_top_cima - self.altura_cima

        # Para o cano inferior:
        # head_top = buraco + gap
        # body_top = head_top + head_height
        head_top_baixo = buraco + self.gap
        body_top_baixo = head_top_baixo + self.cabeca_altura

        # rects para colisão (usar tamanho: largura x (body + head) para simplificar)
        self.rect_cima = pygame.Rect(self.x, body_top_cima, self.largura, self.altura_cima + self.cabeca_altura)
        self.rect_baixo = pygame.Rect(self.x, head_top_baixo, self.largura, self.altura_baixo + self.cabeca_altura)

        # salvar posições de desenho
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
        # recompute head_top_baixo and body_top_baixo consistently
        self.head_top_baixo = self.rect_baixo.y
        self.body_top_baixo = self.head_top_baixo + self.cabeca_altura

    def desenhar(self):
        # --- CANO SUPERIOR ---
        # corpo (invertido e esticado para cima)
        if self.altura_cima > 0:
            corpo_cima = pygame.transform.flip(self.corpo, False, True)
            corpo_cima = pygame.transform.scale(corpo_cima, (self.largura, self.altura_cima))
            self.tela.blit(corpo_cima, (self.x, self.body_top_cima))
        # cabeça invertida (acima do corpo)
        cabeca_cima = pygame.transform.flip(self.cabeca, False, True)
        self.tela.blit(cabeca_cima, (self.x, self.head_top_cima))

        # --- CANO INFERIOR ---
        # corpo (normal e esticado para baixo)
        if self.altura_baixo > 0:
            corpo_baixo = pygame.transform.scale(self.corpo, (self.largura, self.altura_baixo))
            self.tela.blit(corpo_baixo, (self.x, self.body_top_baixo))
        # cabeça normal (no topo do cano inferior)
        self.tela.blit(self.cabeca, (self.x, self.head_top_baixo))

    def detectarColisao(self, jogador_rect):
        return (
            self.rect_cima.colliderect(jogador_rect) or
            self.rect_baixo.colliderect(jogador_rect)
        )
