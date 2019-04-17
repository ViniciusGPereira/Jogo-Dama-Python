import pygame
from pygame import *
import pygame.mixer

#----CORES-----------------
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)
VERMELHO = (120, 0, 0)
VERDE_ESCURO = (0, 120, 0)
VERDE_CLARO = (0, 255, 0)
VERMELHO_CLARO = (255, 0, 0)
AZUL = (0, 0, 255)
COR_FUNDO = (54, 54, 54)
COR_TABULEIRO = (0, 31, 0)
CINZA_CLARO = (241,241,241)
DOURADO = (218, 165, 32)
AZUL1 = (51, 198, 254)
AZUL2 = (51, 255, 243)
AZUL3 = (51, 226, 249)

Clock = pygame.time.Clock()

pygame.display.set_caption('Dama - Vinicius')

class Tabuleiro(object):


    def __init__(self):
        # ------INICIA-TELA-------------------------
        self.screen = pygame.display.set_mode((400, 470))
        pygame.display.set_caption('Jogo de Damas')
        pygame.font.init()

        # --------------IMAGENS----------------------
        p_branco_image_filename = 'p_branca.png'
        p_preto_image_filename = 'p_preta.png'
        b_branco_image_filename = 'b_branco.png'
        b_preto_image_filename = 'b_preto.png'
        b_box_image_filename = 'box1.png'
        b_flecha1_image_filename = 'flecha1.png'
        b_flecha2_image_filename = 'flecha2.png'
        p_branco_dama_image_filename = 'p_branca1.png'
        p_preto_dama_image_filename = 'p_preta1.png'

        # --------CHAMANDO-IMAGENS-------------------
        b_branco = pygame.image.load(b_branco_image_filename).convert()
        b_preto = pygame.image.load(b_preto_image_filename).convert()

        branco = pygame.image.load(p_branco_image_filename).convert_alpha()
        preto = pygame.image.load(p_preto_image_filename).convert_alpha()

        b_box = pygame.image.load(b_box_image_filename).convert()
        b_flecha1 = pygame.image.load(b_flecha1_image_filename).convert_alpha()
        b_flecha2 = pygame.image.load(b_flecha2_image_filename).convert_alpha()

        d_branco = pygame.image.load(p_branco_dama_image_filename).convert_alpha()
        d_preto = pygame.image.load(p_preto_dama_image_filename).convert_alpha()

        # -----------CONVERTENDO-IMAGENS-------------
        self.bloco_branco = pygame.transform.scale(branco, (50, 50))
        self.bloco_preto = pygame.transform.scale(preto, (55, 50))
        self.b_bloco_branco = pygame.transform.scale(b_branco, (50, 50))
        self.b_bloco_preto = pygame.transform.scale(b_preto, (50, 50))
        self.box = pygame.transform.scale(b_box, (400, 70))
        self.flecha1 = pygame.transform.scale(b_flecha1, (70, 30))
        self.flecha2 = pygame.transform.scale(b_flecha2, (70, 30))
        self.dama_preta = pygame.transform.scale(d_preto, (55, 50))
        self.dama_branca = pygame.transform.scale(d_branco, (50, 50))

        # ------------CHAMADA-SOM--------------------


        #-------------LIMITE-PARA-DAMA----------------
        self.limite_preta = [(0, 0), (100, 0), (200, 0), (300, 0)]
        self.limite_branca = [(50, 350), (150, 350), (250, 350), (350, 350)]
        #------------VETOR-DAMA-----------------------
        self.pos_dama = []
        self.font = pygame.font.SysFont("Comic sans MS", 20)
        self.screen.fill(CINZA)
        self.turno = False
        self.val_pontos_branco = []
        self.jogada_branco = []
        self.val_pontos_preto = []
        self.jogada_preto = []
        self.pecas_tab_preto = []
        self.pontuacao_branco = 0
        self.pontuacao_preto = 0
    def gera_tabuleiro(self, pecas_tabuleiro):
        tamanho = 50
        x, y = 0, 0
        P = self.b_bloco_preto
        B = self.b_bloco_branco
        aux = False
        for j in range(8):
            if aux == True:
                y += tamanho
                x = 0
                TEMP = P
                P = B
                B = TEMP
            for i in range(4):
                self.screen.blit(P, (x, y))
                pecas_tabuleiro.append((x, y))
                self.pecas_tab_preto.append((x,y))
                x += tamanho

                self.screen.blit(B, (x, y))
                pecas_tabuleiro.append((x, y))
                x += tamanho
                aux = True
            pygame.display.flip()

    def imprime_pecas(self, p_preta, p_branca):
        for ux, uy in p_preta:
            self.screen.blit(self.bloco_preto,(ux-2.5, uy))
        for px, py in p_branca:
            self.screen.blit(self.bloco_branco, (px, py))

    def identifica_peca(self, pecas, x, y):
        for x_tab, y_tab in pecas:
            if x > x_tab and y > y_tab and (x_tab + 50) > x and (y_tab + 50) > y:
                return x_tab, y_tab
        return (0,0)

    def seleciona_peca(self, coord, cor):
        x, y = coord
        pygame.draw.circle(self.screen, cor, (x + 25, y + 25), 23)
        pygame.display.flip()

    def regras (self, pecas_branca, pecas_preta, pos_atual, pos_pulo):
        #-REGRA DE MOVIMENTAÇÃO------------------
        x, y = pos_atual
        px,py = pos_pulo

        regra_movi_branca = [(x - 50, y + 50), (x + 50, y + 50)]
        regra_movi_preta = [(x + 50, y - 50), (x - 50, y - 50)]
        kill_branca = [(px + 50, py - 50), (px - 50, py - 50)]
        kill_preta = [(px - 50, py + 50), (px + 50, py + 50)]
        regra_kill_branca = [(x - 2*50, y + 2*50),(x + 2*50, y + 2*50)]
        regra_kill_preta = [(x + 2 * 50, y - 2 * 50), (x - 2 * 50, y - 2 * 50)]
        if pos_atual in pecas_branca:
            if pos_pulo not in pecas_preta:
                if pos_pulo in regra_movi_branca:
                    self.val_pontos_branco.append(1)
                    self.jogada_branco.append((pos_atual,pos_pulo))
                    return 1
                else:
                    for aux_pedra in pecas_preta:
                        if pos_pulo in regra_kill_branca and aux_pedra in kill_branca and pos_pulo not in pecas_branca:
                            self.val_pontos_branco.append(3)
                            self.jogada_branco.append((pos_atual,pos_pulo))
                            return 2
        elif pos_atual in pecas_preta:
            if pos_pulo in regra_movi_preta:
                self.val_pontos_preto.append(1)
                self.jogada_preto.append((pos_atual,pos_pulo))
                return 1
            else:
                for aux_pedra in pecas_branca:
                    if pos_pulo in regra_kill_preta and aux_pedra in kill_preta and pos_pulo not in pecas_preta:
                        self.val_pontos_preto.append(3)
                        self.jogada_preto.append((pos_atual,pos_pulo))
                        return 2
        else:
            return 0

    def kill_pedra(self, pos,pos_pulo, peca_branca, peca_preta):
        x, y = pos
        px, py = pos_pulo
        if pos in peca_branca:
            tab.pontuacao_branco += 1
            if pos_pulo == (x + 2 * 50, y + 2 * 50):
                kill = (px - 50, py - 50)
                peca_preta.remove(kill)
            else:
                kill = (px + 50, py - 50)
                peca_preta.remove(kill)
        else:#if pos in peca_preta:
            tab.pontuacao_preto += 1
            if pos_pulo == (x + 2 * 50, y - 2 * 50):
                kill = (px - 50, py + 50)
                peca_branca.remove(kill)
            else:
                kill = (px + 50, py + 50)
                peca_branca.remove(kill)
    def dama(self, pecas_brancas , pecas_pretas, pedra_select, pedra_select_pulo):

        #movimenta_branca
        x_select, y_select = pedra_select
        x_jump, y_jump = pedra_select_pulo
        aux = pecas_brancas + pecas_pretas
        for n in range(8):
            regra_movimento = [(x_select - 50 * n, y_select + 50 * n), (x_select + 50 * n, y_select + 50 * n),
                               (x_select + 50 * n, y_select - 50 * n), (x_select - 50 * n, y_select - 50 * n)]

            kill = [(x_jump + 50, y_jump - 50), (x_jump - 50, y_jump - 50), (x_jump - 50, y_jump + 50),
                    (x_jump + 50, y_jump + 50)]

            regra_kill = [(x_select - 2 * 50 * n, y_select + 2 * 50 * n),
                          (x_select + 2 * 50 * n, y_select + 2 * 50 * n),
                          (x_select + 2 * 50 * n, y_select - 2 * 50 * n),
                          (x_select - 2 * 50 * n, y_select - 2 * 50 * n)]

            for peca in pecas_brancas + pecas_pretas:
                if pedra_select_pulo in regra_kill and peca in kill:
                    self.kill_dama(pedra_select, pedra_select_pulo, pecas_brancas, pecas_pretas)
                    return 3
                elif pedra_select_pulo in regra_movimento:
                    return 1
                else:
                    print("1")

        return 3
    def kill_dama(self, pos,pos_pulo, peca_branca, peca_preta):
        x, y = pos
        px, py = pos_pulo
        if pos in peca_branca:
            tab.pontuacao_branco += 1
            for n in range(8):
                if pos_pulo == (x + 2 * 50*(n+1), y + 2 * 50*(n+1)):
                    kill = (px - 50, py - 50)
                    peca_preta.remove(kill)
                else:
                    kill = (px + 50, py - 50)
                    peca_preta.remove(kill)
        else:
            tab.pontuacao_preto += 1
            for n in range(8):
                if pos_pulo == (x + 2 * 50*(n+1), y - 2 * 50*(n+1)):
                    kill = (px - 50, py + 50)
                    peca_branca.remove(kill)
                else:
                    kill = (px + 50, py + 50)
                    peca_branca.remove(kill)
    def imprime_dama(self, pecas_pretas, pecas_brancas):
        for peca in self.pos_dama:
            if peca in pecas_pretas:
                x, y = peca
                self.screen.blit(self.dama_preta, (x - 2.5, y))
            else:
                x, y = peca
                self.screen.blit(self.dama_branca, (x - 2.5, y))


class pedras(Tabuleiro):

    def inicia_pecas_pc(self, pecas_tabuleiro, pc):
        tam = len(pecas_tabuleiro)-1
        for i in range(3):
            for j in range(4):
                x, y = pecas_tabuleiro[tam]
                pc.append((x, y))
                tam -= 2
            if i == 1:
                tam += 1
            else:
                tam -= 1
        pygame.display.flip()

    def inicia_pecas_user(self, pecas_tabuleiro, usuario):
        i = 0
        for q in range(3):
            for j in range(4):
                x, y = pecas_tabuleiro[i]
                usuario.append((x, y))
                i += 2
            if q == 1:
                i -= 1
            else:
                i += 1
        pygame.display.flip()

while True:
    #----OBJETOS------
    tab = Tabuleiro()
    pedra = pedras()
    #----ARRAY-DE-POSICOES---
    pecas_tabuleiro = []
    pecas_pretas = []
    pecas_brancas = []
    #----CHAMADA-DE-METODOS---
    tab.gera_tabuleiro(pecas_tabuleiro)
    pedra.inicia_pecas_pc(pecas_tabuleiro, pecas_pretas)
    pedra.inicia_pecas_user(pecas_tabuleiro, pecas_brancas)
    tab.imprime_pecas(pecas_pretas,pecas_brancas)
    tab.screen.blit(tab.box, (0, 400))
    #----O-METODO-IMPRIME_PEÇAS-APENAS-GERA-A-POSIÇÃO-DAS-PEDRAS
    pygame.display.flip()
    #-----VARIAVEL-DE-CONTROLE-DE-LOOP---
    fim = False
    #-----VARIAVEL-DE-CONTROLE-PARA-SELECIONAR-ONDE-PULAR
    pula_pBranca = False
    pula_pPreta = False
    #-----PEGA-NOMES---------
    player1 = input("digite o nome do Primeiro jogador")
    player2 = input("digite o nome do Segundo jogador")
    while not fim:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    fim = True
                if event.key == K_v:
                    pedra_select = (0, 0)
                    pedra_select_pulo = (0, 0)
                    tab.turno = not tab.turno
                    pula_pPreta = False
                    pula_pBranca = False

                    tab.gera_tabuleiro(pecas_tabuleiro)
                    tab.imprime_pecas(pecas_pretas, pecas_brancas)
                    pygame.display.flip()

            if event.type == MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if tab.turno == False:
                    if pula_pBranca == True:
                        pedra_select_pulo = tab.identifica_peca(pecas_tabuleiro, x_mouse, y_mouse)
                    else:
                        pedra_select = tab.identifica_peca(pecas_brancas, x_mouse, y_mouse)
                    if pedra_select != (0, 0):
                        if pula_pBranca == False:
                            tab.seleciona_peca(pedra_select, DOURADO)
                        if pula_pBranca == True:
                            pedra_select_pulo = tab.identifica_peca(pecas_tabuleiro,x_mouse,y_mouse)
                            if pedra_select in tab.pos_dama:
                                regra = tab.dama(pecas_brancas , pecas_pretas, pedra_select, pedra_select_pulo)
                                #-----AQUI SERA A CHAMADA DA DAMA
                            else:
                                regra = tab.regras(pecas_brancas,pecas_pretas,pedra_select,pedra_select_pulo)

                            if regra == 1:
                                pecas_brancas.append(pedra_select_pulo)
                                pecas_brancas.remove(pedra_select)
                                pula_pBranca = False
                                tab.turno = True
                                if pedra_select in tab.pos_dama:
                                    tab.pos_dama.append(pedra_select_pulo)
                                    tab.pos_dama.remove(pedra_select)

                                tab.gera_tabuleiro(pecas_tabuleiro)
                                tab.imprime_pecas(pecas_pretas, pecas_brancas)
                                tab.imprime_dama(pecas_pretas, pecas_brancas)
                                pygame.display.flip()
                            if regra == 2:
                                tab.kill_pedra(pedra_select, pedra_select_pulo, pecas_brancas, pecas_pretas)
                                pecas_brancas.append(pedra_select_pulo)
                                pecas_brancas.remove(pedra_select)
                                pula_pBranca = False

                                tab.gera_tabuleiro(pecas_tabuleiro)
                                tab.imprime_pecas(pecas_pretas, pecas_brancas)
                                tab.imprime_dama(pecas_pretas, pecas_brancas)
                                pygame.display.flip()
                                pedra_select = pedra_select_pulo
                            if regra == 3:
                                print("andou")
                        else:
                            pula_pBranca = True
                elif tab.turno == True:
                    if pula_pPreta == True:
                        pedra_select_pulo = tab.identifica_peca(pecas_tabuleiro, x_mouse, y_mouse)
                    else:
                        pedra_select = tab.identifica_peca(pecas_pretas, x_mouse, y_mouse)
                    if pedra_select != (0, 0):
                        if pula_pPreta == False:
                            tab.seleciona_peca(pedra_select, DOURADO)
                        if pula_pPreta == True:
                            pedra_select_pulo = tab.identifica_peca(pecas_tabuleiro,x_mouse,y_mouse)
                            regra = tab.regras(pecas_brancas, pecas_pretas, pedra_select, pedra_select_pulo)
                            if regra == 1:
                                pecas_pretas.append(pedra_select_pulo)
                                pecas_pretas.remove(pedra_select)
                                pula_pPreta = False
                                tab.turno = False
                                if pedra_select in tab.pos_dama:
                                    tab.pos_dama.append(pedra_select_pulo)
                                    tab.pos_dama.remove(pedra_select)

                                tab.gera_tabuleiro(pecas_tabuleiro)
                                tab.imprime_pecas(pecas_pretas, pecas_brancas)
                                tab.imprime_dama(pecas_pretas, pecas_brancas)
                                pygame.display.flip()
                            if regra == 2:
                                tab.kill_pedra(pedra_select, pedra_select_pulo, pecas_brancas, pecas_pretas)
                                pecas_pretas.append(pedra_select_pulo)
                                pecas_pretas.remove(pedra_select)
                                pula_pPreta = False

                                tab.gera_tabuleiro(pecas_tabuleiro)
                                tab.imprime_pecas(pecas_pretas, pecas_brancas)
                                tab.imprime_dama(pecas_pretas, pecas_brancas)
                                pygame.display.flip()
                                pedra_select = pedra_select_pulo
                        else:
                            pula_pPreta = True

        nome1 = tab.font.render(player1, True, AZUL)
        nome2 = tab.font.render(player2, True, AZUL)
        pontos1 = tab.font.render(str(tab.pontuacao_branco), False, AZUL)
        pontos2 = tab.font.render(str(tab.pontuacao_preto), False, AZUL)
        tab.screen.blit(nome1, [15, 400])
        tab.screen.blit(nome2, [270, 400])

        pygame.draw.rect(tab.screen, AZUL1, (45, 435, 30, 20))
        tab.screen.blit(pontos1, [50, 430])

        pygame.draw.rect(tab.screen, AZUL2, (315, 435, 30, 20))
        tab.screen.blit(pontos2, [320, 430])

        if tab.turno == True:
            pygame.draw.rect(tab.screen, AZUL3, (170, 420, 70, 30))
            tab.screen.blit(tab.flecha1, [170, 420])
        else:
            pygame.draw.rect(tab.screen, AZUL3, (170, 420, 70, 30))
            tab.screen.blit(tab.flecha2, [170, 420])
        pygame.display.flip()

        if len(pecas_brancas) < 1:
            print(player1 + " GANHOU!!")
            fim = True
        if len(pecas_pretas) < 1:
            print(player2 + " GANHOU!!")
            fim = True

        for davez in pecas_brancas:
            if davez in tab.limite_branca:
                tab.pos_dama.append(davez)
        for davez in pecas_pretas:
            if davez in tab.limite_preta:
                tab.pos_dama.append(davez)

        tab.imprime_dama(pecas_pretas, pecas_brancas)
        Clock.tick(10)
