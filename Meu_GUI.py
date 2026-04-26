from tkinter import *
from tkinter import messagebox


class Posicionar:
    def __init__(self, tabuleiro_h, navios_h, prox_funcao):
        self.tabuleiro_h = tabuleiro_h
        self.navios_h = navios_h
        self.prox_funcao = prox_funcao
        self.idx_navio = 0

        self.janela = Tk()
        self.janela.title("Batalha Naval")
        self.janela.geometry("720x520")

        # ===== FRAME PRINCIPAL =====
        self.main_frame = Frame(self.janela)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ===== TOPO =====
        self.top_frame = Frame(self.main_frame)
        self.top_frame.pack(fill="x", pady=(0, 10))

        self.cabeca = Label(
            self.top_frame,
            text="A posição de referência será sempre uma extremidade (superior ou esquerda).\nEscolha bem as coordenadas."
        )
        self.cabeca.pack()

        self.msg_navio = Label(self.top_frame, text="",
                               font=("Arial", 10, "bold"))
        self.msg_navio.pack()

        # ===== CENTRO =====
        self.center_frame = Frame(self.main_frame)
        self.center_frame.pack(fill="both", expand=True)

        # --- TABULEIRO (ESQUERDA) ---
        self.tabuleiro_frame = Frame(self.center_frame, relief=RAISED, bd=3)
        self.tabuleiro_frame.pack(side="left", padx=10)

        self.tabuleiro = Frame(self.tabuleiro_frame)
        self.tabuleiro.pack()

        for i in range(10):
            Label(self.tabuleiro, text=str(i)).grid(row=i+1, column=0)

        for j in range(10):
            Label(self.tabuleiro, text=str(j)).grid(row=0, column=j+1)

        self.matriz_labels = []
        for i in range(10):
            linha = []
            for j in range(10):
                celula = Label(self.tabuleiro, bg="blue",
                               width=2, height=1, relief=RAISED, bd=1)
                celula.grid(row=i+1, column=j+1, padx=1, pady=1)
                linha.append(celula)
            self.matriz_labels.append(linha)

        # --- FORMULÁRIO (DIREITA) ---
        self.form_frame = Frame(self.center_frame, relief=GROOVE, bd=3)
        self.form_frame.pack(side="right", padx=10, fill="y")

        Label(self.form_frame, text="Entrada de Dados", font=(
            "Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        Label(self.form_frame, text="Linha (0-9):").grid(row=1,
                                                         column=0, sticky="e", padx=5, pady=5)
        self.entrada_linha = Entry(self.form_frame, width=5)
        self.entrada_linha.grid(row=1, column=1, pady=5)

        Label(self.form_frame, text="Coluna (0-9):").grid(row=2,
                                                          column=0, sticky="e", padx=5, pady=5)
        self.entrada_coluna = Entry(self.form_frame, width=5)
        self.entrada_coluna.grid(row=2, column=1, pady=5)

        Label(self.form_frame, text="Direção (1=H, 2=V):").grid(
            row=3, column=0, sticky="e", padx=5, pady=5)
        self.entrada_direcao = Entry(self.form_frame, width=5)
        self.entrada_direcao.grid(row=3, column=1, pady=5)

        # ===== RODAPÉ =====
        self.bottom_frame = Frame(self.main_frame)
        self.bottom_frame.pack(fill="x", pady=10)

        self.confirma = Button(
            self.bottom_frame,
            text="Confirmar",
            command=self.ler_entrada,
            width=20
        )
        self.confirma.pack()

        self.confirma.config(activebackground="#FF0000")

    def atualizar_mensagem(self):
        navio_atual = self.navios_h[self.idx_navio]
        self.msg_navio.config(
            text=f"Posicionando {navio_atual.getNome()}. Tamanho:{navio_atual.getTamanho()}")

    def encerra(self):
        self.janela.destroy()
        self.prox_funcao()

    def ler_entrada(self):

        try:
            i = int(self.entrada_linha.get())
            j = int(self.entrada_coluna.get())
            dir = int(self.entrada_direcao.get())
        except ValueError:
            messagebox.showerror(
                title="ERRO!", message="Valores invalidos, use somente numeros inteiros.")
            return

        if dir not in (1, 2):
            messagebox.showerror(title="ERRO!", message="Direção inválida.")
            return

        navio_atual = self.navios_h[self.idx_navio]

        coords = []
        for k in range(navio_atual.getTamanho()):
            if dir == 1:
                coords.append((i, j+k))
            else:
                coords.append((i+k, j))

        if self.tabuleiro_h.posicionar_navio(navio_atual, coords):
            for (linha, coluna) in coords:
                self.matriz_labels[linha][coluna].config(bg="green")
                self.tabuleiro_h.altera_valores(coords)

            # limpa campos de entrada de texto.
            for campo in (self.entrada_linha, self.entrada_coluna, self.entrada_direcao):
                campo.delete(0, END)

            self.idx_navio += 1
            # confere se todos os navios foram posicionados.
            if self.idx_navio >= len(self.navios_h):
                self.confirma.config(state=DISABLED)
                messagebox.showinfo(
                    title="SUCESSO!", message="Todos os navios foram posicionados.")
                self.janela.after(1200, self.encerra)
            else:
                self.atualizar_mensagem()
        else:
            messagebox.showerror(
                title="ERRO!", message="Erro ao posicionar navio.")
            return

    def loop_principal(self):
        self.atualizar_mensagem()
        self.janela.mainloop()


class Combate:
    def __init__(self, tabuleiro_h, tabuleiro_ia, navios_h, navios_ia, objeto_ia, verifica_fim):
        self.tabuleiro_h = tabuleiro_h
        self.tabuleiro_ia = tabuleiro_ia
        self.navios_h = navios_h
        self.navios_ia = navios_ia
        self.IA = objeto_ia
        self.verifica_fim = verifica_fim

        self.janela = Tk()
        self.janela.title("Batalha Naval")
        self.janela.geometry("760x520")

        # ===== FRAME PRINCIPAL =====
        self.main_frame = Frame(self.janela)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ===== TOPO =====
        self.top_frame = Frame(self.main_frame)
        self.top_frame.pack(fill="x", pady=(0, 10))

        self.cabeca = Label(
            self.top_frame,
            text="Clique nas células do campo inimigo para atacar.",
            font=("Arial", 10, "bold")
        )
        self.cabeca.pack()

        # ===== CENTRO =====
        self.center_frame = Frame(self.main_frame)
        self.center_frame.pack(fill="both", expand=True)

        # =========================
        # CAMPO INIMIGO (ESQUERDA)
        # =========================
        self.enemy_frame = Frame(self.center_frame, relief=GROOVE, bd=3)
        self.enemy_frame.pack(side="left", padx=10)

        self.titulo_1 = Label(
            self.enemy_frame, text="Campo Inimigo", font=("Arial", 10, "bold"))
        self.titulo_1.pack(pady=5)

        self.tabuleiro_IA = Frame(self.enemy_frame)
        self.tabuleiro_IA.pack()

        for i in range(10):
            Label(self.tabuleiro_IA, text=i).grid(row=i+1, column=0)
        for j in range(10):
            Label(self.tabuleiro_IA, text=j).grid(row=0, column=j+1)

        self.matriz_botoes = []
        for i in range(10):
            lista_botoes = []
            for j in range(10):
                celula = Button(self.tabuleiro_IA, bg="blue",
                                width=2, height=1, relief=RAISED, bd=1)
                celula.grid(row=i+1, column=j+1, padx=1, pady=1)

                celula.bind("<Button-1>", lambda e, linha=i,
                            coluna=j: self.ao_clicar(linha, coluna))

                lista_botoes.append(celula)
            self.matriz_botoes.append(lista_botoes)

        # =========================
        # CAMPO ALIADO (DIREITA)
        # =========================
        self.ally_frame = Frame(self.center_frame, relief=GROOVE, bd=3)
        self.ally_frame.pack(side="right", padx=10)

        self.titulo_2 = Label(
            self.ally_frame, text="Campo Aliado", font=("Arial", 10, "bold"))
        self.titulo_2.pack(pady=5)

        self.tabuleiro_humano = Frame(self.ally_frame)
        self.tabuleiro_humano.pack()

        for i in range(10):
            Label(self.tabuleiro_humano, text=i).grid(row=i+1, column=0)
        for j in range(10):
            Label(self.tabuleiro_humano, text=j).grid(row=0, column=j+1)

        self.matriz_label = []
        for i in range(10):
            lista_label = []
            for j in range(10):
                celula = Label(self.tabuleiro_humano, bg="blue",
                               width=2, height=1, relief=RAISED, bd=1)
                celula.grid(row=i+1, column=j+1, padx=1, pady=1)

                # sem comando (mantido)
                lista_label.append(celula)
            self.matriz_label.append(lista_label)

    def pintar_tabuleiro(self):
        for navio in self.navios_h.values():
            for coordenada in navio.getCoordenadas():
                linha = coordenada.getLinha()
                coluna = coordenada.getColuna()
                self.matriz_label[linha][coluna].config(bg="green")

    def ataque_ia(self):
        i, j, ataque = self.IA.atacar(self.tabuleiro_h)

        if ataque:
            self.matriz_label[i][j].config(bg="red")
        else:
            self.matriz_label[i][j].config(bg="grey")

        # checagem de fim de jogo
        if self.verifica_fim():
            messagebox.showinfo(title="Fim de Jogo", message="Você perdeu.")
            self.janela.destroy()

    def ao_clicar(self, linha, coluna):
        if self.tabuleiro_ia.atacar(linha, coluna):
            self.matriz_botoes[linha][coluna].config(bg="red")
        else:
            self.matriz_botoes[linha][coluna].config(bg="grey")

        # checagem do fim do jogo.
        if self.verifica_fim():
            messagebox.showinfo(title="Fim de Jogo", message="Você venceu!")
            self.janela.destroy()

        # vez da ia
        self.janela.after(400, self.ataque_ia)

    def loop_principal(self):
        self.pintar_tabuleiro()
        self.janela.mainloop()
