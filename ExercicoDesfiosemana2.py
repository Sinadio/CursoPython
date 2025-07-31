###
#


#Crie uma lista vazia chamada my_list .
#Adicione os seguintes elementos à minha_lista : 10, 20, 30, 40.
#Introduza o valor 15 na segunda posição da lista.
#Estenda my_list com outra lista: [50, 60, 70].
#Remova o último elemento de my_list .
#Classifique my_list   por ordem crescente.
#Encontre e imprima o índice do valor 30 em my_list .
#
# ###

lista =[]

lista.append(10)
lista.append(20)
lista.append(30)
lista.append(40)

print(lista)

lista.insert(1, 15)
print(lista)

lista.extend([50, 60, 70])

print('Lista extendida: ',lista)

print("Lista sem o ultimo elemento: ", lista.pop())
print(lista)
lista.sort()
print('Lista iprimida em ordem crescente: ',lista )

indice_30 = lista.index(30)

# Mostrar resultados
print("Lista final:", lista)
print("Índice do valor 30:", indice_30)