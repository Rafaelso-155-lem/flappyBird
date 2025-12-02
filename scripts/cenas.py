import pygame
from scripts.cano import Cano
from scripts.jogador import Jogador
from scripts.interfaces import Texto, Botao

class Partida:
    def __init__(self, tela):
        self.tela = tela

        # Estado inicial para poder começar o jogo
        self.estado = "menu"

        # tela do jogador
        self.jogador = Jogador(tela, 100, 100)

        # Lista de canos
        self.canos = []

        # contador dos pontos para o jogo
        self.pontosValor = 0
        self.contador = 0
        self.pontosTexto = Texto(tela, str(self.pontosValor), 10, 10, (255,255,255), 30)

        # Botão que aparece no menu
        self.botaoJogar = Botao(
            tela,
            tela.get_width()//2 - 80,
            tela.get_height()//2,
            160,
            50,
            "Jogar",
            self.reiniciar
        )

        # Altura do chão
        self.base_y = tela.get_height() - 50

    # Reiniciar partida → chamado quando clicar no botão
    def reiniciar(self):
        self.jogador = Jogador(self.tela, 100, 100)
        self.canos = []
        self.pontosValor = 0
        self.contador = 0
        self.pontosTexto.atualizarTexto(self.pontosValor)
        self.estado = "partida"

    # Eventos do mouse
    def tratar_evento(self, evento):
        if self.estado == "menu":
            self.botaoJogar.checarClique(evento)

    # Atualização do jogo
    def atualizar(self):
        if self.estado == "menu":
            return

        # Atualizar jogador
        self.jogador.atualizar()

        # Criar canos
        if len(self.canos) == 0 or self.canos[-1].x < 200:
            self.canos.append(Cano(self.tela))

        # Atualizar canos
        for cano in list(self.canos):
            cano.atualizar()
            if cano.x + 80 < 0:
                self.canos.remove(cano)

        # Sistema de pontos (1 ponto por ~1 segundo)
        self.contador += 1
        if self.contador > 60:
            self.pontosValor += 1
            self.contador = 0
            self.pontosTexto.atualizarTexto(self.pontosValor)

        # Colisão com canos
        for cano in self.canos:
            if cano.detectarColisao(self.jogador.getRect()):
                self.voltar_menu()
                return

        # Colisão com topo da tela
        if self.jogador.getRect().top < 0:
            self.voltar_menu()
            return

        # Colisão com chão
        if self.jogador.getRect().bottom > self.base_y:
            self.voltar_menu()
            return

    # Voltar ao menu quando bater
    def voltar_menu(self):
        self.estado = "menu"
        self.jogador = Jogador(self.tela, 100, 100)
        self.canos = []
        self.pontosValor = 0
        self.contador = 0
        self.pontosTexto.atualizarTexto(self.pontosValor)

    # Desenhar menu / partida
    def desenhar(self):
        # MENU
        if self.estado == "menu":
            self.tela.fill((135, 206, 250))   # fundo azul

            # Título
            font = pygame.font.SysFont(None, 60)
            titulo = font.render("Flappy Bird", True, (255, 255, 255))
            self.tela.blit(
                titulo,
                titulo.get_rect(center=(self.tela.get_width()//2, 180))
            )

            # Botão Jogar
            self.botaoJogar.desenhar()
            return

        # PARTIDA
        self.tela.fill((135, 206, 250))  # fundo azul

        # desenhar canos
        for cano in self.canos:
            cano.desenhar()

        # jogador
        self.jogador.desenhar()

        # chão
        pygame.draw.rect(
            self.tela,
            (222,184,135),   # cor do chão
            (0, self.base_y, self.tela.get_width(), 50)
        )

        # pontos
        self.pontosTexto.desenhar()
