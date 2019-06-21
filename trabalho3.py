#!/usr/bin/python

# DANIEL GOBBI BERGHOLZ 16/0004551
# TRABALHO 3 FUNDAMENTOS DE REDES 1

from igraph import *
import os, re

# variavel global para ir armazenando decisoes do usuario 
n = 0

# variaveis globais do grafo

g = Graph() 
vertices = []
arestas = []
pesos = []

'''
g.add_vertices(4)
g.add_edges([(0,1), (1,2), (0,2), (2,3)])
g.vs["name"] = ["v0", "v1", "v2", "v3"]
g.es["weight"] = [1,2,3,4]

# plotar grafo
g.vs["label"] = g.vs["name"]
g.es["label"] = g.es["weight"]

layout = g.layout("kk")

print (g)
plot(g, layout = layout)
'''

# ----------------------------------------------------------------------MENU-----------------------------------------------
def menu(primeira_vez=True):
    global n  
    if (primeira_vez == True):
        os.system('clear')
        print 'Seja bem vindo ao meu programa que simula grafos\n'
    print 'A seguir os algoritmos disponiveis:\n'
    print '1) Dijkstra\n2) Bellman-Ford\n3) RPF\n4) Spanning Tree\n5) SAIR'
    n = input('Por favor, selecione um algoritmo que vc gostaria de executar:\n')
    while (n < 1 or n > 5):
        n = input('Escolha um numero valido (entre 1 e 5):\n')

def ler_dot():
    lista = []
    vertices_aux = []
    n_vertices = 0
    global vertices 
    global arestas
    global pesos
    global g
    g = Graph()
    vertices = []
    arestas = []
    pesos = []

    # abrir arquivo do usuario e ler cada linha 
    x = raw_input('Por favor digite o nome do arquivo: (eh preciso ter .dot no final e o PATH adequado)\n')
    file = open(x, 'r')
    linhas = file.readlines()
    pattern = '\w+\.*\w*'

    # lista = variavel que guarda par de vertices que possuem aresta
    # comeca a ler da linha 1 ao inves da 0, pois a linha zero contem o nome do grafo
    for i in range(1, len(linhas)): 
        lista.append(re.findall(pattern, linhas[i]))

    # apos o regex, temos de deletar o 'label' e salvar o peso da aresta
    for i in range(len(lista)):
        if (len(lista[i]) == 4):
            lista[i].remove('label')
            pesos.append(float(lista[i][2]))
            del lista[i][2]

    # lista = lista de listas. vertices = lista
    for sublista in lista:
        for item in sublista:
            vertices.append(item)

    # caso haja qualquer item vazio, eliminar da lista
    # repetir isso ate que nao haja mais item nenhum vazio
    while True:
        try:
            vertices.remove('')
        except ValueError:
            break 

    # agora iremos adicionar as arestas no grafo
    tupla = ()
    global arestas
    for i in range(0, len(vertices), 2):
        tupla = (vertices[i], vertices[i+1])
        arestas.append(tupla)

    # loop para eliminar duplicatas na lista "vertices"
    for i in vertices:
        if i not in vertices_aux:
            vertices_aux.append(i)
    vertices = vertices_aux

    # finalmente, vertices se tornou uma lista "limpa"
    n_vertices = len(vertices)
    g.add_vertices(n_vertices)
    g.vs["name"] = vertices
    g.add_edges(arestas)
    g.es["weight"] = pesos
    file.close()

def criar_grafo():
    print 'Agora iremos criar seu grafo de testes\n'
    y = raw_input('Voce gostaria de carregar um grafo a partir de um arquivo .DOT? (s/n)\n')
    if (y == 's'):
        ler_dot()
    else:
        global g
        g = Graph()
        vertices = []
        arestas = []
        while True:
            try:
                x = input('Quantos vertices tem seu grafo?\n')
            except SyntaxError:
                print 'Voce somente apertou ENTER. Por favor, digite um numero valido\n'
                continue
            break
        g.add_vertices(x)
        lista = [] # lista auxiliar
        for i in range(g.vcount()):
            lista.append("v" + str(i))
        g.vs["name"] = lista
        lista = []
        print 'Agora iremos construir as arestas deste grafo\nPara parar de criar arestas basta nao digitar valor e apertar enter\n'
        while True: 
            try:
                y, z = input('Escreva um vertice de origem e um de destino (dois valores separados por virgula)\n')
            except SyntaxError:
                y = z = None
            if ((y != None) and (z != None)):
                if((y > (g.vcount() - 1)) or ((z > (g.vcount() - 1)))):
                    print 'Voce digitou um numero invalido de vertice. Seu grafo tem ' + str(g.vcount()) + ' vertices.\n'
                else:
                    g.add_edges([(y, z)])
                    w = input('Qual o peso desta aresta?\n')
                    lista.append(w)
            else:
                g.es["weight"] = lista
                break
    g.vs["label"] = g.vs["name"]
    g.es["label"] = g.es["weight"]
    layout = g.layout("kk")
    print 'Grafo criado com sucesso!'
    plot(g, layout=layout)

# ----------------------------------------------------------------------ALGORITMOS-----------------------------------------------
def dijkstra():
    global g
    global vertices
    global arestas
    global pesos
    v_visitados = []
    predecessor = {}
    custo = {}
    menor_custo = {}

    # mensagem de boas vindas / relembrar quais vertices existem no grafo
    print '\nVoce selecionou o algoritmo de DIJKSTRA\nA seguir o nome dos vertices do seu grafo:\nV = {',
    for i in range(len(vertices)):
        if (i < len(vertices)-1):
            print vertices[i] + ', ',
        else:
            print vertices[i] + ' }'

    # loop para selecionar vertice raiz
    while True:
        no_inicial = raw_input('Qual sera o seu no inicial(Raiz)?\n')
        if (no_inicial not in vertices):
            print 'Por favor, digite um vertice que realmente exista no grafo\nA seguir os vertices do seu grafo:\nV = {',
            for i in range(len(vertices)):
                if (i < len(vertices)-1):
                    print vertices[i] + ', ',
                else:
                    print vertices[i] + ' }'
        else:
            break

    # inicializando o dijkstra
    v_visitados.append(no_inicial)
    predecessor[no_inicial] = '0'
    menor_custo[no_inicial] = 0
    for i in range(len(arestas)):
        custo[arestas[i]] = pesos[i]

    # descobrir os vizinhos do vertice raiz



#g.vcount()
#g.ecount()



# ----------------------------------------------------------------------MAIN-----------------------------------------------------
def main():
    global n
    menu()
    while (n != 5):
        criar_grafo()
        if (n == 1):
            dijkstra()
        menu(False)

if __name__ == "__main__":
    main()








