class Car:
    def __init__(self, cor, modelo):

        self.cor = cor
        self.modelo = modelo

    #Criando variaveis com um unico valor

car1 = Car("Blue", "BMW")
car2 = Car("Red", "AMG")

print(car1.cor)
print(car2.modelo)