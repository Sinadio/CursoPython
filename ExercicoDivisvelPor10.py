
# Definimos uma função chamada divisivel_por_dez que recebe um parâmetro chamado num
def divisivel_por_dez(num):
    # Usamos o operador módulo (%) para verificar se o resto da divisão por 10 é igual a 0
    # Se for, a função retorna True (divisível por 10), senão retorna False
    return num % 10 == 0

# Solicitamos ao utilizador que digite um número inteiro
numero = int(input("Digite um número: "))

# Chamamos a função divisivel_por_dez e verificamos o valor retornado
if divisivel_por_dez(numero):
    # Se a função retornar True, imprimimos que o número é divisível por 10
    print(f"O número {numero} é divisível por 10.")
else:
    # Caso contrário, imprimimos que o número NÃO é divisível por 10
    print(f"O número {numero} NÃO é divisível por 10.")
