###
#
# Escreva um programa que aceite a entrada do utilizador
# para criar dois conjuntos de números inteiros.
# De seguida, crie um novo conjunto que contenha apenas
# os elementos comuns a ambos os conjuntos.
# ###

# Programa que cria dois conjuntos com números inseridos pelo utilizador
# e mostra apenas os elementos comuns (interseção)

# Entrada de dados
conjunto1 = set(map(int, input("Digite números para o primeiro conjunto, separados por espaço: ").split()))
conjunto2 = set(map(int, input("Digite números para o segundo conjunto, separados por espaço: ").split()))

# Interseção entre os conjuntos
comuns = conjunto1 & conjunto2  # ou: conjunto1.intersection(conjunto2)

# Resultado
print("\nElementos comuns aos dois conjuntos:")
print(comuns)
