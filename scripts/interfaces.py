import pygame

class Texto:
    def __init__(self, tela, texto, x, y, cor=(255,255,255), tamanho=30):
        self.tela = tela
        self.texto = str(texto)
        self.x = x
        self.y = y
        self.cor = cor
        self.font = pygame.font.SysFont(None, tamanho)
    def atualizarTexto(self, novo):
        self.texto = str(novo)
    def desenhar(self):
        img = self.font.render(str(self.texto), True, self.cor)
        self.tela.blit(img, (self.x, self.y))

class Botao:
    def __init__(self, tela, x, y, largura, altura, texto, acao):
        self.tela = tela
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.acao = acao
        self.font = pygame.font.SysFont(None, 32)
        self.clicando = False

    def desenhar(self):
        pygame.draw.rect(self.tela, (0,150,255), self.rect, border_radius=8)
        img = self.font.render(self.texto, True, (0,0,0))
        img_rect = img.get_rect(center=self.rect.center)
        self.tela.blit(img, img_rect)

    def checarClique(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.acao()
