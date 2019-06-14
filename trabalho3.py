#!/usr/bin/python

# DANIEL GOBBI BERGHOLZ 16/0004551
# TRABALHO 3 FUNDAMENTOS DE REDES 1

from igraph import *
import os

# variavel global para ir armazenando decisoes do usuario 
n = 0

# criar grafo
g = Graph() 

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

def menu(primeira_vez=True):
    if (primeira_vez == True):
        os.system('clear')
        print 'Seja bem vindo ao meu programa que simula grafos\n'
    print 'A seguir os algoritmos disponiveis:\n'
    print '1) Dijkstra\n2) Bellman-Ford\n3) RPF\n4) Spanning Tree\n5) SAIR'
    global n  
    n = input('Por favor, selecione um algoritmo que vc gostaria de executar:\n')
    while (n < 1 or n > 5):
        n = input('Escolha um numero valido (entre 1 e 5):\n')

def criar_grafo():
    print 'Agora iremos criar seu grafo de testes\n'
    y = raw_input('Voce gostaria de carregar um grafo a partir de um arquivo .DOT? (s/n)\n')
    if (y == 's'):
        print 'kk eae men'
        # fazer algo aqui depois
    else:
        x = input('Quantos vertices tem seu grafo?\n')
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
#def dijkstra(grafo, no_inicial):




# ----------------------------------------------------------------------MAIN-----------------------------------------------------
def main():
    global n
    menu()
    while (n != 5):
        criar_grafo()
        menu(False)

if __name__ == "__main__":
    main()
