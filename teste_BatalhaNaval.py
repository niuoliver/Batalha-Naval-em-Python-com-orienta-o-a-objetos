# TESTE DE APLICAÇÃO DE CLASSES EM POO "Python Blyat"
import random
from tkinter import messagebox
'''Substituiur os prints dos métodos nas classes auxiliares por retornos de valores caso haja uma interface tkinter'''


class Coordenada:
    def __init__(self, linha, coluna):
        self.__linha = linha
        self.__coluna = coluna

    def getLinha(self):
        return self.__linha

    def getColuna(self):
        return self.__coluna


# -----------------------------------------------------------------
class Navio:
    # nome = str
    # posicoes, abates = int
    # status = bool -> vivo ou morto
    def __init__(self, nome, tamanho):
        self.__nome = nome
        self.__tamanho = tamanho
        self.__coordenadas = []
        self.__abates = 0
        self.__status = True

    # adiciona coordenadas ao navio ao posicina-lo
    def add_coordenada(self, cood):
        self.__coordenadas.append(cood)

    # determina a quantidade de posições abatidas do navio
    def setAbate(self):
        self.__abates += 1

        if self.__abates >= self.__tamanho:
            self.__status = False
            print(self.__nome, " foi destruido!")

    def getStatus(self):
        return self.__status

    def getTamanho(self):
        return self.__tamanho

    def getNome(self):
        return self.__nome

    def getAbates(self):
        return self.__abates


# -----------------------------------------------------------------
class Porta_Avioes(Navio):
    def __init__(self):
        super().__init__("Porta Avioes", 5)


class Encouraçado(Navio):
    def __init__(self):
        super().__init__("Encouracado", 4)


class Cruzador(Navio):
    def __init__(self):
        super().__init__("Cruzador", 3)


class Submarino(Navio):
    def __init__(self):
        super().__init__("Submarino", 2)


class Destroier(Navio):
    def __init__(self):
        super().__init__("Destroier", 1)


# -----------------------------------------------------------------
class Celula:
    def __init__(self):
        self.__valor = "~"
        self.__cheio = False
        self.__status = False
        self.__navio = None

    # controle visual(water(~)/boat(o))
    def getValor(self):
        return self.__valor

    # controle de opsição(vazia/com barco)
    def getCheio(self):
        return self.__cheio

    # controle de posição(bombardeado/!bombardeado)
    def getStatus(self):
        return self.__status

    # "o" para barco, "*" para bombardeio, "x" para acerto.
    def setValor(self, novoValor):
        self.__valor = novoValor

    def setCheio(self, navio_obj):
        self.__cheio = True
        self.__navio = navio_obj

    def setStatus(self):
        if self.__status:
            print("Essa coordenada já foi bombardeada.")
            return

        self.__status = True

        if self.__navio:
            print("Acerto!")
            self.__valor = "x"
            self.__navio.setAbate()
        else:
            print("Agua!")
            self.__valor = "*"


# -----------------------------------------------------------------
class Tabuleiro:
    def __init__(self, linhas, colunas):
        self.__linhas = linhas
        self.__colunas = colunas
        self.__matriz = [[Celula() for _ in range(colunas)]
                         for _ in range(linhas)]

    def verifica_cood(self, i, j):
        return 0 <= i < self.__linhas and 0 <= j < self.__colunas

    def verifica_status(self, i, j):
        return self.__matriz[i][j].getStatus()

    def mostra(self):
        # cabeçalho do tabuleiro
        print(end=" ")
        for k in range(self.__colunas):
            print(" ", k, " ", end=" ")
        print()
        for i in range(self.__linhas):
            print(i, end="")
            for j in range(self.__colunas):
                print("|", self.__matriz[i][j].getValor(), "|", end=" ")
            print()

    # talvez repasse esse método para as classes dos jogadores
    def posicionar_navio(self, navio, coordenadas):
        for (i, j) in coordenadas:
            if self.verifica_cood(i, j) == False:
                print("Coordenadas invalidas.")
                return False

            celula = self.__matriz[i][j]

            if celula.getCheio():
                print("Já existe um navio nessa posicao")
                return False

        for (i, j) in coordenadas:
            celula = self.__matriz[i][j]
            celula.setCheio(navio)
            navio.add_coordenada(Coordenada(i, j))

        return True

    # função auxiliar para feedback visual do jogador ao posicionar um navio
    def altera_valores(self, coordenadas):
        for (i, j) in coordenadas:
            celula = self.__matriz[i][j]
            celula.setValor("o")

    # talvez repasse esse método para as classes de jogadores
    def atacar(self, i, j):
        if self.verifica_cood(i, j) == False:
            print("Coordenadas inválidas!")
            return

        self.__matriz[i][j].setStatus()


# classe genérica que irá moldar as ações dos jogadores.-----------
class Jogador:
    # nome = string
    def __init__(self, nome):
        self.__nome = nome

    # @abstractmethod
    def posicionar_navio(self):
        pass

    # @abstractmethod
    def atacar(self):
        pass


# ações ofensivas do humano alteram valores no tabuleiro da IA-----
class Humano(Jogador):
    def posicionar_navio(self, tabuleiro_humano, navio):
        print("\n'''A posição de referência para posicionar o navio será sempre uma de suas extremidades, a superior ou a esquerda."

              "\nTenha isso em mente ao escolher as coordenadas dos seus navios.'''")
        print("\nPosicionando ", navio.getNome(),
              " tamanho: ", navio.getTamanho(), ".")

        ct = True
        while ct == True:
            try:
                tabuleiro_humano.mostra()
                i = int(input("Linha inicial: "))
                j = int(input("Coluna inicial: "))
                ct2 = True
                while ct2 == True:
                    direcao = int(input("[1].Horizontal | [2].Vertical > "))
                    if direcao not in [1, 2]:
                        print("Direção inválida.")
                    else:
                        ct2 = False
            except ValueError:
                print("Valores invalidos, uso somente numeros inteiros.")
                return

            coords = []

            for k in range(navio.getTamanho()):
                if direcao == 1:
                    coords.append((i, j+k))
                else:
                    coords.append((i+k, j))

            if tabuleiro_humano.posicionar_navio(navio, coords):
                tabuleiro_humano.altera_valores(coords)

                print("Navio posicionado com sucesso.")
                ct = False
            else:
                print("Erro ao posicionar navio.")
                messagebox.showerror(
                    title="ERRO!", message="Erro ao posicioanr navio. Tente novamente.")

    def atacar(self, tabuleiro_IA):
        try:
            i = int(input("Linha: "))  # - 1
            j = int(input("Coluna: "))  # - 1
        except ValueError:
            print("Valores invalidos, use apenas numeros inteiros")
            return

        if (0 <= i < 10 and 0 <= j < 10):
            tabuleiro_IA.atacar(i, j)


# ------------------------------------------------------------------
class Ia(Jogador):
    def posicionar_navio(self, tabuleiro_IA, navio):
        ct = True
        # estabelecer laço para repetir processo caso o posicionamento falhe.
        while ct == True:
            i = random.randint(0, 9)
            j = random.randint(0, 9)
            direcao = random.randint(1, 2)
            coords = []

            # verificar se as posições sorteadas são válidas.
            for k in range(navio.getTamanho()):
                if direcao == 1:
                    coords.append((i, j+k))
                else:
                    coords.append((i+k, j))
            if tabuleiro_IA.posicionar_navio(navio, coords):
                # essas funções são só para controle, não estarão no jogo final.
                tabuleiro_IA.altera_valores(coords)
                print("Navio posicionado como sucesso.")
                ct = False

            else:
                print("Erro ao posicionar navio.")

    def atacar(self, tabuleiro_humano):

        tentativas = 0

        # verificador para não atacar coordenadas repetidas
        while tentativas < 100:
            i = random.randint(0, 9)
            j = random.randint(0, 9)

            if tabuleiro_humano.verifica_status(i, j) == True:
                print("Coordenadas repetidas")
                tentativas += 1
            else:
                tabuleiro_humano.atacar(i, j)
                break


# ------------------------------------------------------------------
'''Na classe jogo deve haver dois dicionários para controle de status dos navios,
 assim será possível conferir as condiçõe de encerramento com acesso direto.'''


class Jogo():
    def __init__(self):
        self.__tabuleiro_humano = Tabuleiro(10, 10)
        self.__tabuleiro_IA = Tabuleiro(10, 10)

        self.__humano = Humano("JOGADOR")
        self.__ia = Ia("CPU")

        self.__navios_humano = {0: Destroier(), 1: Submarino(
        ), 2: Cruzador(), 3: Encouraçado(), 4: Porta_Avioes()}

        self.__navios_Ia = {0: Destroier(), 1: Submarino(
        ), 2: Cruzador(), 3: Encouraçado(), 4: Porta_Avioes()}

        self.__controle = True

    # verificador de fim do jogo.
    def verifica_fim(self):
        ct1 = 0
        ct2 = 0
        for k in self.__navios_humano:
            if self.__navios_humano[k].getStatus() == False:
                ct1 += 1
        for k in self.__navios_Ia:
            if self.__navios_Ia[k].getStatus() == False:
                ct2 += 1

        if ct1 == 5:
            print("Você perdeu.")
            self.__controle = False

        if ct2 == 5:
            print("Você venceu!")
            self.__controle = False

    def init_tabuleiros(self):
        # chamadas das funções de posicionamento de navios.
        for k in self.__navios_Ia:
            self.__ia.posicionar_navio(
                self.__tabuleiro_IA, self.__navios_Ia[k])

        for k in self.__navios_humano:
            self.__humano.posicionar_navio(
                self.__tabuleiro_humano, self.__navios_humano[k])

    def andamento(self):
        # loop simples de ataque.
        while self.__controle == True:
            try:
                op = int(input(
                    "\nEscolha uma das opcoes.\n[1].Relatorio de danos\n[2].Atacar\n[0].sair\n->"))
                if op == 1:
                    self.__tabuleiro_humano.mostra()
                    print("Seus navios:")
                    for k in self.__navios_humano:
                        print(self.__navios_humano[k].getNome(
                        ), " - ataques sofridos:", self.__navios_humano[k].getAbates())
                elif op == 2:
                    self.__tabuleiro_IA.mostra()
                    self.__humano.atacar(self.__tabuleiro_IA)
                    self.__ia.atacar(self.__tabuleiro_humano)
                    self.verifica_fim()
                elif op == 0:
                    print("Encerrando o jogo")
                    self.__controle = False
                else:
                    print("opcao inválida.")
            except ValueError:
                print("Valor de entrada invalido, use somente numeros inteiros.")
                continue


# MAIN()-----------------------------------------------------------
jogo = Jogo()
jogo.init_tabuleiros()
jogo.andamento()
