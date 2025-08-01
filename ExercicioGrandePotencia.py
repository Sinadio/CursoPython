# Crie um método que teste se o resultado da elevação de um número a outro resulta num resultado superior a 5000. Utilizaremos uma instrução condicional para devolver Verdadeiro se o resultado for superior a 5000 ou Falso se não for. Para tal, necessitaremos dos seguintes passos:
#Defina a função para aceitar dois parâmetros de entrada denominados base e expoente
#Calcular o resultado da base elevada à potência do expoente
#utilize uma instrução if para testar se o resultado é superior a 5000. Se for, devolva True . Caso contrário, devolva False.


def elevado(base, expoente):
    resultado = base ** expoente
    if resultado > 5000:
        return True
    else:
        return False

# Entradas do utilizador
b = int(input("Insira uma base: "))
e = int(input("Insira um expoente: "))

# Verificar o resultado
if elevado(b, e):
    print(f"A base {b} elevada ao expoente {e} é superior a 5000.")
else:
    print(f"A base {b} elevada ao expoente {e} é inferior ou igual a 5000.")
