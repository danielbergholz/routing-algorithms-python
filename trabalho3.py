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


# ------------------------------------------------------------FUNCOES-DOS-ALGORITMOS-----------------------------------------------
# descobrir os vizinhos de um vertice e salvar na variavel adjacentes
def vizinhos(arestas, vertice, primeira_vez = False):
    aux = []
    predecessor = {}
    adjacentes = {}
    for i in range(len(arestas)):
        for j in range(2):
            if(arestas[i][j] == vertice):
                if(j == 1):
                    predecessor[arestas[i][0]] = arestas[i]
                    aux.append(arestas[i])
                elif (j == 0):
                    aux.append(arestas[i])
                    predecessor[arestas[i][1]] = arestas[i]
    adjacentes[vertice] = aux
    if (primeira_vez == True):
        return predecessor, adjacentes
    if (primeira_vez == False):
        return adjacentes
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
    adjacentes = {}
    no_inicial = ''
    no_final = ''

    # mensagem de boas vindas / relembrar quais vertices existem no grafo
    print '\nVoce selecionou o algoritmo de DIJKSTRA\nA seguir o nome dos vertices do seu grafo:\nV = {',
    for i in range(len(vertices)):
        if (i < len(vertices)-1):
            print vertices[i] + ', ',
        else:
            print vertices[i] + ' }'

    # loop para selecionar vertice raiz e destino
    while True:
        no_inicial = raw_input('Qual sera o seu no inicial(Raiz)?\n')
        no_final = raw_input('E o seu no final?\n')
        if ((no_inicial not in vertices) or (no_final not in vertices)):
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
    menor_custo[no_inicial] = 0
    for i in range(len(arestas)):
        custo[arestas[i]] = pesos[i]
    predecessor, adjacentes =  vizinhos(arestas, no_inicial, True)
    dict = {}
    for v in vertices:
        if (v not in predecessor) and (v != no_inicial):
            menor_custo[v] = 999
        if v in predecessor:
            menor_custo[v] = custo[predecessor[v]]

    # salva em adjacentes todas as arestas que sao adjacentes em cada vertice
    for v in vertices:
        dict = vizinhos(arestas, v)
        adjacentes.update(dict)
   
#    print 'ANTES DO DIJKSTRA'
#    print predecessor
#    print adjacentes
#    print menor_custo
#    print '\n'

    # agora comecando de verdade o algoritmo
    predecessor_aux = {}
    falta_vertice = True
    while True:
        for p in predecessor:
            for a in adjacentes[p]:
                if (a != predecessor[p]):
                    for tupla in a:
                        if (tupla != p):
                            if ((menor_custo[p] + custo[a]) < menor_custo[tupla]):
                                aux =  menor_custo[p] + custo[a]
                                aux2 = aux%(int(aux))
                                if ((aux2 > 0.09) and (aux2 < 0.1)):
                                    aux = int(aux) + 0.1
                                elif (aux2 < 0.009): 
                                    aux = int(aux)
                                menor_custo[tupla] = aux
                                predecessor_aux[tupla] = a
        predecessor.update(predecessor_aux)
        falta_vertice = False
        for v in vertices:
            if v not in predecessor:
                if(v != no_inicial):
                    falta_vertice = True
        if falta_vertice == False:
            break
#    print 'DEPOIS DO DIJKSTRA'
#    print predecessor
#    print adjacentes
#    print menor_custo
#    print '\n'
   
    # printar na tela o menor caminho e o menor custo
    aux = []
    cont = 0
    cabou = False
    print 'O menor caminho entre ' + no_inicial + ' e ' + no_final + ' eh: ',
    aux.append(no_final)
    while cabou == False:
        for tupla in predecessor[aux[cont]]:
            if (tupla == no_inicial):
                cabou = True
            if (tupla != aux[cont]):
                aux.append(tupla)
                a = cont + 1
        cont = a
    aux = aux[::-1]
                
    for i in range(len(aux)):
        if (i == (len(aux)-1)):
            print aux[i]
        else:
            print aux[i] + ' -> ',
    print 'Com o custo total de: ' + str(menor_custo[no_final])
    print 'A seguir a arvore de caminho minimo criada pelo DIJKSTRA:'

    # printar arvore criada para o dijkstra
    t = Graph()
    t.add_vertices(len(vertices))
    arestas_final = []
    lista = []
    for p in predecessor:
        arestas_final.append(predecessor[p])
        lista.append(custo[predecessor[p]])
    t.vs["name"] = vertices
    t.add_edges(arestas_final)
    t.es["weight"] = lista
    t.vs["label"] = t.vs["name"]
    t.es["label"] = t.es["weight"]
    cont = 0
    for v in vertices:
        if(v == no_inicial):
            break
        cont = cont + 1
    lista = []
    lista.append(cont)
    layout = t.layout("tree", root = lista)
    plot(t, layout=layout)

#g.vcount()
#g.ecount()

# o algoritmo usado na spanning tree foi o de Kruskal
def spanning_tree():
    global g
    global vertices
    global arestas
    global pesos
    antes = {}
    depois = {}
    arestas2 = []
    pesos2 = []
    
    print 'Voce selecionou o algoritmo de SPANNING TREE\nA partir do seu grafo, sera construida uma arvore minima:'
    print 'VERTICES: ' + str(vertices)
    print 'ARESTAS: ' + str(arestas)
    print 'PESOS: ' + str(pesos)

    for i in range(len(vertices)):
        antes[arestas[i]] = pesos[i]
    print antes
    menor = pesos
    menor.sort()
    arestas2.append
'''
    t = Graph()
    t.add_vertices(len(vertices))
    for p in predecessor:
        arestas_final.append(predecessor[p])
        lista.append(custo[predecessor[p]])
    t.vs["name"] = vertices
    t.add_edges(arestas_final)
    t.es["weight"] = lista
    t.vs["label"] = t.vs["name"]
    t.es["label"] = t.es["weight"]
    cont = 0
    for v in vertices:
        if(v == no_inicial):
            break
        cont = cont + 1
    lista = []
    lista.append(cont)
    layout = t.layout("tree", root = lista)
    plot(t, layout=layout)
'''

# ----------------------------------------------------------------------MAIN-----------------------------------------------------
def main():
    menu()
    while (n != 5):
        criar_grafo()
        if (n == 1):
            dijkstra()
        elif n == 4:
            spanning_tree()
        menu(False)

if __name__ == "__main__":
    main()








