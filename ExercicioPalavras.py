###
#Programa que filtra palavras com número ímpar de caracteres usando compreensão de listas
#
# ###

lista = []
dados = ''
tamanho = int(input('Insira o tamanho da lista: '))

for i in range(tamanho):

    dados = input("Insira dados na lista:")
    lista.append(dados)

print(lista)

# Usando compreensão de lista para selecionar palavras com número ímpar de caracteres
palavras_impares = [palavra for palavra in lista if len(palavra) % 2 != 0]


print("\nPalavras com número ímpar de caracteres:")
print(palavras_impares)


