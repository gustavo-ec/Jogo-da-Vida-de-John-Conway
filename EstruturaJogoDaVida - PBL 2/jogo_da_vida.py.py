import os
import time

# Tabuleiro, contador e posição inicial do cursor
tabuleiro = []
ultima_geracao = []
penultima_geracao = []
pos_x = pos_y = 0
cont = 0

# Entrada dos simbolos
viva = input('Digite uma figura para representar as vivas: ')
morta = input('Digite uma figura para representar as mortas: ')

# criação inicial da matriz preenchida com células mortas 
for l in range(10):
    linha = []
    for c in range(10):
        linha.append(morta)
    tabuleiro.append(linha)

# Função que exibe a matriz no terminal destacando a posição do cursor 
def matriz_com_cursor(Matriz, pos_x, pos_y):
    for y in range(10):
        Matriz = []
        print()
        for x in range(10):
            if y == pos_y and x == pos_x:
                Matriz.append(f"[{tabuleiro[y][x]}]")
            else:
                Matriz.append(f"{tabuleiro[y][x]}")
        print(Matriz)

# Função para contar quantidade de vivos ao redor da posição
def contar_vizinhos_vivos(tabuleiro, x, y):
    deslocamento = [(-1, -1), (-1, 0), (-1, 1),
                    ( 0, -1),          ( 0, 1),
                    ( 1, -1), ( 1, 0), ( 1, 1)]
    c = 0
    for dx, dy in deslocamento:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < 10 and 0 <= ny < 10:
            if tabuleiro[ny][nx] == viva:
                c += 1
    return c

# Fução para mudar o estado da matriz
def verificar_tabuleiro(tabuleiro):
    nova_matriz = []
    for y in range(10):
        nova_linha = []
        for x in range(10):
            vivos = contar_vizinhos_vivos(tabuleiro, x, y)
            if tabuleiro[y][x] == viva:
                if vivos < 2 or vivos > 3:
                    nova_linha.append(morta)
                else:
                    nova_linha.append(viva)
            else:
                if vivos == 3:
                    nova_linha.append(viva)
                else:
                    nova_linha.append(morta)
        nova_matriz.append(nova_linha)
    return nova_matriz

# Fução para verificar fim do jogo
def finalizar_jogo(tabuleiro, nova_geracao, ultima_geracao, penultima_geracao):
    todas_mortas = all(celula != viva for linha in nova_geracao for celula in linha)
    estatico = nova_geracao == tabuleiro
    oscilador = nova_geracao == penultima_geracao
    return todas_mortas or estatico or oscilador

# Para o controle de modo inserção inicial
posicao_inicial = True
while posicao_inicial:
    os.system('cls' if os.name == 'nt' else 'clear')
    matriz_com_cursor(tabuleiro, pos_x, pos_y)
    print('Use W (cima), A (esquerda), S (baixo), D (direita), V (marcar vivo), ! (iniciar jogo)')
    comando = input('Comando: ').lower()
    if comando == '!':
        posicao_inicial = False
    elif comando == 'w' and pos_y > 0:
        pos_y -= 1
    elif comando == 's' and pos_y < 10 - 1:
        pos_y += 1
    elif comando == 'a' and pos_x > 0:
        pos_x -= 1
    elif comando == 'd' and pos_x < 10 - 1:
        pos_x += 1
    elif comando == 'v':
        tabuleiro[pos_y][pos_x] = viva
    matriz_com_cursor(tabuleiro, pos_x, pos_y)

# Fase de execução do jogo
jogo = True
while jogo:
    os.system('cls' if os.name == 'nt' else 'clear')
    matriz_com_cursor(tabuleiro, -1, -1)
    cont += 1
    print(cont, '° GERAÇÃO')
    nova_geracao = verificar_tabuleiro(tabuleiro)
    penultima_geracao = [linha[:] for linha in ultima_geracao]
    ultima_geracao = [linha[:] for linha in tabuleiro]
    if cont >= 3:
        if finalizar_jogo(tabuleiro, nova_geracao, ultima_geracao, penultima_geracao):
            print('Todas mortas, estáticas ou oscilando.')
            jogo = False
    tabuleiro = nova_geracao
    time.sleep(1.2)
