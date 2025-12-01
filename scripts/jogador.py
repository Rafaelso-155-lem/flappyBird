import pygame
import os

class Jogador:
    def __init__(self, tela, x, y):
        assets = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.frames = []
        for n in ["passaro-0.png", "passaro-1.png", "passaro-2.png"]:
            caminho = os.path.join(assets, n)
            try:
                img = pygame.image.load(caminho).convert_alpha()
            except:
                img = pygame.Surface((34,24), pygame.SRCALPHA)
                img.fill((255,200,0))
            self.frames.append(img)
        self.indice = 0
        self.imagem = self.frames[self.indice]
        self.rect = self.imagem.get_rect(center=(x, y))
        self.vel = 2
        self.grav = 0.3
        self.anim = 0
        self.tela = tela
    def flap(self):
        self.vel = -6
    def atualizar(self):
        self.vel += self.grav
        self.rect.y += int(self.vel)
        self.anim += 1
        if self.anim % 5 == 0:
            self.indice = (self.indice + 1) % len(self.frames)
            self.imagem = self.frames[self.indice]
    def desenhar(self):
        self.tela.blit(self.imagem, self.rect)
    def getRect(self):
        return self.rect
    def getMask(self):
        return pygame.mask.from_surface(self.imagem)
