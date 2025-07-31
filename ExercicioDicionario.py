###
# Escreva um programa que utilize um dicionário para armazenar informação sobre uma pessoa, como o nome,
# a idade e a cor favorita. Peça ao utilizador uma entrada e armazene a informação no dicionário.
# Em seguida, imprima o dicionário na consola.
# ###

pessoa ={}

pessoa["nome"]=input("insira seu nome: ")
pessoa["idade"]=int(input("Insira a idade:"))
pessoa["cor favorita"]=input("Insira a sua cor favorita:")

print("\n Dados da Pessoa: ")
print(pessoa)