# Batalha-Naval-em-Python-com-orienta-o-a-objetos
Projeto feito para a disciplina de programação avançada durante o quinto semestre Bacharelado em Ciências da Computação

A etapa inicial do projeto consistiu em compartimentalizar o jogo em classes, 
aplicando conceitos de orientação a objetos (POO). Inicialmente foram 
implementadas seis (6) classes principais, sendo elas: 
 Coordenadas – uma classe pensada para auxiliar no armazenamento de 
dados usados ao computar ações possíveis dentro do jogo (posicionar 
navios e atacar); 
 Navio – Uma classe base de atributos privados e todos os métodos já 
definidos, os diferentes tipos de navios herdam dessa classe alterando 
apenas seus atributos (nome e tamanho).  
 Celula – Uma classe feita para reunir valores lógicos essências para o 
funcionamento do jogo. 
 Tabuleiro – Classe de controle implementada para manter e gerenciar 
matrizes de células de forma iterável.  
 Jogador – Uma classe abstrata, criada para servir de molde para suas duas 
subclasses: Humano e Ia. 
 Jogo – Classe auxiliar implementada para controlar o fluxo do jogo (ordenar 
jogadas e controlar condições de parada) 
Todos os atributos essenciais dessas classes são privados. A comunicação entre 
elas é feita inteiramente através de métodos “getter” e “setter”. 
A primeira versão do jogo foi implementada inteiramente com interface em 
terminal, para que fosse possível testar e acompanhar com clareza toda a lógica 
do jogo. Posteriormente foi desenvolvida uma segunda versão que se comunica 
com o usuário através de interfaces gráficas (GUI) feitas com a biblioteca tKinter. A 
lógica inicial do jogo não foi alterada, apenas foram feitas adaptações em alguns 
métodos no que diz respeito a entrada e retorno de dados.
