###Crie um programa Python simples que peça ao utilizador para introduzir dois números e uma operação matemática
# (adição, subtração,
# multiplicação ou divisão).
#Execute a operação com base na entrada do utilizador e imprima o resultado.
#Exemplo: Se um utilizador introduzir 10, 5, e +, o seu programa deve exibir 10 + 5 = 15.###

n1 = int(input('Insira Um número: '))
n2 = int(input('insira o segundo número:'))

print('Podes fazer as seguintes operações: A)Soma, B)Divisão, C)Subtração e D)Multiplicação')

res = input('Sua Escolha: ').upper()

if(res == 'A'):

    soma = n1 + n2
    print(n1, '+' , n2 , '=', soma)

elif(res == 'B'):

    div = n1/n2
    print(n1, '/', n2, '=', div)

elif(res == 'C'):

    sub = n1 - n2
    print(n1, '-', n2, '=', sub)

elif(res == 'D'):

    mult = n1 * n2
    print(n1, '*', n2, '=', mult)
else:
    print('Operação Invalida!')
