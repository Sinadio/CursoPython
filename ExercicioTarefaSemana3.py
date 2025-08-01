

def calcula_discount(preco, percent):

     if(percent >=20):
         valordescontado = preco * (percent / 100)

         precoComDescon = preco - valordescontado
         return precoComDescon
     else:
         return preco
preco = float(input("Insira o valor original: "))
percentagem = float(input("Insira a percentagem: "))

#chamando funcao

precoFinal = calcula_discount(preco, percentagem)

if percentagem >= 20:
    print(f"O preço final com desconto é: {precoFinal:.2f} MT")
else:
    print(f"Desconto insuficiente. O preço permanece: {precoFinal:.2f} MT")